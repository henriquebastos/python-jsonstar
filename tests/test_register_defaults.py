import pytest

import jsonstar
from jsonstar import JSONEncoderStar


class CustomType:
    """
    CustomType to test our implementation of the default method.
    Types supported by the standard JSONEncoder are encoded before our code run.
    """


class TestDefaultEncoderRegistration:
    @pytest.fixture
    def empty_encoder(self, monkeypatch):
        monkeypatch.setattr(jsonstar.JSONEncoderStar, "default_functional_encoders", [])
        monkeypatch.setattr(jsonstar.JSONEncoderStar, "default_typed_encoders", {})

    def test_register_default_encoder_with_module_api(self, empty_encoder):
        jsonstar.register_default_encoder(lambda o: "functional default encoder")
        jsonstar.register_default_encoder(lambda o: "typed default encoder", CustomType)

        assert jsonstar.dumps(CustomType()) == '"typed default encoder"'
        assert jsonstar.dumps(object()) == '"functional default encoder"'

    def test_register_default_encoder_with_classmethod(self, empty_encoder):
        JSONEncoderStar.register_default_encoder(lambda o: "functional default encoder")
        JSONEncoderStar.register_default_encoder(lambda o: "typed default encoder", CustomType)

        assert jsonstar.dumps(CustomType()) == '"typed default encoder"'
        assert jsonstar.dumps(object()) == '"functional default encoder"'
