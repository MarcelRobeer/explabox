.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/explabox.png?raw=true
   :alt: Explabox logo
   :align: center


{ ``Explore`` | ``Examine`` | ``Expose`` | ``Explain`` } your model with the *explabox*!
----------------------------------------------------------------------------------------

.. image:: https://img.shields.io/pypi/v/explabox
   :target: https://pypi.org/project/explabox/

.. image:: https://pepy.tech/badge/explabox
   :target: https://pepy.tech/project/explabox

.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue
   :target: https://pypi.org/project/explabox/

.. image:: https://img.shields.io/pypi/l/explabox
   :target: https://www.gnu.org/licenses/lgpl-3.0.en.html

.. image:: https://github.com/MarcelRobeer/explabox/actions/workflows/check.yml/badge.svg
   :target: https://github.com/MarcelRobeer/explabox/actions/workflows/check.yml

.. image:: https://codecov.io/gh/MarcelRobeer/explabox/branch/main/graph/badge.svg?token=7XVEUE5PDM
   :target: https://codecov.io/gh/MarcelRobeer/explabox

The ``explabox`` aims to support data scientists and machine learning (ML) engineers in explaining, testing and documenting AI/ML models, developed in-house or acquired externally. The ``explabox`` turns your **ingestibles** (AI/ML model and/or dataset) into **digestibles** (statistics, explanations or sensitivity insights)!

.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/ingestibles-to-digestibles.png?raw=true
   :alt: Ingestibles to digestibles
   :align: center

The ``explabox`` can be used to:

- **Explore**\ : describe aspects of the model and data.
- **Examine**\ : calculate quantitative metrics on how the model performs.
- **Expose**\ : see model sensitivity to random inputs (\ *robustness*\ ), test model generalizability (\ *robustness*\ ), and see the effect of adjustments of attributes in the inputs (e.g. swapping male pronouns for female pronouns; *fairness*\ ), for the dataset as a whole (\ *global*\ ) as well as for individual instances (\ *local*\ ).
- **Explain**\ : use XAI methods for explaining the whole dataset (\ *global*\ ), model behavior on the dataset (\ *global*\ ), and specific predictions/decisions (\ *local*\ ).

A number of experiments in the ``explabox`` can also be used to provide transparency and explanations to stakeholders, such as end-users or clients.

.. note::
    The ``explabox`` currently only supports natural language text as a modality. In the future, we intend to extend to other modalities.


Quick tour
----------

The ``explabox`` is distributed on `PyPI <https://pypi.org/project/explabox/>`_. To use the package with Python, install it (\ ``pip install explabox``\ ), import your ``data`` and ``model`` and wrap them in the ``Explabox``\ :

.. code-block:: python

   >>> from explabox import import_data, import_model
   >>> data = import_data('./drugsCom.zip', data_cols='review', label_cols='rating')
   >>> model = import_model('model.onnx', label_map={0: 'negative', 1: 'neutral', 2: 'positive'})

   >>> from explabox import Explabox
   >>> box = Explabox(data=data,
   ...                model=model,
   ...                splits={'train': 'drugsComTrain.tsv', 'test': 'drugsComTest.tsv'})

Then ``.explore``\ , ``.examine``\ , ``.expose`` and ``.explain`` your model:

.. code-block:: python

   >>> # Explore the descriptive statistics for each split
   >>> box.explore()


.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_explore.png?raw=true
   :alt: drugscom_explore


.. code-block:: python

   >>> # Show wrongly classified instances
   >>> box.examine.wrongly_classified()


.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_examine.png?raw=true
   :alt: drugscom_examine


.. code-block:: python

   >>> # Compare the performance on the test split before and after transforming all tokens to uppercase
   >>> box.expose.compare_metrics(split='test', perturbation='upper')


.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_expose.png?raw=true
   :alt: drugscom_expose


.. code-block:: python

   >>> # Get a local explanation (uses LIME by default)
   >>> box.explain.explain_prediction('Hate this medicine so much!')


.. image:: https://github.com/MarcelRobeer/explabox/blob/main/img/example/drugscom_explain.png?raw=true
   :alt: drugscom_explain


Using explabox
--------------
:doc:`installation`
    Installation guide, directly installing it via `pip`_ or through the `git`_.

:doc:`example-usage`
    An extended usage example, showcasing how you can *explore*, *examine*, *expose* and *explain* your AI model.

:doc:`overview`
   Overview of the general idea behind the `explabox` and its package structure.

:doc:`Explabox API reference <api/explabox>`
    A reference to all classes and functions included in the `explabox`.

Development
-----------
`Explabox @ GIT`_
    The `git`_ includes the open-source code and the most recent development version.

:doc:`changelog`
    Changes for each version are recorded in the changelog.

:doc:`contributing`
    A guide to making your own contributions to the open-source *explabox* package.

Citation
--------

...

.. _pip: https://pypi.org/project/explabox/
.. _git: https://github.com/MarcelRobeer/explabox
.. _`Explabox @ GIT`: https://github.com/MarcelRobeer/explabox

.. toctree::
   :maxdepth: 1
   :caption: Using explabox
   :hidden:

   installation.md
   example-usage.md

.. toctree::
   :maxdepth: 4
   :caption: API reference
   :hidden:

   overview.md
   api/explabox.rst

.. toctree::
   :maxdepth: 1
   :caption: Development
   :hidden:

   changelog.md
   contributing.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
