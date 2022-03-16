"""..."""

from typing import Optional, Union

from genbase import Readable, add_callargs
from instancelib import AbstractClassifier, Environment, MemoryLabelProvider
from instancelib.analysis.base import (contingency_table, get_keys,
                                       label_metrics)
from instancelib.labels.memory import MemoryLabelProvider

from ..digestibles import Performance, WronglyClassified
from ..ingestibles import Ingestible
from ..mixins import IngestiblesMixin, ModelMixin


class Examiner(Readable, ModelMixin, IngestiblesMixin):
    def __init__(
        self,
        data: Optional[Environment] = None,
        model: Optional[AbstractClassifier] = None,
        ingestibles: Optional[Ingestible] = None,
    ):
        if ingestibles is None:
            ingestibles = Ingestible(data=data, model=model)
        self.ingestibles = ingestibles
        self.check_requirements(["data", "model"])
        self.predictions = {}

    def __predict(self, split):
        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        named_split = self.ingestibles.get_named_split(split, validate=True)

        if split in self.predictions:
            return named_split, self.predictions[split]

        self.predictions[split] = MemoryLabelProvider.from_tuples(self.model.predict(named_split))
        return named_split, self.predictions[split]

    @add_callargs
    def wrongly_classified(self, split="test", **kwargs) -> WronglyClassified:
        """Give all wrongly classified samples.

        Args:
            split: Name of split.

        Returns:
            WronglyClassified: Wrongly classified examples in this  split.
        """
        callargs = kwargs.pop("__callargs__", None)

        named_split, predictions = self.__predict(split)
        ground_truth = MemoryLabelProvider.from_provider(self.labels, named_split)

        return WronglyClassified(
            named_split,
            contingency_table=contingency_table(ground_truth, predictions, named_split),
            callargs=callargs,
            **kwargs
        )

    @add_callargs
    def __call__(self, metrics=["f1", "accuracy", "precision", "recall"], split="test", **kwargs) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            metrics: ...
            split: ...
            **kwargs: ...
        """
        callargs = kwargs.pop("__callargs__", None)

        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        split, predictions = self.__predict(split)
        performance = {
            label: label_metrics(self.labels, predictions, get_keys(split), label) for label in self.labelset
        }

        return Performance(labels=self.labelset, metrics=performance, callargs=callargs, **kwargs)
