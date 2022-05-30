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

"""Ingestibles are your model and data, which can be turned into digestibles that explore/examine/explain/expose
your data and/or model."""

from typing import Dict, List, Optional

from instancelib import AbstractClassifier, Environment, InstanceProvider
from instancelib.typehints import KT

from .data import import_data, rename_labels, train_test_split
from .model import import_model


class Ingestible(dict):
    def __init__(
        self,
        data: Optional[Environment] = None,
        model: Optional[AbstractClassifier] = None,
        splits: Dict[KT, KT] = {
            "train": "train",
            "test": "test",
            "validation": "validation",
        },
    ):
        self["data"] = data
        self["model"] = model
        self.__splits = splits

    @property
    def data(self):
        return self["data"]

    def get_named_split(self, name: KT, validate: bool = False) -> Optional[InstanceProvider]:
        """Get split by name.

        Args:
            name (KT): Name of split.
            validate (bool, optional): Return None if no split is found or throw an error. Defaults to False.

        Raises:
            ValueError: Unknown split

        Returns:
            Optional[InstanceProvider]: Provider of split if it exists, else None.
        """
        if name in self.__splits.keys() and self.__splits[name] in self.data.keys():
            return self.data[self.__splits[name]]
        elif name in self.data.keys():
            return self.data[name]
        if validate:
            raise ValueError(f'Unknown split "{name}", choose from {self.splits}')
        return None

    @property
    def train(self):
        """Train data split."""
        return self.get_named_split("train")

    @property
    def test(self):
        """Test data split."""
        return self.get_named_split("test")

    @property
    def validation(self):
        """Validation data split."""
        return self.get_named_split("validation")

    @property
    def splits(self):
        """Names of splits."""
        return [k for k, v in self.__splits.items() if v in self.data._named_providers]

    @property
    def labels(self):
        """Labelprovider."""
        return self.data.labels

    @labels.setter
    def labels(self, labelprovider):
        self.data.labels = labelprovider

    @property
    def labelset(self):
        """Label names."""
        return list(self.labels.labelset) if self.labels else None

    @property
    def model(self):
        """Predictive model."""
        return self["model"]

    @model.setter
    def model(self, model):
        self["model"] = model

    def check_requirements(self, elements: List[str] = ["data", "model"]) -> bool:
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): Elements to check. Defaults to ['data', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.

        Returns:
            bool: True if all requirements are included.
        """
        for elem in elements:
            if elem not in self or getattr(self, elem) is None:
                raise ValueError(f'"{elem}" should be provided.')
        return True
