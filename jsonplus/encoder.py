import json as stdlib_json
from collections import ChainMap
from contextlib import suppress
from itertools import chain

from jsonplus.default_encoders import DEFAULT_FUNCTIONAL_ENCODERS, DEFAULT_TYPED_ENCODERS
from jsonplus.null_dict import NULL_DICT


__all__ = ["JSONEncoderPlus"]


class FUNCTIONAL:
    pass


class JSONEncoderPlus(stdlib_json.JSONEncoder):
    default_typed_encoders = DEFAULT_TYPED_ENCODERS
    default_functional_encoders = DEFAULT_FUNCTIONAL_ENCODERS

    def __init__(self, *args, functional_encoders=(), typed_encoders: dict[type, callable] = NULL_DICT, **kwargs):
        super().__init__(*args, **kwargs)

        self._typed_encoders = {**typed_encoders}
        self._functional_encoders = [*functional_encoders]

    @property
    def functional_encoders(self):
        return chain(self._functional_encoders, self.default_functional_encoders)

    @property
    def typed_encoders(self):
        return ChainMap(self._typed_encoders, self.default_typed_encoders)

    def register(self, function, type_=FUNCTIONAL):
        if type_ is FUNCTIONAL:
            self._functional_encoders.append(function)
        else:
            self.typed_encoders[type_] = function

    def default(self, o):
        type_ = type(o)

        if encoder := self.typed_encoders.get(type_):
            return encoder(o)

        for encoder in self.functional_encoders:
            with suppress(Exception):
                return encoder(o)

        return super().default(o)
