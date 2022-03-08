"""Functions/classes for sensitivity testing (fairness and robustness) for text data."""

from typing import List, Optional, Union

from genbase import Readable
from text_sensitivity import (OneToManyPerturbation, OneToOnePerturbation,
                              RandomAscii, RandomCyrillic, RandomDigits,
                              RandomEmojis, RandomLower, RandomPunctuation,
                              RandomSpaces, RandomString, RandomUpper,
                              RandomWhitespace, compare_accuracy,
                              compare_metric, compare_precision,
                              compare_recall, input_space_robustness,
                              invariance, mean_score, perturbation)
from text_sensitivity.return_types import SuccessTest

from ...ingestibles import Ingestible
from ...mixins import IngestiblesMixin
from ...ui.notebook import restyle

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
perturbation = restyle(perturbation)


class Exposer(Readable, IngestiblesMixin):
    def __init__(self, data=None, model=None, ingestibles=None):
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
        generator = [GENERATORS[generator] if isinstance(generator, str) and generator in GENERATORS else generator]
        return input_space_robustness(
            model=self.model,
            generators=generators,
            n_samples=n_samples,
            min_length=min_length,
            max_length=max_length,
            seed=seed,
            **kwargs
        )
