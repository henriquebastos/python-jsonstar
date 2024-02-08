import json as stdlib_json

from jsonstar.decoder import JSONDecoderStar
from jsonstar.encoder import JSONEncoderStar


def dump(obj, fp, cls=JSONDecoderStar, **kwargs):
    return stdlib_json.dump(obj, fp, cls=cls, **kwargs)


def dumps(obj, cls=JSONEncoderStar, **kwargs):
    return stdlib_json.dumps(obj, cls=cls, **kwargs)


def load(fp, *, cls=None, **kwargs):
    return stdlib_json.load(fp, cls=cls, **kwargs)


def loads(obj, cls=JSONDecoderStar, **kwargs):
    return stdlib_json.loads(obj, cls=cls, **kwargs)


def register_default_encoder(function, type_=JSONEncoderStar.FUNCTIONAL):
    return JSONEncoderStar.register_default_encoder(function, type_)
