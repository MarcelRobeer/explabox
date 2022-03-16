*<p align="center">
  <img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/explabox.png" alt="explabox logo">*
</p>

**<h3 align="center">
"{`Explore` | `Examine` | `Expose` | `Explain`} your model with the *explabox*!"**
</h3>

---

The `explabox` aims to support data scientists and machine learning (ML) engineers in explaining, testing and documenting AI/ML models, developed in-house or acquired externally. The `explabox` turns your **ingestibles** (AI/ML model and/or dataset) into **digestibles** (statistics, explanations or sensitivity insights)!

> figure: ingestibles to digestibles

The `explabox` can be used to:

- __Explore__: describe aspects of the model and data.
- __Examine__: calculate quantitative metrics on how the model performs
- __Expose__: see model sensitivity to random inputs (_robustness_), test model generalizability (_robustness_), and see the effect of adjustments of attributes in the inputs (e.g. swapping male pronouns for female pronouns; _fairness_), for the dataset as a whole (_global_) as well as for individual instances (_local_).
- __Explain__: use XAI methods for explaining the whole dataset (_global_), model behavior on the dataset (_global_), and specific predictions/decisions (_local_).

A number of experiments in the `explabox` can also be used to provide transparency and explanations to stakeholders, such as end-users or clients.

> :information_source: The `explabox` currently only supports natural language text as a modality. In the future, we intend to extend to other modalities.

&copy; National Police Lab AI (NPAI), 2022

<a name="quick-tour"/></a>
## Quick tour
The `explabox` is distributed on [PyPI](https://pypi.org/project/explabox/). To use the package with Python, install it (`pip install explabox`), import your `data` and `model` and wrap them in the `Explabox`:

```python
>>> from explabox import import_data, import_model
>>> data = import_data('./drugsCom.zip', data_cols='review', label_cols='rating')
>>> model = import_model('model.onnx', label_map={0: 'negative', 1: 'neutral', 2: 'positive'})

>>> from explabox import Explabox
>>> box = Explabox(data=data,
...                model=model,
...                splits={'train': 'drugsComTrain.tsv', 'test': 'drugsComTest.tsv'})
```

Then `.explore`, `.examine`, `.expose` and `.explain` your model:
```python
>>> # Explore the descriptive statistics for each split
>>> box.explore()
```
<img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/example/drugscom_explore.png" alt="drugscom_explore" width="400"/>

```python
>>> # Show wrongly classified instances
>>> box.examine.wrongly_classified()
```
<img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/example/drugscom_examine.png" alt="drugscom_examine" width="400"/>

```python
>>> # Compare the performance on the test split before and after transforming all tokens to uppercase
>>> box.expose.compare_metrics(split='test', perturbation='upper')
```
<img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/example/drugscom_expose.png" alt="drugscom_expose" width="400"/>

```python
>>> # Get a local explanation (uses LIME by default)
>>> box.explain.local_explanation('Hate this medicine so much!')
```
<img src="https://git.science.uu.nl/m.j.robeer/explabox/-/raw/main/img/example/drugscom_explain.png" alt="drugscom_explain" width="400"/>


For more information, visit the [explabox documentation](https://explabox.rtfd.io).

# Contents
- [Quick tour](#quick-tour)
- [Installation](#installation)
- [Documentation](#documentation)
- [Example usage](#example-usage)
- [Releases](#releases)
- [Contributing](#contributing)
- [Citation](#citation)

<a name="installation"/></a>
## Installation
The easiest way to install the latest release of the `explabox` is through `pip`:

```console
user@terminal:~$ pip install explabox
Collecting explabox
...
Installing collected packages: explabox
Successfully installed explabox
```

> :information_source: The `explabox` requires _Python 3.8_ or above.

See the [full installation guide](INSTALLATION.md) for troubleshooting the installation and other installation methods.

<a name="documentation"/></a>
## Documentation
Documentation for the `explabox` is hosted externally on [explabox.rtfd.io](https://explabox.rtfd.io).

<a name="example-usage"/></a>
## Example usage
...

<a name="releases"/></a>
## Releases
The `explabox` is officially released through [PyPI](https://pypi.org/project/explabox/). The [changelog](CHANGELOG.md) includes a full overview of the changes for each version.

<a name="contributing"/></a>
## Contributing
The `explabox` is an open-source project developed and maintained primarily by the Netherlands *National Police Lab AI* (NPAI). However, your contributions and improvements are still required! See [contributing](CONTRIBUTING.md) for a full contribution guide.

<a name="citation"></a>
## Citation
...

```bibtex
```
