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
        splits: Dict[KT, KT] = {"train": "train", "test": "test", "validation": "validation"},
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
            raise ValueError('Unknown split "{name}", choose from {self.splits}')
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

    def check_requirements(self, elements: List[str] = ["data", "model"]):
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): Elements to check. Defaults to ['data', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.
        """
        for elem in elements:
            if elem not in self:
                raise ValueError(f'"{elem}" should be provided.')
