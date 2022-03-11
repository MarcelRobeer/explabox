"""Functions/classes for sensitivity testing (fairness and robustness) for text data."""

from typing import List, Literal, Optional, Union

from genbase import Readable
from instancelib import AbstractClassifier, Environment
from instancelib.typehints import LT
from text_sensitivity import (
    OneToManyPerturbation,
    OneToOnePerturbation,
    RandomAscii,
    RandomCyrillic,
    RandomDigits,
    RandomEmojis,
    RandomLower,
    RandomPunctuation,
    RandomSpaces,
    RandomString,
    RandomUpper,
    RandomWhitespace,
    compare_accuracy,
    compare_metric,
    compare_precision,
    compare_recall,
    input_space_robustness,
    invariance,
    mean_score,
    perturbation,
)
from text_sensitivity.return_types import MeanScore, SuccessTest

from explabox.utils import MultipleReturn

from ...ingestibles import Ingestible
from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
mean_score = restyle(mean_score)
perturbation = restyle(perturbation)


class Exposer(Readable, IngestiblesMixin):
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

    def input_space(
        self,
        generators: List[Union[RandomString, str]],
        n_samples: int = 100,
        min_length: int = 0,
        max_length: int = 100,
        seed: Optional[int] = 0,
        **kwargs
    ) -> SuccessTest:
        """Test the robustness of a machine learning model to different input types.

        Example:
            Test a pretrained black-box `model` for its robustness to 1000 random strings (length 0 to 500),
            containing whitespace characters, ASCII (upper, lower and numbers), emojis and Russian Cyrillic characters:

            >>> from explabox import Explabox, RandomEmojis, RandomCyrillic
            >>> box = Explabox(data=data, model=model)
            >>> box.expose.input_space(generators=['whitespace', 'ascii', RandomEmojis(base=True), RandomCyrillic('ru')],
            ...                        n_samples=1000,
            ...                        min_length=0,
            ...                        max_length=500)

        Args:
            generators (List[RandomString]): Random character generators.
            n_samples (int, optional): Number of test samples. Defaults to 100.
            min_length (int, optional): Input minimum length. Defaults to 0.
            max_length (int, optional): Input maximum length. Defaults to 100.
            seed (Optional[int], optional): Seed for reproducibility purposes. Defaults to 0.

        Returns:
            SuccessTest: Percentage of success cases, list of succeeded/failed instances
        """
        GENERATORS = {
            "ascii": RandomAscii(),
            "emojis": RandomEmojis(),
            "whitespaces": RandomWhitespace(),
            "spaces": RandomSpaces(),
            "ascii_upper": RandomUpper(),
            "acii_lower": RandomLower(),
            "digits": RandomDigits(),
            "punctuation": RandomPunctuation(),
            "cyrillic": RandomCyrillic(),
        }
        generator = [
            GENERATORS[str.lower(generator)]
            if isinstance(generator, str) and str.lower(generator) in GENERATORS
            else generator
        ]

        return input_space_robustness(
            model=self.model,
            generators=generators,
            n_samples=n_samples,
            min_length=min_length,
            max_length=max_length,
            seed=seed,
            **kwargs
        )

    def invariance(self, pattern: str, expectation: Optional[LT], **kwargs) -> SuccessTest:
        """Test for the failure rate under invariance.

        Example:
            Test if predictions remain 'positive' for 50 samples of the pattern `'I {like|love} {name} from {city}!'`:

            >>> from explabox import Explabox
            >>> box = Explabox(data=data, model=model)
            >>> box.expose.invariance('I {like|love} {name} from {city}!', expectation='positive', n_samples=50)

        Args:
            pattern (str): String pattern to generate examples from.
            expectation (Optional[LT], optional): Expected outcome values. Defaults to None.
            **kwargs: Optional arguments passed onto the `data.generate.from_pattern()` function.

        Returns:
            SuccessTest: Percentage of success cases, list of succeeded (invariant)/failed (variant) instances
        """
        return invariance(pattern=pattern, model=self.model, expectation=expectation, **kwargs)

    def mean_score(
        self, pattern: str, selected_labels: Optional[Union[LT, List[LT]]] = "all", **kwargs
    ) -> Union[MeanScore, MultipleReturn]:
        """Calculate mean (probability) score for the given labels, for data generated from a pattern.

        Example:
            Calculate the mean score for the 'positive' label for `'I {like|love} {name} from {city}!'`:

            >>> from explabox import Explabox
            >>> box = Explabox(data=data, model=model)
            >>> box.expose.mean_score('I {like|love} {name} from {city}!', selected_labels='positive', seed=0)

        Args:
            pattern (str): Pattern to generate instance from.
            selected_labels (Optional[Union[LT, List[LT]]], optional): Label name to select(s). If None or 'all' it
                is replaced by all labels. Defaults to 'all'.
            **kwargs: Optional arguments passed onto the `data.generate.from_pattern()` function.

        Todo:
            * Avoid multiple calls to self.model and generate_pattern for multiple labels

        Returns:
            Union[MeanScore, MultipleReturn]: Mean score for one label or all selected labels.
        """
        if isinstance(selected_labels, str) and str.lower(selected_labels) == "all" or selected_labels is None:
            selected_labels = self.labelset

        if not isinstance(selected_labels, list):
            return mean_score(pattern=pattern, model=self.model, selected_label=selected_labels, **kwargs)

        return MultipleReturn(
            [
                mean_score(pattern=pattern, model=self.model, selected_labels=label, **kwargs)
                for label in selected_labels
            ]
        )
