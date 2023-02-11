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

"""Ingestibles are turned into digestibles, containing information to explore/examine/explain/expose your model."""

from collections.abc import Sequence as SequenceType
from typing import Callable, Dict, FrozenSet, Optional, Sequence, Tuple, Union

from genbase import MetaInfo
from genbase.utils import extract_metrics
from instancelib.typehints import DT, KT, LT
from text_explainability.generation.return_types import Instances

from ..ui.notebook import Render


class Performance(MetaInfo):
    def __init__(
        self,
        labels: Sequence[LT],
        metrics: dict,
        type: str = "model_performance",
        subtype: Optional[str] = "classification",
        callargs: Optional[dict] = None,
        **kwargs,
    ):
        """Digestible for performance metrics.

        Args:
            labels (Sequence[LT]): Names of labels.
            metrics (dict): Performance metrics per label.
            type (str, optional): Type description. Defaults to "model_performance".
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            callargs (Optional[dict], optional): Call arguments for reproducibility. Defaults to None.
        """
        super().__init__(type=type, subtype=subtype, callargs=callargs, renderer=Render, **kwargs)
        self.labels = labels
        self._metrics, self._properties = extract_metrics(metrics)

    @property
    def metrics(self):
        """Metrics values."""
        return self._metrics

    @property
    def content(self):
        """Content as dictionary."""
        label_metrics = [{"label": label, "metrics": self.metrics[label]} for label in self.labels]
        return {
            "labels": self.labels,
            "label_metrics": label_metrics,
            "metrics": self._properties,
        }


class Descriptives(MetaInfo):
    def __init__(
        self,
        labels: Sequence[LT],
        label_counts: Dict[str, Dict[LT, int]],
        tokenized_lengths: dict,
        type: str = "descriptives",
        callargs: Optional[dict] = None,
        **kwargs,
    ):
        """Digestible for descriptive statistics.

        Args:
            labels (Sequence[LT]): Names of labels.
            label_counts (Dict[str, Dict[LT, int]]): Counts per label per split.
            tokenized_lengths (dict): Descriptive statistics for lengths of tokenized instances.
            type (str, optional): Type description. Defaults to "descriptives".
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            callargs (Optional[dict], optional): Call arguments for reproducibility. Defaults to None.
        """
        super().__init__(type=type, subtype=None, callargs=callargs, renderer=Render, **kwargs)
        self.labels = labels
        self.label_counts = label_counts
        self.tokenized_lengths = tokenized_lengths

    @property
    def content(self):
        """Content as dictionary."""
        return {
            "labels": self.labels,
            "label_counts": self.label_counts,
            "tokenized_lengths": self.tokenized_lengths,
        }


class WronglyClassified(Instances):
    def __init__(
        self,
        instances,
        contingency_table: Dict[Tuple[LT, LT], FrozenSet[KT]],
        type: str = "wrongly_classified",
        callargs: Optional[dict] = None,
        **kwargs,
    ):
        """Digestible for wrongly classified instances

        Args:
            instances (_type_): Instances.
            contingency_table (Dict[Tuple[LT, LT], FrozenSet[KT]]): Classification contingency table as returned from
                `instancelib.analysis.base.contingency_table()`.
            type (str, optional): Type description. Defaults to "wrongly_classified".
            callargs (Optional[dict], optional): Call arguments for reproducibility. Defaults to None.
        """
        super().__init__(instances=instances, type=type, subtype=None, callargs=callargs, renderer=Render, **kwargs)
        self.__contingency_table = contingency_table

    @property
    def wrongly_classified(self):
        """Wrongly classified instances, grouped by their ground-truth value, predicted value and instances."""
        return [
            {
                "ground_truth": g,
                "predicted": p,
                "instances": [self.instances.get(v_) for v_ in list(v)],
            }
            for (g, p), v in self.__contingency_table.items()
            if g != p
        ]

    @property
    def content(self):
        """Content as dictionary."""
        return {"wrongly_classified": self.wrongly_classified}


