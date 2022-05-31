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

from typing import Dict, FrozenSet, Sequence, Tuple

from genbase import MetaInfo
from genbase.utils import extract_metrics
from instancelib.typehints import KT, LT
from text_explainability.generation.return_types import Instances

from .ui.notebook import Render


class Performance(MetaInfo):
    def __init__(
        self,
        labels: Sequence[LT],
        metrics: dict,
        type: str = "model_performance",
        subtype: str = "classification",
        **kwargs
    ):
        """Digestible for performance metrics.

        Args:
            labels (Sequence[LT]): Names of labels.
            metrics (dict): Performance metrics per label.
            type (str, optional): Type description. Defaults to "model_performance".
            subtype (str, optional): Subtype description. Defaults to "classification".
        """
        super().__init__(type=type, subtype=subtype, renderer=Render, **kwargs)
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
        **kwargs
    ):
        """Digestible for descriptive statistics.

        Args:
            labels (Sequence[LT]): Names of labels.
            label_counts (Dict[str, Dict[LT, int]]): Counts per label per split.
            tokenized_lengths (dict): Descriptive statistics for lengths of tokenized instances.
            type (str, optional): Type description. Defaults to "descriptives".
        """
        super().__init__(type=type, renderer=Render, **kwargs)
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
        **kwargs
    ):
        """Digestible for wrongly classified instances

        Args:
            instances (_type_): _description_
            contingency_table (Dict[Tuple[LT, LT], FrozenSet[KT]]): Classification contingency table as returned from
                `instancelib.analysis.base.contingency_table()`.
            type (str, optional): Type description. Defaults to "wrongly_classified".
        """
        super().__init__(instances=instances, type=type, subtype=None, renderer=Render, **kwargs)
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


class Dataset(Instances):
    def __init__(self, *args, **kwargs):
        """Digestible for dataset."""
        pass
