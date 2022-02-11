"""Functions/classes for sensitivity testing (fairness and robustness) for text data."""

from text_sensitivity import (
    OneToManyPerturbation,
    OneToOnePerturbation,
    compare_metric,
    compare_accuracy,
    compare_precision,
    compare_recall,
    input_space_robustness,
    invariance,
    mean_score,
    perturbation,
)

from ..ui.notebook import restyle

compare_metric = restyle(compare_metric)
input_space_robustness = restyle(input_space_robustness)
invariance = restyle(invariance)
perturbation = restyle(perturbation)