class Dataset(MetaInfo):
    def __init__(
        self,
        instances,
        labels: Sequence[LT],
        type: str = "dataset",
        subtype: Optional[str] = None,
        callargs: Optional[dict] = None,
        **kwargs,
    ):
        """Digestible for dataset.

        Examples:
            Construct a dataset with 5 instances and get instance 2 through 4:

            >>> dataset = Dataset(instances, ['positive', 'negative', 'positive', 'neutral', 'positive'])
            >>> dataset[2:4]

            Get the first instance:

            >>> dataset.head(n=1)

            Randomly sample two instances:

            >>> dataset.sample(n=2, seed=0)

            Get all instances in the dataset labelled as 'positive':

            >>> dataset.filter('positive')

        Args:
            instances (_type_): Instances.
            labels (Sequence[LT]): Ground-truth labels (annotated).
            type (str, optional): Type description. Defaults to "dataset".
            subtype (Optional[str], optional): Subtype description. Defaults to None.
            callargs (Optional[dict], optional): Call arguments for reproducibility. Defaults to None.
        """
        super().__init__(type=type, subtype=subtype, callargs=callargs, renderer=Render, **kwargs)
        self._instances = instances
        self._labels = [label if isinstance(label, frozenset) else frozenset({[label]}) for label in labels]

    @property
    def instances(self):
        """Get instances property"""
        return self._instances

    @property
    def data(self):
        """Get data property."""
        return (
            list(self._instances.all_data())
            if hasattr(self._instances, "all_data")
            else [instance.data for instance in self._instances]
        )

    @property
    def keys(self):
        """Get keys property"""
        return list(self._instances) if hasattr(self._instances, "keys") else list(range(len(self._instances)))

    @property
    def labels(self):
        """Get labels property."""
        return list(self._labels)

    @property
    def content(self):
        """Content as dictionary."""
        return {"instances": self.instances, "labels": self.labels}

    def __len__(self):
        return len(self._instances)

    def __iter__(self):
        return zip(self.data, self.labels)

    def __getitem__(self, index) -> "Dataset":
        """Get item(s) by index. If index are in keys it uses the key, else the integer indices."""
        if isinstance(index, (int, str)):
            index = [index]
        elif isinstance(index, slice):
            index = range(len(self.keys))[index]

        return self.get_by_key(index) if all(i in self.keys for i in index) else self.get_by_index(index)

    def get_by_index(self, index) -> "Dataset":
        """Get item(s) by integer index."""
        if isinstance(index, (int, str)):
            index = [index]
        instances = [self._instances[self.keys[i]] for i in index]
        labels = [self.labels[i] for i in index]
        return Dataset(instances=instances, labels=labels, type=self.type, subtype=self.subtype)

    def get_by_key(self, index) -> "Dataset":
        """Get item(s) by key."""
        if isinstance(index, (int, str)):
            index = [index]
        instances = [self._instances[i] for i in index]
        labels = [self.labels[self.keys.index(i)] for i in index]
        return Dataset(instances=instances, labels=labels, type=self.type, subtype=self.subtype)

    def head(self, n: int = 10) -> "Dataset":
        """Get the first n elements in the dataset.

        Args:
            n (int, optional): Number of elements >= 0. Defaults to 10.

        Raises:
            ValueError: n should be >= 0.

        Returns:
            Dataset: First n elements.
        """
        if n < 0:
            raise ValueError(f"{n=} should be >= 0!")
        return self if n >= len(self) else self.get_by_index(range(0, n))

    def tail(self, n: int = 10) -> "Dataset":
        """Get the last n elements in the dataset.

        Args:
            n (int, optional): Number of elements >= 0. Defaults to 10.

        Raises:
            ValueError: n should be >= 0.

        Returns:
            Dataset: Last n elements.
        """
        if n < 0:
            raise ValueError(f"{n=} should be >= 0!")
        if n == 0:
            return self.head(n=0)
        return self if n >= len(self) else self.get_by_index(range(len(self))[slice(-n, None)])

    def sample(self, n: int = 1, seed: Optional[int] = None) -> "Dataset":
        """Get a random sample of size n.

        Args:
            n (int, optional): Number of elements >= 0. Defaults to 1.
            seed (int, optional): Seed for reproducibility; if None it takes a random seed. Defaults to None.

        Raises:
            ValueError: n should be >= 0.

        Returns:
            Dataset: Random subsample.
        """
        if n < 0:
            raise ValueError(f"{n=} should be >= 0!")
        if n >= len(self):
            return self

        import random

        random.seed(seed)

        return self.get_by_index(random.sample(list(self._instances), n))

    def filter(self, indexer: Union[Callable[[dict], bool], Callable[[DT, LT], bool], Sequence[bool], LT]) -> "Dataset":
        """Filter dataset by label, filter function or boolean list/array.

        Examples:
            Filter by label 'positive':

            >>> dataset.filter('positive')

            Filter if '@' character in data:

            >>> dataset.filter(lambda data, label: '@' in data)

            Filter if '@' character not in instance and label in ('neutral', 'negative'):

            >>> def filter_fn(instance):
            ...     return '@' not in instance['data'] and instance['label'] in (frozenset({'neutral'}), frozenset({'negative'}))
            >>> dataset.filter(filter_fn)

            Filter by boolean sequence (should be equal length to the number of instances):

            >>> dataset.filter([True] * len(dataset))

        Args:
            indexer (Union[Callable[[dict], bool], Callable[[DT, LT], bool], Sequence[bool], LT]): Filter to apply.

        Raises:
            ValueError: Boolean array should be equal length to number of instances.

        Returns:
            Dataset: Filtered dataset.
        """

        def _boolfilter(bool_sequence):
            return self.get_by_index([i for i, s in enumerate(bool_sequence) if s])

        if isinstance(indexer, (frozenset, str, int)):
            if not isinstance(indexer, frozenset):
                indexer = frozenset([indexer])
            return self.filter(lambda _, label: label == indexer)
        elif isinstance(indexer, SequenceType):
            indexer = [i for i in indexer]
            if len(indexer) != len(self):
                raise ValueError("Boolean array should be equal length to the number of instances")
            return self if all(indexer) else _boolfilter(indexer)
        elif isinstance(indexer, Callable):
            from inspect import signature

            indexer_len = len(signature(indexer).parameters)
            if indexer_len == 1:
                return _boolfilter(indexer({"data": data, "label": label}) for data, label in iter(self))
            elif indexer_len == 2:
                return _boolfilter(indexer(data, label) for data, label in iter(self))
        raise ValueError(f"Unknown type of indexer {type(indexer)}")
