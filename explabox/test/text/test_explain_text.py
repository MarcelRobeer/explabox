"""Tests for the `explabox.explain.text` module."""

import pytest

from explabox.explain import Explainer
from explabox.explain.text import FeatureList, Instances
from explabox.ingestibles import Ingestible
from explabox.utils import MultipleReturn

INGESTIBLE = Ingestible(data=pytest.helpers.DATA(), model=pytest.helpers.MODEL())

EXPLAIN_PREDICTION_METHODS_VALID = [
    "lime",
    "shap",
    "shapley",
    "kernel_shap",
    "local_tree",
    "tree",
    "local_rules",
    "rules",
]

EXPLAIN_PREDICTION_CONTRASTIVE_METHODS_VALID = [
    "local_rules",
    "rules",
    "foil",
    "foil_tree",
    "contrastive",
    "contrastive_explanation",
]


def test_explain_prediction_valid_return():  # TODO: add more checks
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.explain_prediction("a")
    assert isinstance(explanation, MultipleReturn)


def test_explain_prediction_index_valid():  # TODO: add more checks
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.explain_prediction(0)
    assert isinstance(explanation, MultipleReturn)


def test_explain_prediction_index_invalid():
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    with pytest.raises(Exception, match=r"Unknown instance identifier .+$"):
        _ = explainer.explain_prediction(-1)


@pytest.mark.parametrize("method", EXPLAIN_PREDICTION_METHODS_VALID)
def test_explain_prediction_valid_generator(method):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.explain_prediction("a", methods=method)
    assert isinstance(explanation, MultipleReturn)
    assert len(explanation) == 1
    # assert isinstance(explanation.to_config(), dict)


@pytest.mark.parametrize("method", [pytest.helpers.corrupt(EXPLAIN_PREDICTION_METHODS_VALID)])
def test_explain_prediction_invalid_generator(method):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    with pytest.warns(UserWarning, match=r"Unknown method .+$"):
        with pytest.raises(Exception):
            _ = explainer.explain_prediction("a", methods=method)


@pytest.mark.parametrize("methods", pytest.helpers.random_combinations(EXPLAIN_PREDICTION_METHODS_VALID))
def test_explain_prediction_valid_generators(methods):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.explain_prediction("a", methods=methods)
    assert isinstance(explanation, MultipleReturn)
    assert len(explanation) == len(methods)
    assert isinstance(explanation._repr_html_(), str)
    # assert isinstance(explanation.to_config(), list)


@pytest.mark.parametrize("method", EXPLAIN_PREDICTION_CONTRASTIVE_METHODS_VALID)
@pytest.mark.parametrize("foil_fn", [0, 1, "punctuation", "no_punctuation"])
def test_explain_prediction_contrastive_valid_generator(method, foil_fn):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.explain_prediction("a", methods=method, foil_fn=foil_fn)
    assert isinstance(explanation, MultipleReturn)
    assert len(explanation) == 1


@pytest.mark.parametrize("method", EXPLAIN_PREDICTION_CONTRASTIVE_METHODS_VALID)
def test_explain_prediction_contrastive_no_foil_fn(method):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    err = (
        pytest.raises(ValueError)
        if method in ["foil", "foil_tree", "contrastive", "contrastive_explanation"]
        else pytest.warns(UserWarning)
    )
    with err:
        _ = explainer.explain_prediction("a", methods=method)


@pytest.mark.parametrize("labelwise", [True, False])
def test_token_frequency_valid_return(labelwise):  # TODO: add more checks
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.token_frequency(splits="test", labelwise=labelwise)
    assert isinstance(explanation, FeatureList)


def test_token_information_valid_return():  # TODO: add more checks
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.token_information(splits="test")
    assert isinstance(explanation, FeatureList)


@pytest.mark.parametrize("method", ["mmdcritic", "kmedoids"])
@pytest.mark.parametrize("n", range(1, 11))
def test_prototypes_valid_return(method, n):  # TODO: add more checks, split
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.prototypes(method=method, n=n)
    assert isinstance(explanation, Instances)
    assert isinstance(explanation.content, dict)
    assert "prototypes" in explanation.content
    assert len(explanation.content["prototypes"]) == n


@pytest.mark.parametrize("method", pytest.helpers.corrupt(["mmdcritic", "kmedoids"]))
@pytest.mark.parametrize("n", range(1, 6))
def test_prototypes_invalid_method(method, n):
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    with pytest.raises(ValueError, match=r"Unknown method .+$"):
        _ = explainer.prototypes(method=method, n=n)


@pytest.mark.parametrize("method", ["mmdcritic", "kmedoids"])
@pytest.mark.parametrize("n", range(1, 4))
def test_prototypes_labelwise_valid_return(method, n):  # TODO: add more checks, split
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.prototypes(method=method, n=n, labelwise=True)
    assert isinstance(explanation, Instances)
    assert isinstance(explanation.content, dict)
    assert "prototypes" in explanation.content
    assert set(explanation.content["prototypes"].keys()) == set(explainer.ingestibles.labelset)
    assert all(len(label) == n for label in explanation.content["prototypes"].values())


@pytest.mark.parametrize("n_prototypes", range(1, 6))
@pytest.mark.parametrize("n_criticisms", range(1, 6))
def test_prototypes_criticisms_valid_return(n_prototypes, n_criticisms):  # TODO: add more checks, split
    """Test: ..."""
    explainer = Explainer(ingestibles=INGESTIBLE)
    explanation = explainer.prototypes_criticisms(n_prototypes=n_prototypes, n_criticisms=n_criticisms)
    assert isinstance(explanation, Instances)
    assert isinstance(explanation.content, dict)
    assert "prototypes" in explanation.content
    assert len(explanation.content["prototypes"]) == n_prototypes
    assert "criticisms" in explanation.content
    assert len(explanation.content["criticisms"]) == n_criticisms


# TODO: labelwise
