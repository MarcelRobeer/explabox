"""..."""

from genbase import Readable

from explabox._version import __version__
from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.expose import Exposer
from explabox.ingestibles import Ingestible, from_sklearn, import_data, train_test_split
from explabox.mixins import IngestiblesMixin


class Explabox(Readable, IngestiblesMixin):
    def __init__(self,
                 ingestibles=None,
                 **kwargs):
        if ingestibles is None:
            ingestibles = Ingestible(**kwargs)
        self.ingestibles = ingestibles
        self.check_requirements(['data', 'labelprovider', 'model'])

        self.examine = Examiner(ingestibles=self.ingestibles)
        self.explain = Explainer(ingestibles=self.ingestibles)
        self.explore = Explorer(ingestibles=self.ingestibles)
        self.expose = Exposer(ingestibles=self.ingestibles)
