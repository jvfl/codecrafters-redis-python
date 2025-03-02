from app.protocol import ArrayCodec

import pytest


class TestArrayParser:
    @pytest.fixture
    def subject(self) -> ArrayCodec:
        return ArrayCodec()

    class TestDecode:
        class TestWhenArrayIsNotEmpty:
            def test_it_returns_the_parsed_array(self, subject: ArrayCodec) -> None:
                assert subject.decode("*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n") == [
                    "LLEN",
                    "mylist",
                ]

        class TestWhenArrayIsEmpty:
            def test_it_returns_empty_array(self, subject: ArrayCodec) -> None:
                assert subject.decode("*0\r\n") == []

        class TestWhenArrayIsNull:
            def test_it_returns_empty_array(self, subject: ArrayCodec) -> None:
                assert subject.decode("*-1\r\n") == []

        class TestWhenArrayHasNestedElements:
            def test_it_returns_nested_array(self, subject: ArrayCodec) -> None:
                input_data = "*2\r\n*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n$4\r\nPING\r\n"
                assert subject.decode(input_data) == [["LLEN", "mylist"], "PING"]

    class TestEncode:
        class TestWhenArrayIsNotEmpty:
            def test_it_encodes_simple_array(self, subject: ArrayCodec) -> None:
                assert (
                    subject.encode(["LLEN", "mylist"])
                    == "*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n"
                )

        class TestWhenArrayIsEmpty:
            def test_it_encodes_empty_array(self, subject: ArrayCodec) -> None:
                assert subject.encode([]) == "*0\r\n"

        class TestWhenArrayHasNestedElements:
            def test_it_encodes_nested_array(self, subject: ArrayCodec) -> None:
                input_data = [["LLEN", "mylist"], "PING"]
                expected = "*2\r\n*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n$4\r\nPING\r\n"
                assert subject.encode(input_data) == expected
