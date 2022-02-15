*<p align="center">
  <img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/explabox.png" alt="explate logo">*
</p>

**<h3 align="center">
"{`Explain` | `Debug` | `Test` | `Validate`} your model with the *explabox*!"**
</h3>

---

The `explabox` aims to support data scientists and machine learning (ML) engineers in explaining, testing and documenting AI/ML models, developed in-house and or acquired externally. The `explabox` improves the following processes:

- __Transparency__: Describing aspects of the model and data.
- __Model performance__: Calculating quantitative metrics on how the model performs.
- __Explainability__: Various methods for explaining the whole dataset (_global_), model behavior on the dataset (_global_), and specific predictions/decisions (_local_).
- __Sensitivity (robustness)__: The effect of random inputs on the model (_robustness_) and testing model generalizability (_robustness_).
- __Sensitivity (fairness)__: The effect of adjustments of attributes in the inputs (e.g. swapping male pronouns for female pronouns; _fairness__), for the dataset as a whole (_global_) as well as for individual instances (_local_).

A number of tools in the `explabox` can also be used to provide transparency and explanations for local/global explanations to stakeholders, such as end-users or clients.

> :information_source: The `explabox` currently only supports natural language text as a modality. In the future, we intend to extend the toolkit to other modalities.

&copy; National Police Lab AI (NPAI), 2022

## Quick tour
...

## Installation
Before installation, check if the required packages (in `requirements.txt`) have been installed. Installation can be done via `pip install -r requirements.txt`.

The `explabox` requires _Python 3.8_ or above.

## Releases
The `explabox` is officially released through [PyPI](https://pypi.org/project/explabox/).

See [CHANGELOG.md](CHANGELOG.md) for a full overview of the changes for each version.

## Contributing
...
