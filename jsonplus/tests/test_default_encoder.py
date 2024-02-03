from datetime import datetime, timedelta

import pytest
from pytz import timezone

from jsonplus.default_encoders import encode_datetime_as_ecma262, encode_timedelta_as_iso_string


class TestDatetimeEncoder:
    @pytest.mark.parametrize(
        "tz,expected",
        [
            ("UTC", "2023-01-01T13:45:30.643Z"),
            ("US/Eastern", "2023-01-01T13:45:30.643-04:56"),
            ("America/Sao_Paulo", "2023-01-01T13:45:30.643-03:06"),
            ("Australia/Sydney", "2023-01-01T13:45:30.643+10:05"),
        ],
    )
    def test_encode_datetime_as_ecma262_different_timezones(self, tz, expected):
        dt = datetime(2023, 1, 1, 13, 45, 30, 643768, tzinfo=timezone(tz))
        assert encode_datetime_as_ecma262(dt) == expected


class TestTimedeltaEncoder:
    def test_encode_timedelta_as_iso_string_positive_duration(self):
        duration = timedelta(days=2, hours=3, minutes=4, seconds=5)
        assert encode_timedelta_as_iso_string(duration) == "P2DT03H04M05S"

    def test_encode_timedelta_as_iso_string_negative_duration(self):
        duration = timedelta(days=-2, hours=-3, minutes=-4, seconds=-5)
        assert encode_timedelta_as_iso_string(duration) == "-P2DT03H04M05S"

    def test_encode_timedelta_as_iso_string_zero_duration(self):
        duration = timedelta(0)
        assert encode_timedelta_as_iso_string(duration) == "P0DT00H00M00S"

    def test_encode_timedelta_as_iso_string_with_microseconds(self):
        duration = timedelta(seconds=1, microseconds=123456)
        assert encode_timedelta_as_iso_string(duration) == "P0DT00H00M01.123456S"
