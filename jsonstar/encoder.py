import inspect
import json as stdlib_json
from collections import ChainMap, OrderedDict
from contextlib import suppress
from itertools import chain

from jsonstar.default_encoders import DEFAULT_FUNCTIONAL_ENCODERS, DEFAULT_TYPED_ENCODERS
from jsonstar.null_dict import NULL_DICT


__all__ = ["JSONEncoderStar"]


class TypedEncoderRegistry(OrderedDict):
    def __setitem__(self, type_, function):
        """Register the type encoder and ensures inherited takes precedence over its base types encoders."""
        super().__setitem__(type_, function)
        for base in inspect.getmro(type_):
            if base in self:
                self.move_to_end(base)


class JSONEncoderStar(stdlib_json.JSONEncoder):
    class FUNCTIONAL:
        """Sentinel type to register a functional encoder."""

    default_typed_encoders = TypedEncoderRegistry(DEFAULT_TYPED_ENCODERS)
    default_functional_encoders = DEFAULT_FUNCTIONAL_ENCODERS

    def __init__(self, *args, functional_encoders=(), typed_encoders: dict[type, callable] = NULL_DICT, **kwargs):
        super().__init__(*args, **kwargs)

        self._typed_encoders = TypedEncoderRegistry(typed_encoders)
        self._functional_encoders = [*functional_encoders]

    @property
    def functional_encoders(self):
        return chain(self._functional_encoders, self.default_functional_encoders)

    @property
    def typed_encoders(self):
        return ChainMap(self._typed_encoders, self.default_typed_encoders)

    def register(self, function, type_=FUNCTIONAL):
        if type_ is self.FUNCTIONAL:
            self._functional_encoders.append(function)
        else:
            self._typed_encoders[type_] = function

    @classmethod
    def register_default_encoder(cls, function, type_=FUNCTIONAL):
        if type_ is cls.FUNCTIONAL:
            cls.default_functional_encoders.append(function)
        else:
            cls.default_typed_encoders[type_] = function

    def default(self, o) -> str:
        for base, encoder in self.typed_encoders.items():
            if isinstance(o, base):
                return encoder(o)

        for encoder in self.functional_encoders:
            with suppress(Exception):
                return encoder(o)

        return super().default(o)
