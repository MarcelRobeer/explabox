*<p align="center">
  <img src="https://github.com/MarcelRobeer/explabox/blob/main/img/explabox.png?raw=true" alt="explabox logo">*
</p>

**<h3 align="center">
"{`Explore` | `Examine` | `Expose` | `Explain`} your model with the *explabox*!"**
</h3>

---

| Status | |
|:-----------------|:------------------
| _Latest release_ | [![PyPI](https://img.shields.io/pypi/v/explabox)](https://pypi.org/project/explabox/)  [![Downloads](https://pepy.tech/badge/explabox)](https://pepy.tech/project/explabox)  [![Python_version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/explabox/)  [![License](https://img.shields.io/pypi/l/explabox)](https://www.gnu.org/licenses/lgpl-3.0.en.html)
| _Development_ | [![Lint, Security & Tests](https://github.com/MarcelRobeer/explabox/actions/workflows/check.yml/badge.svg)](https://github.com/MarcelRobeer/explabox/actions/workflows/check.yml)  [![codecov](https://codecov.io/gh/MarcelRobeer/explabox/branch/main/graph/badge.svg?token=7XVEUE5PDM)](https://codecov.io/gh/MarcelRobeer/explabox)  [![Documentation Status](https://readthedocs.org/projects/explabox/badge/?version=latest)](https://explabox.readthedocs.io/en/latest/?badge=latest)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

The `explabox` aims to support data scientists and machine learning (ML) engineers in explaining, testing and documenting AI/ML models, developed in-house or acquired externally. The `explabox` turns your **ingestibles** (AI/ML model and/or dataset) into **digestibles** (statistics, explanations or sensitivity insights)!

*<p align="center">
  <img src="https://github.com/MarcelRobeer/explabox/blob/main/img/ingestibles-to-digestibles.png?raw=true" alt="ingestibles to digestibles">*
</p>

The `explabox` can be used to:

- __Explore__: describe aspects of the model and data.
- __Examine__: calculate quantitative metrics on how the model performs.
- __Expose__: see model sensitivity to random inputs (_safety_), test model generalizability (e.g. sensitivity to typos; _robustness_), and see the effect of adjustments of attributes in the inputs (e.g. swapping male pronouns for female pronouns; _fairness_), for the dataset as a whole (_global_) as well as for individual instances (_local_).
- __Explain__: use XAI methods for explaining the whole dataset (_global_), model behavior on the dataset (_global_), and specific predictions/decisions (_local_).

A number of experiments in the `explabox` can also be used to provide transparency and explanations to stakeholders, such as end-users or clients.

> :information_source: The `explabox` currently only supports natural language text as a modality. In the future, we intend to extend to other modalities.

&copy; National Police Lab AI (NPAI), 2022

<a name="quick-tour"/></a>
## Quick tour
The `explabox` is distributed on [PyPI](https://pypi.org/project/explabox/). To use the package with Python, install it (`pip install explabox`), import your `data` and `model` and wrap them in the `Explabox`. The example dataset and model shown here can be easily imported using demo package `explabox-demo-drugreview`.

> :information_source: To easily follow along without a need for installation, run the Notebook in [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14lXvXV01DaSruSAhD1RLbILRl2mPQ4nS?usp=sharing)

First, import the pre-provided `model`, and import the `data` from the `dataset_file`. All we need to know is in which column(s) your data is, and where we can find the corresponding labels:

```python
from explabox_demo_drugreview import model, dataset_file
from explabox import import_data

data = import_data(dataset_file,
                   data_cols='review',
                   label_cols='rating')
```

Second, we provide the `data` and `model` to the `Explabox`, and it does the rest! Rename the splits from your file names for easy access:
```python
from explabox import Explabox

box = Explabox(data=data,
               model=model,
               splits={'train': 'drugsComTrain.tsv', 'test': 'drugsComTest.tsv'})
```

Then `.explore`, `.examine`, `.expose` and `.explain` your model:
```python
# Explore the descriptive statistics for each split
box.explore()
```
<img src="https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_explore.png?raw=true" alt="drugscom_explore" width="600"/>

```python
# Show wrongly classified instances
box.examine.wrongly_classified()
```
<img src="https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_examine.png?raw=true" alt="drugscom_examine" width="600"/>

```python
# Compare the performance on the test split before and after adding typos to the text
box.expose.compare_metric(split='test', perturbation='add_typos')
```
<img src="https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_expose.png?raw=true" alt="drugscom_expose" width="600"/>

```python
# Get a local explanation (uses LIME by default)
box.explain.explain_prediction('Hate this medicine so much!')
```
<img src="https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_explain.png?raw=true" alt="drugscom_explain" width="600"/>


For more information, visit the [explabox documentation](https://explabox.rtfd.io).

# Contents
- [Quick tour](#quick-tour)
- [Installation](#installation)
- [Documentation](#documentation)
- [Example usage](#example-usage)
- [Advanced set-up](#advanced-setup)
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

<img src="https://github.com/MarcelRobeer/explabox/blob/main/img/layers.png?raw=true" alt="layers" width="400"/>

The `explabox` consists of three layers:
1. __Ingestibles__ provide a unified interface for importing models and data, which abstracts away how they are accessed and allows for optimized processing.
2. __Analyses__ are used to turn opaque ingestibles into transparent digestibles. The four types of analyses are _explore_, _examine_, _explain_ and _expose_.
3. __Digestibles__ provide insights into model behavior and data, assisting stakeholders in increasing the explainability, fairness, auditability and safety of their AI systems. Depending on their needs, these can be accessed interactively (e.g. via the Jupyter Notebook UI or embedded via the API) or through static reporting.

<a name="example-usage"/></a>
## Example usage
The [example usage guide](EXAMPLE_USAGE.md) showcases the `explabox` for a black-box model performing multi-class classification of the [UCI Drug Reviews](https://archive.ics.uci.edu/dataset/461/drug+review+dataset+druglib+com) dataset.

Without requiring any local installations, the notebook is provided on [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14lXvXV01DaSruSAhD1RLbILRl2mPQ4nS?usp=sharing).

If you want to follow along on your own device, simply `pip install explabox-demo-drugreview` and run the lines in the [Jupyter notebook](https://colab.research.google.com/drive/14lXvXV01DaSruSAhD1RLbILRl2mPQ4nS?usp=sharing) we have prepared for you!

<a name="advanced-setup"></a>
## Advanced set-up
When importing your own model and data, you can refer to a(n) (archive of) file(s), on disk or with an online URL. The `explabox` does all the importing for you. Consult the [ingestibles documentation](https://explabox.readthedocs.io/en/latest/overview.html#ingestibles) for an up-to-date list of the supported file formats.

```python
from explabox import import_data, import_model

data = import_data('./drugsCom.zip',
                   data_cols='review',
                   label_cols='rating')

model = import_model('model.onnx',
                     label_map={0: 'negative', 1: 'neutral', 2: 'positive'})
```

In this example, the data in the archive `drugsCom.zip` contains two `.tsv` (tab-separated values) files with the data in the `review` column and the gold labels in the `rating` column. The two files in `drugsCom.zip` are `drugsComTrain.tsv` and `drugsComTest.tsv`, containing the training data and test data, respectively.

The model is provided as an `onnx` file, where output `0` corresponds to a `negative` review, `1` to a `neutral` review, and `2` to a `positive` review.

You can add a mapping from the files in `drugsCom.zip` that refer to your train/test/validation splits by renaming them for easy access:
```python
from explabox import Explabox

box = Explabox(data=data,
               model=model,
               splits={'train': 'drugsComTrain.tsv', 'test': 'drugsComTest.tsv'})
```

Now you can `.explore`, `.examine`, `.expose` and `.explain` your data and model as usual.

<a name="releases"/></a>
## Releases
The `explabox` is officially released through [PyPI](https://pypi.org/project/explabox/). The [changelog](CHANGELOG.md) includes a full overview of the changes for each version.

<a name="contributing"/></a>
## Contributing
The `explabox` is an open-source project developed and maintained primarily by the Netherlands *National Police Lab AI* (NPAI). However, your contributions and improvements are still required! See [contributing](CONTRIBUTING.md) for a full contribution guide.

<a name="citation"></a>
## Citation
If you use the Explabox in your work, please read the corresponding paper at [doi:10.48550/arXiv.2411.15257](https://doi.org/10.48550/arXiv.2411.15257), and cite the paper as follows:

```bibtex
@misc{Robeer2024,
  title = {{The Explabox: Model-Agnostic Machine Learning Transparency \& Analysis}},
  author = {Robeer,  Marcel and Bron,  Michiel and Herrewijnen,  Elize and Hoeseni,  Riwish and Bex,  Floris},
  publisher = {arXiv},
  doi = {10.48550/arXiv.2411.15257},
  url = {https://arxiv.org/abs/2411.15257},
  year = {2024},
}
```
