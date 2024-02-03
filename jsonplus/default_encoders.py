import datetime
import decimal
import uuid


try:
    from django.db.models import Model
    from django.forms.models import model_to_dict

    DJANGO_ENCODERS = {
        Model: model_to_dict,
    }
except ImportError:
    DJANGO_ENCODERS = {}

try:
    from pydantic import BaseModel

    PYDANTIC_ENCODERS = {
        BaseModel: lambda o: o.dict(),
    }
except ImportError:
    PYDANTIC_ENCODERS = {}


def encode_timedelta_as_iso_string(duration):
    sign = "-" if duration < datetime.timedelta(0) else ""
    duration = abs(duration)
    total_seconds = int(duration.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms = f".{duration.microseconds:06d}" if duration.microseconds else ""
    return f"{sign}P{days}DT{hours:02d}H{minutes:02d}M{seconds:02d}{ms}S"


DEFAULT_ENCODERS = {
    datetime.datetime: lambda o: o.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    datetime.date: lambda o: o.isoformat(),
    datetime.time: lambda o: o.isoformat(timespec="milliseconds"),
    datetime.timedelta: encode_timedelta_as_iso_string,
    decimal.Decimal: str,
    uuid.UUID: str,
    complex: lambda o: [o.real, o.imag],
    bytes: lambda o: o.decode("utf-8"),
    set: list,
    frozenset: list,
    **DJANGO_ENCODERS,
    **PYDANTIC_ENCODERS,
}
