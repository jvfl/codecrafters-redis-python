from app.protocol import BulkStringCodec

import pytest


class TestBulkStringParser:
    @pytest.fixture
    def subject(self) -> BulkStringCodec:
        return BulkStringCodec()

    class TestDecode:
        class TestWhenDataIsNotEmpty:
            def test_it_returns_the_parsed_data(self, subject: BulkStringCodec) -> None:
                assert subject.decode("$6\r\nfoobar\r\n") == "foobar"

        class TestWhenDataIsEmpty:
            def test_it_returns_an_empty_string(self, subject: BulkStringCodec) -> None:
                assert subject.decode("$0\r\n\r\n") == ""

        class TestWhenDataIsNull:
            def test_it_returns_an_empty_string(self, subject: BulkStringCodec) -> None:
                assert subject.decode("$-1\r\n") == ""

    class TestEncode:
        class TestWhenDataIsNotEmpty:
            def test_it_encodes_the_data(self, subject: BulkStringCodec) -> None:
                assert subject.encode("foobar") == "$6\r\nfoobar\r\n"

        class TestWhenDataIsEmpty:
            def test_it_encodes_the_data(self, subject: BulkStringCodec) -> None:
                assert subject.encode("") == "$0\r\n\r\n"
