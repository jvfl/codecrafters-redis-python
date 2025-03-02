from ._bulk_string_codec import BulkStringCodec

import re

from typing import Any, cast


class ArrayCodec:
    """
    RESP Arrays' encoding uses the following format:

    *<number-of-elements>\r\n<element-1>...<element-n>
    An asterisk (*) as the first byte.
    One or more decimal digits (0..9) as the number of elements in the array as
    an unsigned, base-10 value.
    The CRLF terminator.
    An additional RESP type for every element of the array.


    So an empty Array is just the following:

    *0\\r\\n
    Whereas the encoding of an array consisting of the two bulk strings "hello"
    and "world" is:

    *2\\r\\n$5\\r\\nhello\\r\\n$5\\r\\nworld\r\n
    """

    bulk_string_codec = BulkStringCodec()

    def decode(self, data) -> list[str]:
        elements = re.split(r"(\$|\*)", data)

        number_of_elements = int(elements[2])

        if number_of_elements < 0:
            return []

        return self._extract_elements(elements[3:])

    def encode(self, data: list[Any]) -> str:
        acc = [f"*{len(data)}"]

        for element in data:
            if isinstance(element, list):
                acc.append(self.encode(element).removesuffix("\r\n"))
            elif isinstance(element, str):
                acc.append(f"${len(element)}\r\n{element}")

        return "\r\n".join(acc) + "\r\n"

    def _extract_elements(self, elements: list[str]) -> list[Any]:
        acc = []

        iterable = iter(elements)
        for element in iterable:
            if element == "*":
                number_of_elements = int(next(iterable))

                inner_elements = [next(iterable) for _ in range(number_of_elements * 2)]

                acc.append(self._extract_elements(inner_elements))
            elif element == "$":
                bulk_string = self.bulk_string_codec.decode(next(iterable))
                acc.append(cast(Any, bulk_string))
            else:
                continue

        return acc
