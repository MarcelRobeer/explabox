"""..."""

from genbase import Readable

from explabox._version import __version__
from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.expose import Exposer
from explabox.ingestibles import from_sklearn, import_data, train_test_split
from explabox.mixins import IngestiblesMixin


class Explabox(Readable, IngestiblesMixin):
    def __init__(self, data, model, labelprovider, train=None, test=None, ingestibles=None):
        if ingestibles is not None:
            self.from_ingestibles(ingestibles, required=['data', 'model', 'labelprovider'])
        else:
            if self.data is None and train is not None or test is not None:
                self.data = {}
                if train is not None:
                    self.data['train'] = train
                if test is not None:
                    self.data['test'] = test
            elif self.data is not None:
                self.data = data
            else:
                raise ValueError('data, train or test should be provider for using explabox')
            self.model = model
            self.labelprovider = labelprovider

        self.examine = Examiner(ingestibles=self.ingestibles)
        self.explain = Explainer(ingestibles=self.ingestibles)
        self.explore = Explorer(ingestibles=self.ingestibles)
        self.expose = Exposer(ingestibles=self.ingestibles)
