import json as stdlib_json

from jsonplus.decoder import JSONDecoderPlus
from jsonplus.encoder import JSONEncoderPlus


def dump(obj, fp, cls=JSONDecoderPlus, **kwargs):
    return stdlib_json.dump(obj, fp, cls=cls, **kwargs)


def dumps(obj, cls=JSONEncoderPlus, **kwargs):
    return stdlib_json.dumps(obj, cls=cls, **kwargs)


def load(fp, *, cls=None, **kwargs):
    return stdlib_json.load(fp, cls=cls, **kwargs)


def loads(obj, cls=JSONDecoderPlus, **kwargs):
    return stdlib_json.loads(obj, cls=cls, **kwargs)


def register_default_encoder(function, type_=JSONEncoderPlus.FUNCTIONAL):
    return JSONEncoderPlus.register_default_encoder(function, type_)
