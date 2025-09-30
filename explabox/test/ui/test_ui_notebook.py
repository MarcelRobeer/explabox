# Copyright (c) 2022 Marcel Robeer for National Police Lab AI (NPAI).
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License (LGPL) as published by the Free Software Foundation; either version 3 (LGPLv3) of the License, or (at
# your option) any later version. You may not use this file except in compliance with the license. You may obtain a copy
# of the license at:
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

"""Tests for the `explabox.ui.notebook` module."""

import genbase_test_helpers

from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.ingestibles import Ingestible
from explabox.ui.notebook import GBRenderRestyled, Render, TERenderRestyled, TSRenderRestyled

INGESTIBLE = Ingestible(data=genbase_test_helpers.TEST_ENVIRONMENT, model=genbase_test_helpers.TEST_MODEL)


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
