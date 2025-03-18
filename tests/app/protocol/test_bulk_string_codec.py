from app.protocol import BulkStringCodec


class TestBulkStringParser:
    class TestDecode:
        class TestWhenDataIsNotEmpty:
            def test_it_returns_the_parsed_data(self) -> None:
                assert BulkStringCodec.decode("$6\r\nfoobar\r\n") == "foobar"

        class TestWhenDataIsEmpty:
            def test_it_returns_an_empty_string(self) -> None:
                assert BulkStringCodec.decode("$0\r\n\r\n") == ""

        class TestWhenDataIsNull:
            def test_it_returns_an_empty_string(self) -> None:
                assert BulkStringCodec.decode("$-1\r\n") == ""

    class TestEncode:
        class TestWhenDataIsNotEmpty:
            def test_it_encodes_the_data(self) -> None:
                assert BulkStringCodec.encode("foobar") == "$6\r\nfoobar\r\n".encode()

        class TestWhenDataIsEmpty:
            def test_it_encodes_the_data(self) -> None:
                assert BulkStringCodec.encode("") == "$0\r\n\r\n".encode()

        class TestWhenDataIsNull:
            def test_it_encodes_the_data(self) -> None:
                assert BulkStringCodec.encode(None) == "$-1\r\n".encode()
