import json as stdlib_json

from jsonplus.default_encoders import DEFAULT_ENCODERS


class JSONEncoderPlus(stdlib_json.JSONEncoder):
    class_registry = DEFAULT_ENCODERS

    def __init__(self, *args, encoders=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_registry = encoders if encoders is not None else {}

    def register_instance(self, type_, function):
        self.instance_registry[type_] = function

    def default(self, o):
        type_ = type(o)
        if type_ in self.instance_registry:
            return self.instance_registry[type_](o)
        elif type_ in self.class_registry:
            return self.class_registry[type_](o)
        else:
            return super().default(o)
