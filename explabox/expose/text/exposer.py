# Copyright (c) 2022 Marcel Robeer for National Police Lab AI (NPAI).
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License (LGPL) as published by the Free Software Foundation; either version 3 (LGPLv3) of the License, or (at
# your option) any later version. You may not use this file except in compliance with the license. You may obtain a copy
# of the license at:
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

"""Main Exposer class."""

from typing import List, Optional, Union

from genbase import Readable
from instancelib import AbstractClassifier, Environment, TextEnvironment
from instancelib.typehints import LT
from text_sensitivity import (
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
    compare_metric,
    input_space_robustness,
    invariance,
    mean_score,
)
from text_sensitivity.return_types import LabelMetrics, MeanScore, SuccessTest

from ...ingestibles import Ingestible
from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle
from ...utils import MultipleReturn

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
mean_score = restyle(mean_score)


class Exposer(Readable, IngestiblesMixin):
    def __init__(
        self,
        data: Optional[Environment] = None,
        model: Optional[AbstractClassifier] = None,
        ingestibles: Optional[Ingestible] = None,
        **kwargs,
    ):
        """The Exposer exposes your model and/or data, by performing sensitivity tests.

        With the Exposer you can see model sensitivity to random inputs (robustness), test model generalizability
        (robustness), and see the effect of adjustments of attributes in the inputs (e.g. swapping male pronouns for
        female pronouns; fairness), for the dataset as a whole (global) as well as for individual instances (local).

        The Exposer requires 'data' and 'model' defined. It is included in the Explabox under the `.expose` property.

        Examples:
            See how performance of a model on the test dataset is affected when text is randomly changed to uppercase:

            >>> from explabox.expose import Exposer
            >>> exposer = Exposer(data=data, model=model)
            >>> exposer.compare_metric(splits='test', perturbation='random_upper')

        Args:
            data (Optional[Environment], optional): Data for ingestibles. Defaults to None.
            model (Optional[AbstractClassifier], optional): Model for ingestibles. Defaults to None.
            ingestibles (Optional[Ingestible], optional): Ingestible. Defaults to None.
        """
        if ingestibles is None:
            ingestibles = Ingestible(data=data, model=model)
        self.ingestibles = ingestibles
        self.check_requirements(["data", "model"])

    def input_space(
        self,
        generators: Union[str, RandomString, List[Union[RandomString, str]]],
        n_samples: int = 100,
        min_length: int = 0,
        max_length: int = 100,
        seed: Optional[int] = 0,
        **kwargs,
    ) -> SuccessTest:
        """Test the robustness of a machine learning model to different input types (safety).

        Example:
            Test a pretrained black-box `model` for its robustness to 1000 random strings (length 0 to 500),
            containing whitespace characters, ASCII (upper, lower and numbers), emojis and Russian Cyrillic characters:

            >>> from explabox import Explabox, RandomEmojis, RandomCyrillic
            >>> box = Explabox(data=data, model=model)
            >>> box.expose.input_space(generators=['whitespace',
            ...                                    'ascii',
            ...                                    RandomEmojis(base=True),
            ...                                    RandomCyrillic('ru')],
            ...                        n_samples=1000,
            ...                        min_length=0,
            ...                        max_length=500)

        Args:
            generators (Union[str, RandomString, List[Union[RandomString, str]]]): Random character generators. If 'all'
                select all generators. For strings choose from 'ascii', 'emojis, 'whitespace', 'spaces', 'ascii_upper',
                'ascii_lower', 'digits', 'punctuation', 'cyrillic'.
            n_samples (int, optional): Number of test samples. Defaults to 100.
            min_length (int, optional): Input minimum length. Defaults to 0.
            max_length (int, optional): Input maximum length. Defaults to 100.
            seed (Optional[int], optional): Seed for reproducibility purposes. Defaults to 0.

        Returns:
            SuccessTest: Percentage of success cases, list of succeeded/failed instances
        """
        GENERATORS = {
            "ascii": RandomAscii,
            "emojis": RandomEmojis,
            "whitespace": RandomWhitespace,
            "spaces": RandomSpaces,
            "ascii_upper": RandomUpper,
            "ascii_lower": RandomLower,
            "digits": RandomDigits,
            "punctuation": RandomPunctuation,
            "cyrillic": RandomCyrillic,
        }

        if generators == "all":
            generators = list(GENERATORS.keys())
        if isinstance(generators, (str, RandomString)):
            generators = [generators]

        generators = [
            (
                GENERATORS[str.lower(generator)]()
                if isinstance(generator, str) and str.lower(generator) in GENERATORS
                else generator
            )
            for generator in generators
        ]

        for generator in generators:
            if not isinstance(generator, RandomString):
                raise ValueError(f'Unknown generator "{generator}"')

        return input_space_robustness(
            model=self.model,
            generators=generators,
            n_samples=n_samples,
            min_length=min_length,
            max_length=max_length,
            seed=seed,
            **kwargs,
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
        self,
        pattern: str,
        selected_labels: Optional[Union[LT, List[LT]]] = "all",
        **kwargs,
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

        def ms(label):
            return mean_score(pattern=pattern, model=self.model, selected_label=label, **kwargs)

        return (
            ms(selected_labels)
            if not isinstance(selected_labels, list)
            else MultipleReturn(*[ms(label) for label in selected_labels])
        )

    def compare_metric(
        self,
        perturbation: Union[OneToOnePerturbation, str],
        splits: Union[str, List[str]] = "test",
    ) -> Union[LabelMetrics, MultipleReturn]:
        """Compare metrics for each ground-truth label and attribute after applying a dataset-wide perturbation.

        Examples:
            Compare metric of model performance (e.g. accuracy, precision) before and after mapping each instance
            in the test dataset to uppercase:

            >>> box.expose.compare_metric(splits='test', peturbation='upper')

            Add '!!!' to the end of each text in the 'train' and 'test' split and see how it affects performance:

            >>> from explabox.expose.text import OneToOnePerturbation
            >>> perturbation_fn = OneToOnePerturbation(lambda x: f'{x}!!!')
            >>> box.expose.compare_metrics(splits=['train', 'test'], perturbation=perturbation_fn)

        Args:
            perturbation (Union[OneToOnePerturbation, str]): Custom perturbation or one of the default ones, picked by
                their string: 'lower', 'upper', 'random_lower', 'random_upper', 'add_typos', 'random_case_swap',
                'swap_random' (swap characters), 'delete_random' (delete characters), 'repeat' (repeats twice).
            splits (Union[str, List[str]], optional): Split to apply the perturbation to. Defaults to "test".

        Raises:
            ValueError: Unknown perturbation.

        Returns:
            Union[LabelMetrics, MultipleReturn]: Original label (before perturbation), perturbed label (after
                perturbation) and metrics for label-attribute pair.
        """
        from .characters import add_typos, delete_random, random_case_swap, random_lower, random_upper, swap_random
        from .sentences import repeat_k_times, to_lower, to_upper

        PERTURBATIONS = {
            "lower": to_lower,
            "upper": to_upper,
            "random_lower": random_lower,
            "random_upper": random_upper,
            "add_typos": add_typos,
            "random_case_swap": random_case_swap,
            "swap_random": swap_random,
            "delete_random": delete_random,
            "repeat": repeat_k_times(k=2),
        }

        if isinstance(perturbation, str):
            if perturbation not in PERTURBATIONS:
                raise ValueError(f'Unknown perturbation "{perturbation}", choose from {list(PERTURBATIONS.keys())}')
            perturbation = PERTURBATIONS[perturbation]

        def cm(split):
            env = TextEnvironment(
                dataset=self.ingestibles.get_named_split(split, validate=True),
                labelprovider=self.labels,
            )
            return compare_metric(env=env, model=self.model, perturbation=perturbation)

        return cm(splits) if isinstance(splits, str) else MultipleReturn(*[cm(split) for split in splits])
