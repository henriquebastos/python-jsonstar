import json


class ResponsesSequence:
    def __init__(self, *triplets):
        self._responses = triplets
        self._it = None

    def __iter__(self):
        for status, headers, body in self._responses:
            if not isinstance(body, str):
                body = json.dumps(body)

            yield status, headers, body

    def __call__(self, request):
        if not self._it:
            self._it = iter(self)

        return next(self._it)