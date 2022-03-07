"""Ingestibles are turned into digestibles, containing information to explore/examine/explain/expose your model."""

from genbase import MetaInfo
from genbase.utils import extract_metrics, recursive_to_dict

from .ui.notebook import Render


class Performance(MetaInfo):
    def __init__(self, labels, metrics, type: str = "model_performance", subtype: str = "classification", **kwargs):
        """..."""
        super().__init__(type=type, subtype=subtype, renderer=Render, **kwargs)
        self.labels = labels
        self._metrics, self._properties = extract_metrics(metrics)

    @property
    def metrics(self):
        return self._metrics

    @property
    def content(self):
        label_metrics = [{"label": label, "metrics": self.metrics[label]} for label in self.labels]
        return {"labels": self.labels, "label_metrics": label_metrics, "metrics": self._properties}


class Descriptives(MetaInfo):
    def __init__(self, labels, label_counts, tokenized_lengths, type: str = "descriptives", **kwargs):
        """..."""
        super().__init__(type=type, renderer=Render, **kwargs)
        self.labels = labels
        self.label_counts = label_counts
        self.tokenized_lengths = tokenized_lengths

    @property
    def content(self):
        return {
            "labels": self.labels,
            "label_counts": self.label_counts,
            "tokenized_lengths": self.tokenized_lengths,
        }
