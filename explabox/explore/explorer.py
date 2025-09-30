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

"""Main Explorer class."""

from typing import Optional

import numpy as np
from genbase import Readable, add_callargs
from instancelib import Environment

from ..digestibles import Dataset, Descriptives
from ..ingestibles import Ingestible
from ..mixins import IngestiblesMixin


class Explorer(Readable, IngestiblesMixin):
    def __init__(self, data: Optional[Environment] = None, ingestibles: Optional[Ingestible] = None, **kwargs):
        """The Explorer explores your data by providing descriptive statistics.

        The Explorer requires 'data' defined. It is included in the Explabox under the `.explore` property.

        Examples:
            Get dataset descriptives:

            >>> from explabox.explore import Explorer
            >>> explorer = Explorer(data=data)
            >>> explorer()

            Show the first 10 instances of the test split

            >>> from explabox.explore import Explorer
            >>> explorer = Explorer(data=data)
            >>> explorer.instances(split="test")[:10]

        Args:
            data (Optional[Environment], optional): Data for ingestibles. Defaults to None.
            ingestibles (Optional[Ingestible], optional): Ingestible. Defaults to None.
        """
        if ingestibles is None:
            ingestibles = Ingestible(data=data)
        self.ingestibles = ingestibles
        self.check_requirements(["data"])

    @add_callargs
    def instances(self, split: str = "test", **kwargs) -> Dataset:
        """Get the instances of the given split.

        Args:
            split (str, optional): Split to select. Defaults to "test".

        Returns:
            Dataset: Instances in the split.
        """
        callargs = kwargs.pop("__callargs__", None)

        instances = self.ingestibles.get_named_split(split, validate=True)
        labels = [self.ingestibles.labels[key] for key in instances]
        labelset = self.ingestibles.labelset

        return Dataset(
            instances=instances,
            labels=labels,
            labelset=labelset,
            callargs=callargs,
            **kwargs,
        )

    @add_callargs
    def descriptives(self, **kwargs) -> Descriptives:
        """Describe features such as the amount per label for the train, test and model predictions
        and text data specific features such as the maximum/minimum/mean amount of words in a sample and
        the standard deviation.

        Returns:
            Descriptives: Descriptive statistics of each split.
        """
        callargs = kwargs.pop("__callargs__", None)

        label_counts = {
            split_name: {
                label: len(self.labels.get_instances_by_label(label).intersection(split)) for label in self.labelset
            }
            for split_name, split in self.data.items()
        }

        from text_explainability import default_tokenizer

        # TODO: move to text-specific version of descriptives
        tokenized_lengths = {}
        for split_name, split in self.data.items():
            token_lengths = np.array([len(default_tokenizer(instance.data)) for _, instance in iter(split.items())])
            tokenized_lengths[split_name] = {
                "mean": np.mean(token_lengths),
                "max": np.max(token_lengths),
                "min": np.min(token_lengths),
                "std": np.std(token_lengths),
            }
        return Descriptives(
            labels=self.labelset,
            label_counts=label_counts,
            tokenized_lengths=tokenized_lengths,
            callargs=callargs,
            **kwargs,
        )

    def __call__(self, **kwargs) -> Descriptives:
        """Describe features such as the amount per label for the train, test and model predictions
        and text data specific features such as the maximum/minimum/mean amount of words in a sample and
        the standard deviation.

        Returns:
            Descriptives: Descriptive statistics of each split.
        """
        return self.descriptives(**kwargs)
