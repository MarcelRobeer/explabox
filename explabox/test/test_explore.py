import pytest

from explabox.digestibles import Dataset, Descriptives
from explabox.explore import Explorer
from explabox.ingestibles import Ingestible

DATA, MODEL = pytest.helpers.DATA(), pytest.helpers.MODEL()
INGESTIBLE = Ingestible(data=DATA, model=MODEL)


def test_requirements():
    """Test: If all ingestibles are None, should throw a ValueError."""
    with pytest.raises(ValueError):
        Explorer(data=None, model=None, ingestibles=None)


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_empty(data, model):
    """Test: If ingestibles arguments are None (precedence over data/model argument), should throw ValueError."""
    with pytest.raises(ValueError):
        Explorer(data=data, model=model, ingestibles=Ingestible(data=None, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_model(data, model):
    """Test: If only the ingestibles argument for model is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Explorer(data=data, model=model, ingestibles=Ingestible(data=None, model=MODEL))


@pytest.mark.parametrize("model", [MODEL, None])
def test_valid_ingestible_data(model):
    """Test: Correct construction if only data is provided as argument."""
    assert isinstance(Explorer(data=DATA, model=model, ingestibles=None), Explorer)


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_valid_args_data(data, model):
    """Test: Correct construction if only data is provided as ingestible."""
    assert isinstance(Explorer(data=data, model=model, ingestibles=Ingestible(data=DATA, model=None)), Explorer)


def test_valid_constructor_args():
    """Test: Correct construction when data and model are provided as arguments."""
    assert isinstance(Explorer(data=DATA, model=MODEL), Explorer)


def test_valid_constructor_ingestible():
    """Test: Correct construction when data and model are provided as ingestible."""
    assert isinstance(Explorer(data=None, model=None, ingestibles=Ingestible(data=DATA, model=MODEL)), Explorer)


def test_valid_constructor_both():
    """Test: Correct construction when data and model are provided as ingestible and as arguments."""
    assert isinstance(Explorer(data=DATA, model=MODEL, ingestibles=Ingestible(data=DATA, model=MODEL)), Explorer)


def test_call_valid_return():  # TODO: split
    """Test: ..."""
    explorer = Explorer(ingestibles=INGESTIBLE)
    descriptives = explorer.__call__()
    assert isinstance(descriptives, Descriptives)
    assert descriptives.type == "descriptives"
    assert descriptives.labels is not None
    assert descriptives.label_counts is not None
    assert isinstance(descriptives.content, dict)
    assert "labels" in descriptives.content
    assert "label_counts" in descriptives.content


def test_descriptives_valid_return():  # TODO: split
    """Test: ..."""
    explorer = Explorer(ingestibles=INGESTIBLE)
    descriptives = explorer.descriptives()
    assert isinstance(descriptives, Descriptives)
    assert descriptives.type == "descriptives"
    assert descriptives.labels is not None
    assert descriptives.label_counts is not None
    assert isinstance(descriptives.content, dict)
    assert "labels" in descriptives.content
    assert "label_counts" in descriptives.content


# def test_instances_valid_return():
#     """Test: ..."""
#     explorer = Explorer(data=DATA, model=MODEL)
#     assert isinstance(explorer.descriptives(), Dataset)
