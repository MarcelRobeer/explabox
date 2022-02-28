"""..."""

from genbase import Readable, add_callargs
from instancelib.analysis.base import get_keys, label_metrics
from instancelib.labels.memory import MemoryLabelProvider

from ..digestibles import Performance
from ..mixins import ModelMixin


class Examiner(Readable, ModelMixin):
    def __init__(self, model, data, labelprovider, ingestibles=None):
        if ingestibles is not None:
            self.from_ingestibles(ingestibles, required=["data", "model", "labelprovider"])
        else:
            self.data = data
            self.model = model
            self.labelprovider = labelprovider

    def wrongly_classified(self):
        """Give all wrongly classified samples."""
        raise NotImplementedError()

    @add_callargs
    def __call__(self, metrics=["f1", "accuracy", "precision", "recall"], **kwargs) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            metrics: ...
            **kwargs: ...
        """
        callargs = kwargs.pop("__callargs__", None)

        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        keys = get_keys(self.data["test"])
        predictions = self.model.predict(self.data["test"])
        self.predictions = MemoryLabelProvider.from_tuples(predictions)
        performance = {label: label_metrics(self.labelprovider, self.predictions, keys, label) for label in self.labels}

        return Performance(labels=self.labels, metrics=performance, callargs=callargs, **kwargs)
