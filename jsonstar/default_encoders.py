import dataclasses
import datetime
import decimal
import uuid


try:
    from django.db.models import Model
    from django.forms.models import model_to_dict

    DJANGO_TYPED_ENCODERS = {
        Model: model_to_dict,
    }
except ImportError:
    DJANGO_TYPED_ENCODERS = {}


try:
    from pydantic import BaseModel

    def pydantic_dict(o):
        return o.dict()

    PYDANTIC_TYPED_ENCODERS = {
        BaseModel: pydantic_dict,
    }
except ImportError:
    PYDANTIC_TYPED_ENCODERS = {}


try:
    import attrs

    def attrs_dict(o):
        return attrs.asdict(o)

    ATTRS_FUNCTIONAL_ENCODERS = [attrs_dict]
except ImportError:
    ATTRS_FUNCTIONAL_ENCODERS = ()


def encode_timedelta_as_iso_string(duration):
    sign = "-" if duration < datetime.timedelta(0) else ""
    duration = abs(duration)
    total_seconds = int(duration.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms = f".{duration.microseconds:06d}" if duration.microseconds else ""
    return f"{sign}P{days}DT{hours:02d}H{minutes:02d}M{seconds:02d}{ms}S"


def dataclasses_asdict(o):
    return dataclasses.asdict(o)


DEFAULT_FUNCTIONAL_ENCODERS = [
    dataclasses_asdict,
    *ATTRS_FUNCTIONAL_ENCODERS,
]

DEFAULT_TYPED_ENCODERS = {
    datetime.datetime: lambda o: o.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    datetime.date: lambda o: o.isoformat(),
    datetime.time: lambda o: o.isoformat(timespec="milliseconds"),
    datetime.timedelta: encode_timedelta_as_iso_string,
    decimal.Decimal: str,
    uuid.UUID: str,
    set: list,
    frozenset: list,
    **DJANGO_TYPED_ENCODERS,
    **PYDANTIC_TYPED_ENCODERS,
}
