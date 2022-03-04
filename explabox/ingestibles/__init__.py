"""Ingestibles are your model and data, which can be turned into digestibles that explore/examine/explain/expose
your data and/or model."""

from typing import Dict, List, Optional

from instancelib import InstanceProvider, MemoryEnvironment
from instancelib.typehints import KT
from sklearn.exceptions import NotFittedError

from .data import import_data, train_test_split
from .model import import_model


class Ingestible(dict):
    def __init__(self,
                 data=None,
                 model=None,
                 splits: Dict[KT, KT] = {'train': 'train', 'test': 'test', 'validation': 'validation'}):
        self['data'] = data
        self['model'] = model
        self.__splits = splits

    @property
    def environment(self):
        if hasattr(self, '_environment'):
            return self._environment
        return MemoryEnvironment(self.data, self.labelprovider)

    @property
    def data(self):
        return self['data']

    def get_named_split(self, name: KT) -> Optional[InstanceProvider]:
        if name in self.__splits.keys() and self.__splits[name] in self.data.keys():
            return self.data[self.__splits[name]]
        elif name in self.data.keys():
            return self.data[name]
        return None

    @property
    def train(self):
        return self.get_named_split('train')

    @property
    def test(self):
        return self.get_named_split('test')

    @property
    def validation(self):
        return self.get_named_split('validation')

    @property
    def splits(self):
        return [k for k, v in self.__splits.items() if v in self.data._named_providers]

    @property
    def labels(self):
        return self.data.labels

    @labels.setter
    def labels(self, labelprovider):
        self.data.labels = labelprovider

    @property
    def labelset(self):
        return list(self.labels.labelset) if self.labels else None

    @property
    def model(self):
        return self['model']

    @model.setter
    def model(self, model):
        self['model'] = model

    def check_requirements(self, elements: List[str] = ['data', 'model']):
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): Elements to check. Defaults to ['data', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.
        """
        for elem in elements:
            if elem not in self:
                raise ValueError(f'"{elem}" should be provided.')
