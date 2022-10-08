import datetime
import json as stdlib_json


class JSONDecoderPlus(stdlib_json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.hook, *args, **kwargs)

    @staticmethod
    def hook(source):
        d = {}
        for k, v in source.items():
            if isinstance(v, str) and not v.isdigit():
                try:
                    d[k] = datetime.datetime.fromisoformat(v)
                except (ValueError, TypeError):
                    d[k] = v
            else:
                d[k] = v

        return d
