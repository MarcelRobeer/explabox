"""Ingestibles are your model and data, which can be turned into digestibles that explore/examine/explain/expose
your data and/or model."""

from pathlib import Path
from typing import List

from .data import import_data, train_test_split
from .model import from_sklearn


class Ingestible(dict):
    def __init__(self,
                 environment=None,
                 labelprovider=None,
                 model=None,
                 data=None,
                 train=None,
                 test=None,
                 validation=None):
        self.ingestibles = {}
        # TODO: convert data and labels, e.g. csv files to instancelib environment
        if environment is not None and labelprovider is None:
            labelprovider = environment.labels
        if environment is not None and data is None:
            data = environment.instances
        self.__init_data__(data, train, test, validation)
        self.__init_labelprovider__(labelprovider)
        self.__init_model__(model)

    def __init_data__(self, data, train, test, validation):
        if not (data or train or test):
            raise ValueError('At least one of "data", "train", "test" or "validation" should be provided!')
        if data is None:
            data = {}
            for k, v in zip(['train', 'test', 'validation'], [train, test, validation]):
                if v is not None:
                    data[k] = v
        self.ingestibles['data'] = data

    def __init_labelprovider__(self, labelprovider):
        self.ingestibles['labelprovider'] = labelprovider

    def __init_model__(self, model):
        if isinstance(model, str):
            model = Path(model)
            if not model.is_file():
                raise FileNotFoundError(f'Unknown file "{model}')
            file_type = str.lower(model.suffix)
            model = str(model.absolute())
            if file_type == '.pkl':
                import pickle
                model = pickle.loads(model)
            elif file_type == '.onnx':
                import ilonnx
                model = ilonnx.build_data_model(model, classes=[])
            else:
                raise ValueError(f'Unknown file format for "{model}"')

        # TODO: convert a trained model, e.g. scikit-learn or filepath to instancelib

        self.ingestibles['model'] = model

    @property
    def data(self):
        return self.ingestibles['data']

    @property
    def train(self):
        return self.ingestibles.data['train'] if (self.ingestibles.data and 'train' in self.ingestibles.data) else None

    @property
    def test(self):
        return self.ingestibles.data['test'] if (self.ingestibles.data and 'test' in self.ingestibles.data) else None

    @property
    def validation(self):
        return self.ingestibles.data['validation'] if (self.ingestibles.data and 'validation' in self.ingestibles.data)\
            else None

    @property
    def splits(self):
        return list(self.ingestibles.data.keys()) if self.ingestibles.data else None

    @property
    def labelprovider(self):
        return self.ingestibles['labelprovider']

    @labelprovider.setter
    def labelprovider(self, labelprovider):
        self.ingestibles['labelprovider'] = labelprovider

    @property
    def labels(self):
        return list(self.labelprovider.labelset) if self.labelprovider else None

    @property
    def model(self):
        return self.ingestibles['model']

    @model.setter
    def model(self, model):
        self.ingestibles['model'] = model

    def check_requirements(self, elements: List[str] = ['data', 'labelprovider', 'model']):
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): _description_. Defaults to ['data', 'labelprovider', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.
        """
        for elem in elements:
            if elem not in self.ingestibles:
                raise ValueError(f'"{elem}" should be provided.')
