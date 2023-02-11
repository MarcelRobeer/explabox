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

from explabox.digestibles import Dataset, Descriptives
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
    """Test: Valid contents of `digestibles.Descriptives` after `explorer.__call__()`."""
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
    """Test: Valid contents of `digestibles.Descriptives` after `explorer.descriptives()`."""
    explorer = Explorer(ingestibles=INGESTIBLE)
    descriptives = explorer.descriptives()
    assert isinstance(descriptives, Descriptives)
    assert descriptives.type == "descriptives"
    assert descriptives.labels is not None
    assert descriptives.label_counts is not None
    assert isinstance(descriptives.content, dict)
    assert "labels" in descriptives.content
    assert "label_counts" in descriptives.content


def test_instances_valid_return():
    """Test: Valid contents of `digestibles.Dataset`."""
    explorer = Explorer(data=DATA, model=MODEL)
    dataset = explorer.instances()
    assert isinstance(dataset, Dataset)
    assert dataset.type == "dataset"
    assert isinstance(dataset.content, dict)
    assert "instances" in dataset.content
    assert "labels" in dataset.content


def test_instances_length():
    """Test: Dataset length should be the same as the provided dataset length."""
    ingestible = INGESTIBLE
    explorer = Explorer(ingestibles=ingestible)
    dataset = explorer.instances()
    assert len(dataset) == len(ingestible.data.dataset)
    assert len(list(iter(dataset))) == len(ingestible.data.dataset)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 20])
def test_instances_select(n):
    """Test: Selected sample should be of length n for every access method."""
    ingestible = INGESTIBLE
    explorer = Explorer(ingestibles=ingestible)
    dataset = explorer.instances()
    assert len(dataset.head(n=n)) == n
    assert len(dataset.tail(n=n)) == n
    assert len(dataset.get_by_index(range(n))) == n
    assert len(dataset.get_by_index(n)) == 1
    assert len(dataset[slice(None, n)]) == n
    assert len(dataset[slice(n, 2 * n)]) == n
    assert len(dataset[n]) == 1
    assert len(dataset.get_by_key(list(ingestible.data.dataset.keys())[n])) == 1


@pytest.mark.parametrize("n", range(1, 5))
def test_instances_max_select(n):
    """Test: Selected sample should cap out at length of dataset."""
    ingestible = INGESTIBLE
    explorer = Explorer(ingestibles=ingestible)
    dataset = explorer.instances()
    N = n * len(dataset)
    assert len(dataset.head(n=N)) == len(dataset)
    assert len(dataset.tail(n=N)) == len(dataset)
    assert len(dataset.sample(n=N)) == len(dataset)
    with pytest.raises(IndexError):
        dataset.get_by_index(N)
    with pytest.raises(IndexError):
        dataset[N]


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 20])
@pytest.mark.parametrize("seed", [0, 42, 99])
def test_instances_sample(n, seed):
    """Test: Sample should be of length n regardless of random seed."""
    explorer = Explorer(ingestibles=INGESTIBLE)
    dataset = explorer.instances()
    assert len(dataset.sample(n=n, seed=seed)) == n


@pytest.mark.parametrize("n", [-1, -2, -3, -99])
def test_instances_args_n(n):
    """Test: Negative n should raise ValueError."""
    explorer = Explorer(ingestibles=INGESTIBLE)
    dataset = explorer.instances()
    with pytest.raises(ValueError):
        dataset.head(n=n)
    with pytest.raises(ValueError):
        dataset.tail(n=n)
    with pytest.raises(ValueError):
        dataset.sample(n=n)


@pytest.mark.parametrize(
    "label", ["punctuation", frozenset({"punctuation"}), "no_punctuation", frozenset({"no_punctuation"})]
)
def test_instances_filter_label(label):
    """Test: Different ways on filtering by label should only select label."""
    to_check = label if isinstance(label, frozenset) else frozenset({label})
    explorer = Explorer(ingestibles=INGESTIBLE)
    dataset = explorer.instances()
    assert all(label == to_check for label in dataset.filter(label).labels)
    assert all(label == to_check for label in dataset.filter(lambda instance: instance["label"] == to_check).labels)
    assert all(label == to_check for label in dataset.filter(lambda data, label: label == to_check).labels)
    assert all(label == to_check for label in dataset.filter([l == to_check for l in dataset.labels]).labels)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 20])
def test_instances_filter_args_len(n):
    """Test: Wrong length boolean sequence should raise ValueError."""
    with pytest.raises(ValueError):
        explorer = Explorer(ingestibles=INGESTIBLE)
        explorer.instances().filter([True] * n)


def test_instances_filter_args_type():
    """Test: Wrong filter input type should raise ValueError."""
    with pytest.raises(ValueError):
        explorer = Explorer(ingestibles=INGESTIBLE)
        explorer.instances().filter(None)
