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

"""Tests for the `explabox.expose` module."""

import genbase_test_helpers
import pytest

from explabox.expose import Exposer
from explabox.ingestibles import Ingestible

DATA, MODEL = genbase_test_helpers.TEST_ENVIRONMENT, genbase_test_helpers.TEST_MODEL


def test_requirements():
    """Test: If all ingestibles are None, should throw a ValueError."""
    with pytest.raises(ValueError):
        Exposer(data=None, model=None, ingestibles=None)


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_empty(data, model):
    """Test: If ingestibles arguments are None (precedence over data/model argument), should throw ValueError."""
    with pytest.raises(ValueError):
        Exposer(data=data, model=model, ingestibles=Ingestible(data=None, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_data(data, model):
    """Test: If only the ingestibles argument for data is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Exposer(data=data, model=model, ingestibles=Ingestible(data=DATA, model=None))


@pytest.mark.parametrize("data", [DATA, None])
@pytest.mark.parametrize("model", [MODEL, None])
def test_requirements_ingestible_model(data, model):
    """Test: If only the ingestibles argument for model is given, should throw ValueError."""
    with pytest.raises(ValueError):
        Exposer(data=data, model=model, ingestibles=Ingestible(data=None, model=MODEL))


def test_valid_constructor_args():
    """Test: Correct construction when data and model are provided as arguments."""
    assert isinstance(Exposer(data=DATA, model=MODEL), Exposer)


def test_valid_constructor_ingestible():
    """Test: Correct construction when data and model are provided as ingestible."""
    assert isinstance(Exposer(data=None, model=None, ingestibles=Ingestible(data=DATA, model=MODEL)), Exposer)


def test_valid_constructor_both():
    """Test: Correct construction when data and model are provided as ingestible and as arguments."""
    assert isinstance(Exposer(data=DATA, model=MODEL, ingestibles=Ingestible(data=DATA, model=MODEL)), Exposer)
