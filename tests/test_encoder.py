from unittest.mock import Mock

import pytest

from jsonstar.encoder import JSONEncoderStar


class CustomType:
    """
    CustomType to test our implementation of the default method.
    Types supported by the standard JSONEncoder are encoded before our code run.
    """


class JSONEncoderTest(JSONEncoderStar):
    pass


@pytest.fixture
def encoder():
    return JSONEncoderTest()


@pytest.fixture(autouse=True)
def empty_encoder_class(monkeypatch):
    monkeypatch.setattr(JSONEncoderTest, "_default_functional_encoders", [])
    monkeypatch.setattr(JSONEncoderTest, "_default_typed_encoders", {})


class TestTypedEncoders:
    def test_default_typed_encoders_are_used_when_nothing_else_is_registered(self, encoder):
        encoder.__class__._default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}

        assert encoder.encode(CustomType()) == '"CustomType default encoder"'

    def test_typed_encoders_have_precedence_over_default_type_encoders(self, encoder):
        encoder.__class__._default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}
        encoder.register(lambda o: "CustomType encoder", CustomType)

        assert encoder.encode(CustomType()) == '"CustomType encoder"'

    def test_typed_encoders_have_precedence_over_functional_encoders(self, encoder):
        encoder.__class__._default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}
        encoder.register(lambda o: "CustomType encoder", CustomType)
        encoder.register(lambda o: "Functional encoder")

        assert encoder.encode(CustomType()) == '"CustomType encoder"'

    def test_absence_of_typed_encoder_leads_to_functional_encoder_being_used(self, encoder):
        encoder.register(lambda o: "Functional encoder")

        assert encoder.encode(CustomType()) == '"Functional encoder"'

    def test_inherited_types_are_supported_by_base_type_encoder(self, encoder):
        class InheritedType(CustomType):
            pass

        encoder.register(lambda o: "CustomType encoder", CustomType)

        assert encoder.encode(InheritedType()) == '"CustomType encoder"'

    def test_encoder_for_inherited_type_has_precedence_over_encoder_for_base_type(self, encoder):
        class Mother(CustomType):
            pass

        class Father(CustomType):
            pass

        class Child(Mother, Father):
            pass

        encoder.register(lambda o: "CustomType encoder", CustomType)
        encoder.register(lambda o: "Father encoder", Father)
        encoder.register(lambda o: "Child encoder", Child)

        assert encoder.encode(CustomType()) == '"CustomType encoder"'
        assert encoder.encode(Mother()) == '"CustomType encoder"'
        assert encoder.encode(Father()) == '"Father encoder"'
        assert encoder.encode(Child()) == '"Child encoder"'


class TestFunctionalEncoders:
    def test_default_functional_encoders_are_used_when_nothing_else_is_registered(self, encoder):
        encoder.__class__._default_functional_encoders = [lambda o: "default functional encoder"]

        assert encoder.encode(CustomType()) == '"default functional encoder"'

    def test_functional_encoders_have_precedence_over_default_functional_encoders(self, encoder):
        encoder.__class__._default_functional_encoders = [lambda o: "default functional encoder"]
        encoder.register(lambda o: "functional encoder")

        assert encoder.encode(CustomType()) == '"functional encoder"'

    def test_absence_of_encoders_leads_to_super_error(self, encoder):
        with pytest.raises(TypeError):
            encoder.encode(CustomType())


class TestRegistrationOfEncoders:
    def test_registration_of_typed_encoder(self, encoder):
        encoder.register(lambda o: "CustomType encoder", CustomType)
        encoder.register(failing_functional_encoder := Mock(side_effect=Exception))

        assert encoder.encode(CustomType()) == '"CustomType encoder"'
        assert not failing_functional_encoder.called

    def test_registration_of_functional_encoder(self, encoder):
        encoder.register(failing_functional_encoder := Mock(side_effect=Exception))
        encoder.register(lambda o: "Functional encoder")

        assert encoder.encode(CustomType()) == '"Functional encoder"'
        assert failing_functional_encoder.called

    def test_override_typed_encoder(self, encoder):
        encoder.register(lambda o: "CustomType encoder", CustomType)
        encoder.register(lambda o: "CustomType encoder override", CustomType)

        assert encoder.encode(CustomType()) == '"CustomType encoder override"'


class TestRegistrationOnInit:
    def test_registration_of_typed_encoder_on_init(self):
        encoder = JSONEncoderTest(typed_encoders={CustomType: lambda o: "CustomType encoder"})

        assert encoder.encode(CustomType()) == '"CustomType encoder"'

    def test_registration_of_functional_encoder_on_init(self):
        encoder = JSONEncoderTest(functional_encoders=[lambda o: "Functional encoder"])

        assert encoder.encode(CustomType()) == '"Functional encoder"'

    def test_override_typed_encoder_on_init(self):
        encoder = JSONEncoderTest(typed_encoders={CustomType: lambda o: "CustomType encoder"})
        encoder.register(lambda o: "CustomType encoder override", CustomType)

        assert encoder.encode(CustomType()) == '"CustomType encoder override"'
