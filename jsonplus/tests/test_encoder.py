from unittest.mock import Mock

import pytest

from jsonplus.encoder import JSONEncoderPlus


class CustomType:
    """
    CustomType to test our implementation of the default method.
    Types supported by the standard JSONEncoder are encoded before our code run.
    """


class JSONEncoderTest(JSONEncoderPlus):
    default_typed_encoders = {}
    default_functional_encoders = []


@pytest.fixture
def encoder():
    return JSONEncoderTest()


class TestTypedEncoders:
    def test_default_typed_encoders_are_used_when_nothing_else_is_registered(self, encoder):
        encoder.default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}

        assert encoder.encode(CustomType()) == '"CustomType default encoder"'

    def test_typed_encoders_have_precedence_over_default_type_encoders(self, encoder):
        encoder.default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}
        encoder.register(lambda o: "CustomType encoder", CustomType)

        assert encoder.encode(CustomType()) == '"CustomType encoder"'

    def test_typed_encoders_have_precedence_over_functional_encoders(self, encoder):
        encoder.default_typed_encoders = {CustomType: lambda o: "CustomType default encoder"}
        encoder.register(lambda o: "CustomType encoder", CustomType)
        encoder.register(lambda o: "Functional encoder")

        assert encoder.encode(CustomType()) == '"CustomType encoder"'

    def test_absence_of_typed_encoder_leads_to_functional_encoder_being_used(self, encoder):
        encoder.register(lambda o: "Functional encoder")

        assert encoder.encode(CustomType()) == '"Functional encoder"'


class TestFunctionalEncoders:
    def test_default_functional_encoders_are_used_when_nothing_else_is_registered(self, encoder):
        encoder.default_functional_encoders = [lambda o: "default functional encoder"]

        assert encoder.encode(CustomType()) == '"default functional encoder"'

    def test_functional_encoders_have_precedence_over_default_functional_encoders(self, encoder):
        encoder.default_functional_encoders = [lambda o: "default functional encoder"]
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
