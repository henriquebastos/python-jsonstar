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
        monkeypatch.setattr(jsonstar.JSONEncoderStar, "_default_functional_encoders", [])
        monkeypatch.setattr(jsonstar.JSONEncoderStar, "_default_typed_encoders", {})

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


class TestIsolateDefaultsFromEncoderClasses:
    def test_isolate_functional_defaults_from_different_encoder_classes(self):
        class EncoderA1(JSONEncoderStar):
            pass

        class EncoderA2(EncoderA1):
            pass

        class EncoderB1(JSONEncoderStar):
            pass

        def a1(o):
            return o

        def a2(o):
            return o

        def b1(o):
            return o

        default_functional_encoders = JSONEncoderStar._default_functional_encoders.copy()

        EncoderA1.register_default_encoder(a1)
        EncoderA2.register_default_encoder(a2)
        EncoderB1.register_default_encoder(b1)

        assert JSONEncoderStar.default_functional_encoders() == default_functional_encoders
        assert EncoderA1.default_functional_encoders() == [a1] + default_functional_encoders
        assert EncoderA2.default_functional_encoders() == [a2, a1] + default_functional_encoders
        assert EncoderB1.default_functional_encoders() == [b1] + default_functional_encoders

    def test_isolate_typed_defaults_from_different_encoder_classes(self):
        class EncoderA1(JSONEncoderStar):
            pass

        class EncoderA2(EncoderA1):
            pass

        class EncoderB1(JSONEncoderStar):
            pass

        def a1(o):
            return o

        def a2(o):
            return o

        def b1(o):
            return o

        default_typed_encoders = JSONEncoderStar._default_typed_encoders.copy()

        EncoderA1.register_default_encoder(a1, str)
        EncoderA1.register_default_encoder(a1, int)
        EncoderA2.register_default_encoder(a2, str)
        EncoderB1.register_default_encoder(b1, str)

        assert JSONEncoderStar.default_typed_encoders() == default_typed_encoders
        assert EncoderA1.default_typed_encoders() == {**default_typed_encoders, str: a1, int: a1}
        assert EncoderA2.default_typed_encoders() == {**default_typed_encoders, str: a2, int: a1}
        assert EncoderB1.default_typed_encoders() == {**default_typed_encoders, str: b1}
