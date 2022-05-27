import genbase_test_helpers
import pytest

from explabox import Examiner, Explabox, Explainer, Explorer, Exposer
from explabox.ingestibles import Ingestible

DATA, MODEL = genbase_test_helpers.TEST_ENVIRONMENT, genbase_test_helpers.TEST_MODEL
INGESTIBLE = Ingestible(data=DATA, model=MODEL)


def test_requirements():
    """Test: If all ingestibles are None, should throw a ValueError."""
    with pytest.raises(ValueError):
        Explabox(data=None, model=None, ingestibles=None)


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_empty(data, model):
    """Test: If ingestibles arguments are None (precedence over data/model argument), should throw ValueError."""
    with pytest.raises(ValueError):
        Explabox(data=data, model=model, ingestibles=Ingestible(data=None, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_data(data, model):
    """Test: If only the ingestibles argument for data is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Explabox(data=data, model=model, ingestibles=Ingestible(data=DATA, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_model(data, model):
    """Test: If only the ingestibles argument for model is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Explabox(data=data, model=model, ingestibles=Ingestible(data=None, model=MODEL))


def test_valid_constructor_args():
    """Test: Correct construction when data and model are provided as arguments."""
    assert isinstance(Explabox(data=DATA, model=MODEL), Explabox)


def test_valid_constructor_ingestible():
    """Test: Correct construction when data and model are provided as ingestible."""
    assert isinstance(Explabox(data=None, model=None, ingestibles=Ingestible(data=DATA, model=MODEL)), Explabox)


def test_valid_constructor_both():
    """Test: Correct construction when data and model are provided as ingestible and as arguments."""
    assert isinstance(Explabox(data=DATA, model=MODEL, ingestibles=Ingestible(data=DATA, model=MODEL)), Explabox)


def test_valid_types():
    """Test: Each of the four subparts of the Explabox is the correct class."""
    box = Explabox(ingestibles=INGESTIBLE)
    assert isinstance(box.examine, Examiner)
    assert isinstance(box.explain, Explainer)
    assert isinstance(box.explore, Explorer)
    assert isinstance(box.expose, Exposer)
