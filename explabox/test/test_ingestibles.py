import genbase_test_helpers
import pytest

from explabox.ingestibles import Ingestible

DATA, MODEL = genbase_test_helpers.TEST_ENVIRONMENT, genbase_test_helpers.TEST_MODEL


@pytest.mark.parametrize("model", [None, MODEL])
def test_same_data(model):
    """Test: ..."""
    data = DATA
    assert Ingestible(data=data, model=model).data == data


@pytest.mark.parametrize("data", [None, DATA])
def test_same_model(data):
    """Test: ..."""
    model = MODEL
    assert Ingestible(data=data, model=model).model == model


def test_split_train():
    """Test: ..."""
    ingestible = Ingestible(data=DATA, model=MODEL)
    assert ingestible.train == ingestible.get_named_split("train")


def test_split_test():
    """Test: ..."""
    ingestible = Ingestible(data=DATA, model=MODEL)
    assert ingestible.test == ingestible.get_named_split("test")


def test_split_validation():
    """Test: ..."""
    ingestible = Ingestible(data=DATA, model=MODEL)
    assert ingestible.validation == ingestible.get_named_split("validation")
