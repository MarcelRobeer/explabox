"""Calculate quantitative metrics on how the model performs, and examine where the model went wrong."""

from typing import Optional

from genbase import Readable, add_callargs
from instancelib import AbstractClassifier, Environment, MemoryLabelProvider
from instancelib.analysis.base import contingency_table, get_keys, label_metrics
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
        **kwargs,
    ):
        """The Examiner calculates quantitative metrics on how the model performs.

        The Examine requires 'data' and 'model' defined. It is included in the Explabox under the `.examine` property.

        Examples:
            Construct the examiner:

            >>> from explabox.examine import Examiner
            >>> examiner = Explainer(data=data, model=model)

            Calculate model performance metrics on the validation set:

            >>> examiner(split='validation')

            See all wrongly classified examples in the test set:

            >>> examiner.wrongly_classified(split='test')

        Args:
            data (Optional[Environment], optional): Data for ingestibles. Defaults to None.
            model (Optional[AbstractClassifier], optional): Model for ingestibles. Defaults to None.
            ingestibles (Optional[Ingestible], optional): Ingestible. Defaults to None.
        """
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

        self.predictions[split] = MemoryLabelProvider.from_tuples(
            self.model.predict(named_split)
        )
        return named_split, self.predictions[split]

    @add_callargs
    def wrongly_classified(self, split: str = "test", **kwargs) -> WronglyClassified:
        """Give all wrongly classified samples.

        Args:
            split (str, optional): Name of split. Defaults to 'test'.

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
            **kwargs,
        )

    @add_callargs
    def performance(self, split: str = "test", **kwargs) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            split (str, optional): Split to calculate metrics on. Defaults to 'test'.

        Returns:
            Performance: Performance metrics of your model on the split.
        """
        callargs = kwargs.pop("__callargs__", None)

        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        split, predictions = self.__predict(split)
        performance = {
            label: label_metrics(self.labels, predictions, get_keys(split), label)
            for label in self.labelset
        }

        return Performance(
            labels=self.labelset, metrics=performance, callargs=callargs, **kwargs
        )

    def __call__(self, split: str = "test", **kwargs) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            split (str, optional): Split to calculate metrics on. Defaults to 'test'.

        Returns:
            Performance: Performance metrics of your model on the split.
        """
        return self.performance(split=split, **kwargs)
