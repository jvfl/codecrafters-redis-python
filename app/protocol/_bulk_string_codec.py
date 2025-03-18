from typing import Optional


class BulkStringCodec:
    """
    A bulk string represents a single binary string.

    RESP encodes bulk strings in the following way:

    ${length}\r\n{data}\r\n

    The dollar sign ($) as the first byte.
    One or more decimal digits (0..9) as the string's length, in bytes,
    as an unsigned, base-10 value.
    The CRLF terminator.
    The data.
    A final CRLF.

    The empty string's encoding is:

    $0\\r\\n\\r\\n

    A null bulk string's encoding is:
    $-1\\r\\n (for RESP 2)
    """

    @staticmethod
    def decode(data: str) -> str:
        """
        Parse a bulk string from a RESP message.

        :param data: The data to parse.
        :return: The parsed bulk string.
        """
        if data == "$-1\r\n":
            return ""
        elif data == "$0\r\n\r\n":
            return ""

        return data.split("\r\n")[1]

    @staticmethod
    def encode(data: Optional[str]) -> bytes:
        """
        Encode a string into a RESP message as bulk string
        """
        if data is None:
            return "$-1\r\n".encode()

        return f"${len(data)}\r\n{data}\r\n".encode()
