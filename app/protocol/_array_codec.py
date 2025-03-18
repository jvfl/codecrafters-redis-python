from ._bulk_string_codec import BulkStringCodec

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

    def decode(self, data: str) -> list[str]:
        number_prefix, elements = data.split("\r\n", 1)
        number_of_elements = int(number_prefix[1:])

        return self._extract_elements(elements, number_of_elements)

    def encode(self, data: list[Any]) -> str:
        acc = [f"*{len(data)}"]

        for element in data:
            if isinstance(element, list):
                acc.append(self.encode(element).removesuffix("\r\n"))
            elif isinstance(element, str):
                acc.append(f"${len(element)}\r\n{element}")

        return "\r\n".join(acc) + "\r\n"

    def _extract_elements(self, elements: str, number_of_elements: int) -> list[Any]:
        acc: list[Any] = []

        while len(acc) < number_of_elements:
            if elements.startswith("*"):
                array_values = self.decode(elements)
                elements = elements.replace(self.encode(array_values), "")
                acc.append(array_values)
            elif elements.startswith("$"):
                values = elements.split("\r\n", 2)
                elements = values[2]

                current_element = "\r\n".join(values[:2])
                bulk_string = BulkStringCodec.decode(current_element)
                acc.append(cast(Any, bulk_string))
            else:
                continue

        return acc
