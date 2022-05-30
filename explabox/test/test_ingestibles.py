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
