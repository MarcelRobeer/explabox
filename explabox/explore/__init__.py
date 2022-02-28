"""..."""

import numpy as np
from genbase import Readable, add_callargs

from ..digestibles import Descriptives
from ..mixins import IngestiblesMixin


class Explorer(Readable, IngestiblesMixin):
    def __init__(self, data, ingestibles=None):
        if ingestibles is not None:
            self.from_ingestibles(ingestibles, required=["data"])
        else:
            self.data = data

    @add_callargs
    def __call__(self, **kwargs) -> Descriptives:
        """Describe features such as the amount per label for the train, test and model predictions
        and text data specific features such as the maximum/minimum/mean amount of words in a sample and
        the standard deviation.

        Args:
            **kwargs: ...

        Returns:
            ...
        """
        callargs = kwargs.pop("__callargs__", None)

        label_counts = {
            split_name: {
                label: len(self.labelprovider.get_instances_by_label(label).intersection(split))
                for label in self.labels
            }
            for split_name, split in self.data
        }

        from text_explainability import default_tokenizer

        tokenized_lengths = {}
        for split_name, split in self.data:
            token_lengths = np.array([len(default_tokenizer(instance.data)) for _, instance in iter(split.items())])
            tokenized_lengths[split_name] = {
                "mean": np.mean(token_lengths),
                "max": np.max(token_lengths),
                "min": np.min(token_lengths),
                "std": np.std(token_lengths),
            }
        return Descriptives(
            labels=self.labels,
            label_counts=label_counts,
            tokenized_lengths=tokenized_lengths,
            callargs=callargs,
            **kwargs,
        )
