import uuid
from datetime import date, datetime, time, timedelta

import attrs
import pytest
from freezegun import freeze_time
from pydantic import BaseModel
from pytz import timezone

from jsonplus import JSONEncoderPlus


def encode(o):
    return JSONEncoderPlus().encode(o).strip("'\"")


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
        assert encode(dt) == expected


class TestDateEncoder:
    def test_encode_date_as_iso_string(self):
        assert encode(date(2022, 1, 1)) == "2022-01-01"

    def test_encode_date_as_iso_string_edge_case(self):
        assert encode(date(1, 1, 1)) == "0001-01-01"


class TestTimeEncoder:
    def time_encoder_handles_valid_time(self):
        assert encode(time(13, 45, 30, 123456)) == "13:45:30.123"

    def time_encoder_handles_edge_case_no_microseconds(self):
        assert encode(time(0, 0, 0)) == "00:00:00.000"

    def time_encoder_handles_edge_case_max_time(self):
        assert encode(time(23, 59, 59, 999999)) == "23:59:59.999"


class TestTimedeltaEncoder:
    def test_encode_timedelta_as_iso_string_positive_duration(self):
        duration = timedelta(days=2, hours=3, minutes=4, seconds=5)
        assert encode(duration) == "P2DT03H04M05S"

    def test_encode_timedelta_as_iso_string_negative_duration(self):
        duration = timedelta(days=-2, hours=-3, minutes=-4, seconds=-5)
        assert encode(duration) == "-P2DT03H04M05S"

    def test_encode_timedelta_as_iso_string_zero_duration(self):
        duration = timedelta(0)
        assert encode(duration) == "P0DT00H00M00S"

    def test_encode_timedelta_as_iso_string_with_microseconds(self):
        duration = timedelta(seconds=1, microseconds=123456)
        assert encode(duration) == "P0DT00H00M01.123456S"


class TestDecimalEncoder:
    def test_decimal_encoder_handles_valid_decimal(self):
        from decimal import Decimal

        assert encode(Decimal("10.5")) == "10.5"

    def test_decimal_encoder_handles_zero(self):
        from decimal import Decimal

        assert encode(Decimal("0")) == "0"

    def test_decimal_encoder_handles_negative_decimal(self):
        from decimal import Decimal

        assert encode(Decimal("-10.5")) == "-10.5"


class TestUUIDEncoder:
    def test_uuid_encoder_handles_valid_uuid(self):
        u = uuid.uuid4()
        assert encode(u) == str(u)


class TestSetEncoder:
    def test_set_encoder_handles_valid_set(self):
        assert encode({1, 2, 3}) == "[1, 2, 3]"

    def test_set_encoder_handles_empty_set(self):
        assert encode(set()) == "[]"

    def test_set_encoder_handles_set_with_multiple_same_elements(self):
        assert encode({1, 1, 2, 2, 3, 3}) == "[1, 2, 3]"


class TestFrozensetEncoder:
    def test_frozenset_encoder_handles_valid_frozenset(self):
        assert encode(frozenset({1, 2, 3})) == "[1, 2, 3]"

    def test_frozenset_encoder_handles_empty_frozenset(self):
        assert encode(frozenset()) == "[]"

    def test_frozenset_encoder_handles_frozenset_with_multiple_same_elements(self):
        assert encode(frozenset({1, 1, 2, 2, 3, 3})) == "[1, 2, 3]"


@freeze_time("2024-01-01")
class TestDjangoModelEncoder:
    @pytest.fixture(autouse=True, scope="class")
    def user(self):
        import django
        from django.conf import settings

        settings.configure(
            INSTALLED_APPS=[
                "django.contrib.auth",
                "django.contrib.contenttypes",
            ]
        )
        django.setup()

        from django.contrib.auth.models import User

        return User

    def test_django_model_encoder_handles_valid_model(self, user):
        assert encode(user(username="testuser", password="testpass")) == (
            '{"id": null, "password": "testpass", "last_login": null, "is_superuser": false, "username": "testuser", '
            '"first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": '
            '"2024-01-01T00:00:00.000Z", "groups": [], "user_permissions": []}'
        )

    def test_django_model_encoder_handles_empty_model(self, user):
        assert encode(user()) == (
            '{"id": null, "password": "", "last_login": null, "is_superuser": false, "username": "", "first_name": "", '
            '"last_name": "", "email": "", "is_staff": false, "is_active": true, '
            '"date_joined": "2024-01-01T00:00:00.000Z", "groups": [], "user_permissions": []}'
        )

    def test_django_model_encoder_handles_model_with_null_fields(self, user):
        assert encode(user(username=None, password=None)) == (
            '{"id": null, "password": null, "last_login": null, "is_superuser": false, "username": null, '
            '"first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, '
            '"date_joined": "2024-01-01T00:00:00.000Z", "groups": [], "user_permissions": []}'
        )


class TestPydanticEncoder:
    def test_pydantic_encoder_handles_valid_model(self):
        class PydanticModel(BaseModel):
            id: int
            name: str

        assert encode(PydanticModel(id=1, name="test")) == '{"id": 1, "name": "test"}'

    def test_pydantic_encoder_handles_empty_model(self):
        from pydantic import BaseModel

        class PydanticModel(BaseModel):
            id: int = None
            name: str = None

        assert encode(PydanticModel()) == '{"id": null, "name": null}'


class TestAttrsFunctionalEncoders:
    def test_attrs_functional_encoders_are_not_empty_when_attrs_imported(self):
        @attrs.define
        class AttrsClass:
            x: int

        assert encode(AttrsClass(x=5)) == '{"x": 5}'
