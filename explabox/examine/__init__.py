"""..."""

from genbase import Readable, add_callargs
from instancelib.analysis.base import get_keys, label_metrics
from instancelib.labels.memory import MemoryLabelProvider

from ..digestibles import Performance
from ..ingestibles import Ingestible
from ..mixins import IngestiblesMixin, ModelMixin


class Examiner(Readable, ModelMixin, IngestiblesMixin):
    def __init__(self, data=None, model=None, ingestibles=None):
        if ingestibles is None:
            ingestibles = Ingestible(data=data, model=model)
        self.ingestibles = ingestibles
        self.check_requirements(['data', 'model'])

    def __validate_split(self, split):
        if split not in self.splits:
            raise ValueError(f'Unknown split "{split}", choose from {self.splits}.')

    @add_callargs
    def wrongly_classified(self, split="test", **kwargs):
        """Give all wrongly classified samples."""
        callargs = kwargs.pop("__callargs__", None)

        self.__validate_split(split)
        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        raise NotImplementedError()

    @add_callargs
    def __call__(self,
                 metrics=["f1", "accuracy", "precision", "recall"],
                 split="test",
                 **kwargs) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            metrics: ...
            split: ...
            **kwargs: ...
        """
        callargs = kwargs.pop("__callargs__", None)

        self.__validate_split(split)
        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        keys = get_keys(self.data[split])
        predictions = self.model.predict(self.data[split])
        self.predictions = MemoryLabelProvider.from_tuples(predictions)
        performance = {label: label_metrics(self.labelprovider, self.predictions, keys, label) for label in self.labels}

        return Performance(labels=self.labels, metrics=performance, callargs=callargs, **kwargs)
