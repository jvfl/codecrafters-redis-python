from app.protocol import ArrayCodec


class TestArrayParser:
    class TestDecode:
        class TestWhenArrayIsNotEmpty:
            def test_it_returns_the_parsed_array(self) -> None:
                assert ArrayCodec.decode("*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n") == [
                    "LLEN",
                    "mylist",
                ]

        class TestWhenArrayHasKeysArgument:
            def test_it_returns_the_parsed_array(self) -> None:
                assert ArrayCodec.decode("*2\r\n$4\r\nKEYS\r\n$1\r\n*\r\n") == [
                    "KEYS",
                    "*",
                ]

        class TestWhenArrayIsEmpty:
            def test_it_returns_empty_array(self) -> None:
                assert ArrayCodec.decode("*0\r\n") == []

        class TestWhenArrayIsNull:
            def test_it_returns_empty_array(self) -> None:
                assert ArrayCodec.decode("*-1\r\n") == []

        class TestWhenArrayHasNestedElements:
            def test_it_returns_nested_array(self) -> None:
                input_data = "*2\r\n*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n$4\r\nPING\r\n"
                assert ArrayCodec.decode(input_data) == [["LLEN", "mylist"], "PING"]

    class TestEncode:
        class TestWhenArrayIsNotEmpty:
            def test_it_encodes_simple_array(self) -> None:
                assert (
                    ArrayCodec.encode(["LLEN", "mylist"])
                    == "*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n".encode()
                )

        class TestWhenArrayIsEmpty:
            def test_it_encodes_empty_array(self) -> None:
                assert ArrayCodec.encode([]) == "*0\r\n".encode()

        class TestWhenArrayHasNestedElements:
            def test_it_encodes_nested_array(self) -> None:
                input_data = [["LLEN", "mylist"], "PING"]
                expected = "*2\r\n*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n$4\r\nPING\r\n"
                assert ArrayCodec.encode(input_data) == expected.encode()
