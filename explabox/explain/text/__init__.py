"""Add explainability to your text model/dataset."""

import warnings
from typing import List, Optional, Union

from genbase import Readable

from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle
from ...utils import MultipleReturn


class Explainer(Readable, IngestiblesMixin):
    def __init__(self, data, model, labelprovider, ingestibles=None):
        """Single object to create explanations corresponding to a model and dataset (with ground-truth labels).

        Args:
            model: ...
            labelprovider: ...
        """
        if ingestibles is not None:
            self.from_ingestibles(ingestibles, required=["data", "model", "labelprovider"])
        else:
            self.data = data
            self.model = model
            self.labelprovider = labelprovider

    @property
    def labels(self):
        return list(self.labelprovider.labelset)

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
                res.append(cls(env=None, labelset=self.labels)(sample, self.model, **kwargs))
            else:
                warnings.warn(f'Unknown method "{method}". Skipping to next one')
        return MultipleReturn(*res) if res else None

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
