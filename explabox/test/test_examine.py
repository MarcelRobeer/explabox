import copy

import genbase_test_helpers
import pytest

from explabox.digestibles import Performance, WronglyClassified
from explabox.examine import Examiner
from explabox.ingestibles import Ingestible

DATA, MODEL = genbase_test_helpers.TEST_ENVIRONMENT, genbase_test_helpers.TEST_MODEL
INGESTIBLE = Ingestible(data=DATA, model=MODEL)


def test_requirements():
    """Test: If all ingestibles are None, should throw a ValueError."""
    with pytest.raises(ValueError):
        Examiner(data=None, model=None, ingestibles=None)


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_empty(data, model):
    """Test: If ingestibles arguments are None (precedence over data/model argument), should throw ValueError."""
    with pytest.raises(ValueError):
        Examiner(data=data, model=model, ingestibles=Ingestible(data=None, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_data(data, model):
    """Test: If only the ingestibles argument for data is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Examiner(data=data, model=model, ingestibles=Ingestible(data=DATA, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_model(data, model):
    """Test: If only the ingestibles argument for model is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Examiner(data=data, model=model, ingestibles=Ingestible(data=None, model=MODEL))


def test_valid_constructor_args():
    """Test: Correct construction when data and model are provided as arguments."""
    assert isinstance(Examiner(data=DATA, model=MODEL), Examiner)


def test_valid_constructor_ingestible():
    """Test: Correct construction when data and model are provided as ingestible."""
    assert isinstance(Examiner(data=None, model=None, ingestibles=Ingestible(data=DATA, model=MODEL)), Examiner)


def test_valid_constructor_both():
    """Test: Correct construction when data and model are provided as ingestible and as arguments."""
    assert isinstance(Examiner(data=DATA, model=MODEL, ingestibles=Ingestible(data=DATA, model=MODEL)), Examiner)


def test_prediction_cache():
    """Test: ..."""
    examiner = Examiner(ingestibles=INGESTIBLE)
    _ = examiner.performance(split="test")
    preds = copy.deepcopy(examiner.predictions["test"])
    _ = examiner.performance(split="test")
    assert preds == examiner.predictions["test"]


def test_call_valid_return():  # TODO: split
    """Test: ..."""
    examiner = Examiner(ingestibles=INGESTIBLE)
    performance = examiner.__call__()
    assert isinstance(performance, Performance)
    assert performance.type == "model_performance"
    assert performance.subtype == "classification"
    assert isinstance(performance.content, dict)
    assert "labels" in performance.content
    assert "label_metrics" in performance.content
    assert "metrics" in performance.content


def test_performance_valid_return():  # TODO: split
    """Test: ..."""
    examiner = Examiner(ingestibles=INGESTIBLE)
    performance = examiner.performance()
    assert isinstance(performance, Performance)
    assert performance.type == "model_performance"
    assert performance.subtype == "classification"
    assert isinstance(performance.content, dict)
    assert "labels" in performance.content
    assert "label_metrics" in performance.content
    assert "metrics" in performance.content


def test_wrongly_classified_valid_return():  # TODO: split
    """Test: ..."""
    examiner = Examiner(ingestibles=INGESTIBLE)
    wrongly_classified = examiner.wrongly_classified()
    assert isinstance(wrongly_classified, WronglyClassified)
    assert wrongly_classified.type == "wrongly_classified"
    assert isinstance(wrongly_classified.content, dict)
    assert "wrongly_classified" in wrongly_classified.content
