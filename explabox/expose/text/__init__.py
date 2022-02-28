"""Functions/classes for sensitivity testing (fairness and robustness) for text data."""

from genbase import Readable
from text_sensitivity import (OneToManyPerturbation, OneToOnePerturbation,
                              compare_accuracy, compare_metric,
                              compare_precision, compare_recall,
                              input_space_robustness, invariance, mean_score,
                              perturbation)

from explabox.mixins import IngestiblesMixin

from ...ui.notebook import restyle

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
perturbation = restyle(perturbation)


class Exposer(Readable, IngestiblesMixin):
    def __init__(self, data, model, ingestibles=None):
        if ingestibles is not None:
            self.from_ingestibles(ingestibles, required=["data", "model"])
        else:
            self.data = data
            self.model = model
