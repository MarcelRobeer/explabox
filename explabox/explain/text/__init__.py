"""Add explainability to your text model/dataset."""

import warnings
from typing import List, Optional, Union

from genbase import Readable, translate_list
from instancelib import AbstractClassifier, Environment
from text_explainability.data.embedding import Embedder, SentenceTransformer
from text_explainability.generation.return_types import FeatureList, Instances

from ...ingestibles import Ingestible
from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle
from ...utils import MultipleReturn


class Explainer(Readable, IngestiblesMixin):
    def __init__(
        self,
        data: Optional[Environment] = None,
        model: Optional[AbstractClassifier] = None,
        ingestibles: Optional[Ingestible] = None,
    ):
        """Create explanations corresponding to a model and dataset (with ground-truth labels)."""
        if ingestibles is None:
            ingestibles = Ingestible(data=data, model=model)
        self.ingestibles = ingestibles
        self.check_requirements(["data", "model"])

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
            Optional[MultipleReturn]: ...
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
            kwargs["labels"] = self.labelset

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
                res.append(cls(env=None, labelset=self.labelset)(sample, self.model, **kwargs))
            else:
                warnings.warn(f'Unknown method "{method}". Skipping to next one')
        return MultipleReturn(*res) if res else None

    def __return_explanations(self, explanations):
        return MultipleReturn(*explanations) if len(explanations) > 1 else explanations[0]

    @restyle
    def token_frequency(
        self,
        splits: Union[str, List[str]] = "test",
        explain_model: bool = True,
        labelwise: bool = True,
        k: int = 25,
        filter_words: List[str] = translate_list("stopwords"),
        lower: bool = True,
        seed: int = 0,
        **count_vectorizer_kwargs,
    ) -> Union[FeatureList, MultipleReturn]:
        """Show the top-k number of tokens for each ground-truth or predicted label.

        Args:
            splits (Union[str, List[str]], optional): Split names to get the explanation for. Defaults to 'test'.
            explain_model (bool, optional): Whether to explain the model (True) or ground-truth labels (False).
                Defaults to True.
            labelwise (bool, optional): Whether to summarize the counts for each label seperately. Defaults to True.
            k (Optional[int], optional): Limit to the top-k words per label, or all words if None. Defaults to 25.
            filter_words (List[str], optional): Words to filter out from top-k. Defaults to ['de', 'het', 'een'].
            lower (bool, optional): Whether to make all tokens lowercase. Defaults to True.
            seed (int, optional). Seed for reproducibility. Defaults to 0.
            **count_vectorizer_kwargs: Optional arguments passed to `CountVectorizer`/`FastCountVectorizer`.

        Returns:
            Union[FeatureList, MultipleReturn]: Each label with corresponding top words and their frequency
        """
        from text_explainability import TokenFrequency

        if isinstance(splits, str):
            splits = [splits]

        explanations = [
            TokenFrequency(self.ingestibles.get_named_split(split, validate=True), seed=seed)(
                model=self.model,
                labelprovider=self.labels,
                explain_model=explain_model,
                labelwise=labelwise,
                k=k,
                lower=lower,
                filter_words=filter_words,
                **count_vectorizer_kwargs,
            )
            for split in splits
        ]

        return self.__return_explanations(explanations)

    @restyle
    def token_information(
        self,
        splits: Union[str, List[str]] = "test",
        explain_model: bool = True,
        k: Optional[int] = 25,
        filter_words: List[str] = translate_list("stopwords"),
        lower: bool = True,
        seed: int = 0,
        **count_vectorizer_kwargs,
    ) -> Union[FeatureList, MultipleReturn]:
        """Show the top-k token mutual information for a dataset or model.

        Args:
            splits (Union[str, List[str]], optional): Split names to get the explanation for. Defaults to 'test'.
            explain_model (bool, optional): Whether to explain the model (True) or ground-truth labels (False).
                Defaults to True.
            labelwise (bool, optional): Whether to summarize the counts for each label seperately. Defaults to True.
            k (Optional[int], optional): Limit to the top-k words per label, or all words if None. Defaults to 25.
            filter_words (List[str], optional): Words to filter out from top-k. Defaults to ['de', 'het', 'een'].
            lower (bool, optional): Whether to make all tokens lowercase. Defaults to True.
            seed (int, optional). Seed for reproducibility. Defaults to 0.
            **count_vectorizer_kwargs: Optional arguments passed to `CountVectorizer`/`FastCountVectorizer`.

        Returns:
            Union[FeatureList, MultipleReturn]: k labels, sorted based on their mutual information with
                the output (predictive model labels or ground-truth labels)
        """
        from text_explainability import TokenInformation

        if isinstance(splits, str):
            splits = [splits]

        explanations = [
            TokenInformation(self.ingestibles.get_named_split(split, validate=True), seed=seed)(
                model=self.model,
                labelprovider=self.labels,
                explain_model=explain_model,
                k=k,
                filter_words=filter_words,
                lower=lower,
                **count_vectorizer_kwargs,
            )
            for split in splits
        ]

        return self.__return_explanations(explanations)

    @restyle
    def prototypes(
        self,
        method: Union[str, List[str]] = "mmdcritic",
        n: int = 5,
        splits: Union[str, List[str]] = "test",
        embedder: Optional[Embedder] = SentenceTransformer,
        labelwise: bool = False,
        seed: int = 0,
    ) -> Union[Instances, MultipleReturn]:
        """Select n prototypes (representative samples) for the given split(s).

        Args:
            method (str, optional): Method(s) to apply. Choose from ['mmdcritic', 'kmedoids']. Defaults to 'mmdcritic'.
            n (int, optional): Number of prototypes to generate. Defaults to 5.
            splits (Union[str, List[str]], optional): Name(s) of split(s). Defaults to "test".
            embedder (Optional[Embedder], optional): Embedder used. Defaults to SentenceTransformer.
            labelwise (bool, optional): Select for each label. Defaults to False.
            seed (int, optional): Seed for reproducibility. Defaults to 0.

        Raises:
            ValueError: Unknown method selected.

        Returns:
            Union[Instances, MultipleReturn]: Prototypes for each methods and split.
        """
        if isinstance(method, str):
            method = [method]
        method = [str.lower(m) for m in method]

        from text_explainability import (KMedoids, LabelwiseKMedoids,
                                         LabelwiseMMDCritic, MMDCritic)

        methods = {"mmdcritic": (MMDCritic, LabelwiseMMDCritic), "kmedoids": (KMedoids, LabelwiseKMedoids)}

        if isinstance(splits, str):
            splits = [splits]

        def inner(m, split):
            if m not in methods:
                raise ValueError(f'Unknown method "{m}", choose from {list(methods.keys())}')
            instances = self.ingestibles.get_named_split(split, validate=True)
            if labelwise:
                return methods[m][1](instances=instances, labels=self.labels, embedder=embedder).prototypes(n=n)
            return methods[m][0](instances=instances, embedder=embedder).prototypes(n=n)

        explanations = []
        for split in splits:
            for m in method:
                explanations.append(inner(m, split))

        return self.__return_explanations(explanations)

    @restyle
    def prototypes_criticisms(
        self,
        n_prototypes: int = 5,
        n_criticisms: int = 3,
        splits: Union[str, List[str]] = "test",
        embedder: Optional[Embedder] = SentenceTransformer,
        labelwise: bool = False,
        **kwargs,
    ) -> Union[Instances, MultipleReturn]:
        """Select n prototypes (representative samples) and n criticisms (outliers) for the given split(s).

        Args:
            n_prototypes (int, optional): Number of prototypes to generate. Defaults to 5.
            n_criticsms (int, optional): Number of criticisms to generate. Defaults to 3.
            splits (Union[str, List[str]], optional): Name(s) of split(s). Defaults to "test".
            embedder (Optional[Embedder], optional): Embedder used. Defaults to SentenceTransformer.
            labelwise (bool, optional): Select for each label. Defaults to False.

        Returns:
            Union[Instances, MultipleReturn]: Prototypes for each methods and split.
        """
        from text_explainability import LabelwiseMMDCritic, MMDCritic

        if isinstance(splits, str):
            splits = [splits]

        def inner(split):
            instances = self.ingestibles.get_named_split(split, validate=True)
            m = (
                LabelwiseMMDCritic(instances=instances, labels=self.labels, embedder=embedder)
                if labelwise
                else MMDCritic(instances=instances, embedder=embedder)
            )
            return m(n_prototypes=n_prototypes, n_criticisms=n_criticisms, **kwargs)

        return self.__return_explanations([inner(split) for split in splits])
