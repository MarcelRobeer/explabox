"""Add explainability to your text model/dataset."""

import warnings
from typing import List, Optional, Union

import numpy as np
from genbase import Readable, add_callargs
from instancelib.analysis.base import get_keys, label_metrics
from instancelib.labels.memory import MemoryLabelProvider

from ...return_types import Descriptives, Performance
from ...ui.notebook import restyle
from ...utils import MultipleReturn


class Explainer(Readable):
    def __init__(self, model, train, test, labelprovider):
        """Single object to create explanations corresponding to a model and dataset (with ground-truth labels).

        Args:
            model: ...
            train: ...
            test: ...
            labelprovider: ...
        """
        self.model = model
        self.train = train
        self.test = test
        self.labelprovider = labelprovider
        self._performance = self.__performance()

    @property
    def is_classifier(self):
        return "classifier" in str(self.model.__class__).lower()

    @property
    def labels(self):
        return list(self.labelprovider.labelset)

    @property
    def splits(self):
        return list(zip(["train", "test"], [self.train, self.test]))

    def __performance(self) -> dict:
        """Determine TPs, FPs, TNs and FNs for each item in the test set for each label."""
        if not self.is_classifier:
            raise NotImplementedError("Only supported for classifiers")

        keys = get_keys(self.test)
        predictions = self.model.predict(self.test)
        self.predictions = MemoryLabelProvider.from_tuples(predictions)
        performance = {
            label: label_metrics(self.labelprovider, self.predictions, keys, label)
            for label in self.labels
        }
        return performance

    @add_callargs
    def model_performance(
        self, metrics=["f1", "accuracy", "precision", "recall"], **kwargs
    ) -> Performance:
        """Determine performance metrics, the amount of predictions for each label in the test set
        and the values for the confusion matrix for each label in the test set.

        Args:
            metrics: ...
            **kwargs: ...
        """
        callargs = kwargs.pop("__callargs__", None)
        return Performance(
            labels=self.labels, metrics=self._performance, callargs=callargs, **kwargs
        )

    @add_callargs
    def descriptives(self, **kwargs) -> Descriptives:
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
                label: len(
                    self.labelprovider.get_instances_by_label(label).intersection(split)
                )
                for label in self.labels
            }
            for split_name, split in self.splits
        }

        from text_explainability import default_tokenizer

        tokenized_lengths = {}
        for split_name, split in self.splits:
            token_lengths = np.array(
                [
                    len(default_tokenizer(instance.data))
                    for _, instance in iter(split.items())
                ]
            )
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

    @restyle
    def explain_prediction(
        self, sample: Union[int, str], *args, methods: List[str] = ["lime"], **kwargs
    ) -> Optional[MultipleReturn]:
        """Explain specific sample locally.

        Args:
            sample: Identifier of sample in dataset (int) or input (str).
            methods: List of methods to get explanations from. Choose from 'lime', 'shap', 'tree', 'rules', 'foil_tree'.
            *args: Positional arguments passed to local explanation technique.
            **kwargs: Keyword arguments passed to local explanation technique.

        Returns:
            ...
        """
        if isinstance(methods, str):
            methods = [methods]
        if isinstance(sample, int):
            if sample in self.train:
                sample = self.train[sample]
            elif sample in self.test:
                sample = self.test[sample]
            else:
                raise Exception(f"Unknown instance identifier {sample}.")
        elif isinstance(sample, str):
            from text_explainability import from_string

            sample = from_string(sample)

        if "labels" not in kwargs:
            kwargs["labels"] = self.labels

        res = []
        for method in [str.lower(m) for m in methods]:
            cls = None
            if method in ["lime"]:
                from text_explainability.local_explanation import LIME

                cls = LIME
            elif method in ["shap", "shapley", "kernelshap", "kernel_shap"]:
                from text_explainability.local_explanation import KernelSHAP

                cls = KernelSHAP
            elif method in ["localtree", "tree"]:
                from text_explainability.local_explanation import LocalTree

                cls = LocalTree
            elif method in ["localrules", "rules"]:
                from text_explainability.local_explanation import LocalRules

                cls = LocalRules
            elif method in [
                "foil",
                "foiltree",
                "foil_tree",
                "contrastive",
                "contrastive_explanation",
            ]:
                from text_explainability.local_explanation import FoilTree

                cls = FoilTree
            if cls is not None:
                res.append(
                    cls(env=None, labelset=self.labels)(sample, self.model, **kwargs)
                )
            else:
                warnings.warn(f'Unknown method "{method}". Skipping to next one')
        return MultipleReturn(*res) if res else None

    def wrongly_classified(self):
        """Give all wrongly classified samples."""
        raise NotImplementedError()

    def token_frequency(
        self,
        splits: List[str] = ["train", "test"],
        labelwise: bool = True,
        k: int = 10,
        include_ground_truth: bool = True,
        include_model_predictions: bool = True,
    ):
        """Calculate the most frequent tokens for the train and test set for each label.

        Args:
            ...

        Returns:
            ...
        """
        raise NotImplementedError()

    def token_information(self, *args, **kwargs):
        """...

        Args:
            ...

        Returns:
            ...
        """
        raise NotImplementedError()
