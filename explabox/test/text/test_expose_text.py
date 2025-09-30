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

"""Tests for the `explabox.expose.text` module."""

import string

import genbase_test_helpers
import pytest

from explabox.expose import Exposer
from explabox.expose.text import LabelMetrics, MeanScore, RandomString, SuccessTest
from explabox.ingestibles import Ingestible
from explabox.utils import MultipleReturn

INGESTIBLE = Ingestible(data=genbase_test_helpers.TEST_ENVIRONMENT, model=genbase_test_helpers.TEST_MODEL)

INPUT_SPACE_GENERATORS_VALID = [
    "ascii",
    "emojis",
    "whitespace",
    "spaces",
    "ascii_upper",
    "ascii_lower",
    "digits",
    "punctuation",
    "cyrillic",
    RandomString(string.printable),
]

COMPARE_METRIC_GENERATORS_VALID = [
    "lower",
    "upper",
    # "random_lower",
    # "random_upper",
    "add_typos",
    # "random_case_swap",
    "swap_random",
    "delete_random",
    "repeat",
]


def test_input_space_valid_return():  # TODO: add more checks
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.input_space("all", min_length=0, max_length=1)
    assert isinstance(test, SuccessTest)


@pytest.mark.parametrize("generator", INPUT_SPACE_GENERATORS_VALID)
def test_input_space_valid_generator(generator):
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.input_space(generator, min_length=0, max_length=1)
    assert isinstance(test, SuccessTest)


@pytest.mark.parametrize(
    "generator", genbase_test_helpers.corrupt([i for i in INPUT_SPACE_GENERATORS_VALID if isinstance(i, str)])
)
def test_input_space_invalid_generator(generator):
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    with pytest.raises(ValueError, match=r"Unknown generator .+$"):
        _ = exposer.input_space(generator, min_length=0, max_length=1)


@pytest.mark.parametrize("generators", genbase_test_helpers.random_combinations(INPUT_SPACE_GENERATORS_VALID))
def test_input_space_valid_generators(generators):
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.input_space(generators, min_length=0, max_length=1)
    assert isinstance(test, SuccessTest)


def test_invariance_valid_return():  # TODO: add more checks
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.invariance("{characters}", expectation="punctuation", characters=list("'!#$%&()*+,-./:;<=~aA'"))
    assert isinstance(test, SuccessTest)


@pytest.mark.parametrize("generator", COMPARE_METRIC_GENERATORS_VALID)
def test_compare_metric_valid_return(generator):  # TODO: add more checks
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.compare_metric(generator, splits="test")
    assert isinstance(test, LabelMetrics)


@pytest.mark.parametrize("generator", genbase_test_helpers.corrupt(COMPARE_METRIC_GENERATORS_VALID))
def test_compare_metric_invalid_generator(generator):
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    with pytest.raises(ValueError, match=r"Unknown perturbation .+$"):
        _ = exposer.compare_metric(generator, splits="test")


@pytest.mark.parametrize("label", ["punctuation", "no_punctuation", "all"])
def test_mean_score_valid_return(label):  # TODO: add more checks
    """Test: ..."""
    exposer = Exposer(ingestibles=INGESTIBLE)
    test = exposer.mean_score(pattern="{a|b|c}", selected_labels=label)
    if label == "all":
        assert isinstance(test, MultipleReturn)
    else:
        assert isinstance(test, MeanScore)


# TODO: invariance, mean_score, compare_metric
