from datetime import datetime

from requests.auth import AuthBase

from .sessions import EduzzSession


class EduzzToken(AuthBase):
    AUTH_PATH = "/credential/generate_token"
    TOKEN_EXPIRED_ERROR_CODE = "#0029"

    def __init__(self, email, publickey, apikey, session_class=EduzzSession):
        self.credentials = dict(email=email, publickey=publickey, apikey=apikey)
        self.session_class = session_class

        self._token = None
        self._token_valid_until = None

    @property
    def has_token(self):
        return bool(self._token)

    @property
    def is_expired(self):
        if self._token_valid_until is None:
            return True

        return datetime.now() > self._token_valid_until

    @property
    def token(self):
        if self.is_expired:
            self.renew()

        return self._token

    @token.setter
    def token(self, values):
        """For testing purpose only."""
        self._token, self._token_valid_until = values

    def renew(self):
        session = self.session_class()
        r = session.post(self.AUTH_PATH, params=self.credentials)
        r.raise_for_status()

        json = r.json()

        self._token = json["data"]["token"]
        self._token_valid_until = json["data"]["token_valid_until"]

    def handle_401(self, r, **kwargs):
        if r.status_code != 401:
            return r

        # Only try to recover if token expired
        json = r.json()
        if json["code"] != self.TOKEN_EXPIRED_ERROR_CODE:
            return r

        # force token renew
        self.renew()

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        r.content
        r.close()
        prep = r.request.copy()

        prep.headers["Token"] = self.token
        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep

        return _r

    def __call__(self, r):
        r.headers["Token"] = self.token
        r.register_hook("response", self.handle_401)
        return r
