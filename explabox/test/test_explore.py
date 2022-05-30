# Copyright (C) 2021-2022 National Police Lab AI (NPAI).
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

import genbase_test_helpers
import pytest

from explabox.digestibles import Descriptives
from explabox.explore import Explorer
from explabox.ingestibles import Ingestible

DATA, MODEL = genbase_test_helpers.TEST_ENVIRONMENT, genbase_test_helpers.TEST_MODEL
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
