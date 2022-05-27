"""Tests for the `explabox.ui.notebook` module."""

import pytest

from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.ingestibles import Ingestible
from explabox.ui.notebook import GBRenderRestyled, Render, TERenderRestyled, TSRenderRestyled

INGESTIBLE = Ingestible(data=pytest.helpers.DATA(), model=pytest.helpers.MODEL())


Renderer = (GBRenderRestyled, TERenderRestyled, TSRenderRestyled, Render)


def test_explorer_descriptives_render():  # TODO: more checks
    """Test: ..."""
    descriptives = Explorer(ingestibles=INGESTIBLE).descriptives()
    renderer = descriptives._renderer(descriptives.to_config())
    assert isinstance(renderer, Renderer)
    html = renderer.as_html(**descriptives.renderargs)
    assert isinstance(html, str)


def test_examiner_performance_render():  # TODO: more checks
    """Test: ..."""
    performance = Examiner(ingestibles=INGESTIBLE).performance()
    renderer = performance._renderer(performance.to_config())
    assert isinstance(renderer, Renderer)
    html = renderer.as_html(**performance.renderargs)
    assert isinstance(html, str)


def test_examiner_wrongly_classified_render():  # TODO: more checks
    """Test: ..."""
    wrongly_classified = Examiner(ingestibles=INGESTIBLE).wrongly_classified()
    renderer = wrongly_classified._renderer(wrongly_classified.to_config())
    assert isinstance(renderer, Renderer)
    html = renderer.as_html(**wrongly_classified.renderargs)
    assert isinstance(html, str)


def test_explainer_explain_prediction_render():  # TODO: more checks
    """Test: ..."""
    explanation = Explainer(ingestibles=INGESTIBLE).explain_prediction("a")
    for v in explanation.return_values:
        renderer = v._renderer(v.to_config())
        assert isinstance(renderer, Renderer)
        html = renderer.as_html(**v.renderargs)
        assert isinstance(html, str)
