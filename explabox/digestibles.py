"""Ingestibles are turned into digestibles, containing information to explore/examine/explain/expose your model."""

from genbase import MetaInfo
from genbase.utils import extract_metrics
from text_explainability.generation.return_types import Instances

from .ui.notebook import Render


class Performance(MetaInfo):
    def __init__(self, labels, metrics, type: str = "model_performance", subtype: str = "classification", **kwargs):
        """Digestible for performance metrics.

        Args:
            labels (_type_): _description_
            metrics (_type_): _description_
            type (str, optional): _description_. Defaults to "model_performance".
            subtype (str, optional): _description_. Defaults to "classification".
        """
        super().__init__(type=type, subtype=subtype, renderer=Render, **kwargs)
        self.labels = labels
        self._metrics, self._properties = extract_metrics(metrics)

    @property
    def metrics(self):
        """Metrics values."""
        return self._metrics

    @property
    def content(self):  # noqa: D102
        label_metrics = [{"label": label, "metrics": self.metrics[label]} for label in self.labels]
        return {
            "labels": self.labels,
            "label_metrics": label_metrics,
            "metrics": self._properties,
        }


class Descriptives(MetaInfo):
    def __init__(self, labels, label_counts, tokenized_lengths, type: str = "descriptives", **kwargs):
        """Digestible for descriptive statistics.

        Args:
            labels (_type_): _description_
            label_counts (_type_): _description_
            tokenized_lengths (_type_): _description_
            type (str, optional): _description_. Defaults to "descriptives".
        """
        super().__init__(type=type, renderer=Render, **kwargs)
        self.labels = labels
        self.label_counts = label_counts
        self.tokenized_lengths = tokenized_lengths

    @property
    def content(self):  # noqa: D102
        return {
            "labels": self.labels,
            "label_counts": self.label_counts,
            "tokenized_lengths": self.tokenized_lengths,
        }


class WronglyClassified(Instances):
    def __init__(self, instances, contingency_table, type: str = "wrongly_classified", **kwargs):
        """Digestible for wrongly classified instances

        Args:
            instances (_type_): _description_
            contingency_table (_type_): _description_
            type (str, optional): _description_. Defaults to "wrongly_classified".
        """
        super().__init__(instances=instances, type=type, subtype=None, renderer=Render, **kwargs)
        self.__contingency_table = contingency_table

    @property
    def wrongly_classified(self):
        """Wrongly classified instances, grouped by their ground-truth value, predicted value and instances."""
        return [
            {
                "ground_truth": g,
                "predicted": p,
                "instances": [self.instances.get(v_) for v_ in list(v)],
            }
            for (g, p), v in self.__contingency_table.items()
            if g != p
        ]

    @property
    def content(self):  # noqa: D102
        return {"wrongly_classified": self.wrongly_classified}


class Dataset(Instances):
    def __init__(self, *args, **kwargs):
        """Digestible for dataset."""
        pass
