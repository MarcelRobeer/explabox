"""Functions/classes for sensitivity testing (fairness and robustness) for text data."""

from genbase import Readable
from text_sensitivity import (OneToManyPerturbation, OneToOnePerturbation,
                              compare_accuracy, compare_metric,
                              compare_precision, compare_recall,
                              input_space_robustness, invariance, mean_score,
                              perturbation)

from ...ingestibles import Ingestible
from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
perturbation = restyle(perturbation)


class Exposer(Readable, IngestiblesMixin):
    def __init__(self, data=None, model=None, ingestibles=None):
        if ingestibles is None:
            ingestibles = Ingestible(data=data, model=model)
        self.ingestibles = ingestibles
        self.check_requirements(['data', 'model'])
