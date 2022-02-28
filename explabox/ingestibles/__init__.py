"""..."""

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
        # TODO: convert a model, e.g. scikit-learn to instancelib
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

    def check_requirements(self, elements=['data', 'labelprovider', 'model']):
        for elem in elements:
            if elem not in self.ingestibles:
                raise ValueError(f'"{elem}" should be provided.')
