---
title: 'Explabox: Model-Agnostic Machine Learning Transparency & Analysis'
tags:
    - Python
    - explainable AI (XAI)
    - interpretability
    - fairness
    - robustness
    - AI safety
    - AI auditing
authors:
  - name: Marcel Robeer
    orcid: 0000-0002-6430-9774
    affiliation: "1, 2"
  - name: Michiel Bron
    orcid: 0000-0002-4823-6085
    affiliation: "1, 2"
  - name: Elize Herrewijnen
    orcid: 0000-0002-2729-6599
    affiliation: "1, 2"
  - name: Riwish Hoeseni
    affiliation: 2
  - name: Floris Bex
    orcid: 0000-0002-5699-9656
    affiliation: "1, 3"
affiliations:
  - name: National Police Lab AI, Utrecht University, The Netherlands
    index: 1
    ror: 04pp8hn57
  - name: Netherlands National Police, The Netherlands
    index: 2
  - name: School of Law, Utrecht University, The Netherlands
    index: 3
    ror: 04pp8hn57
date: 13 March 2025
bibliography: paper.bib
---

# Summary

`Explabox` is an open-source toolkit for transparent and responsible machine learning (ML) development and usage. It promotes explainable, fair, and robust models using a four-step strategy: *explore*, *examine*, *explain* and *expose*. These model-agnostic steps transform complex `ingestibles` (models, data) into interpretable `digestibles`, covering descriptive statistics, performance, local/global explanations, and robustness, security and fairness assessments. Implemented in Python, `Explabox` supports multiple interaction modes, helping developers/testers operationalize explainability, fairness, auditability, and security. The initial release focuses on text data/models, with expansion planned. Code and documentation are available open-source at [https://explabox.readthedocs.io](https://explabox.readthedocs.io/en/stable).

# Statement of need

Responsible and transparent Machine Learning (ML) development and usage has become crucial. High-stakes decisions can significantly impact individuals and society, with severe consequences potentially stemming from biases or errors. For example, the EU AI Act requires high-risk systems to be tested, documented, and assessed before practical application [@Edwards2022]. However, operationalizing transparency (explainable ML) and testing model behavior (fairness, robustness, and security auditing) remains difficult due to the myriad techniques and their learning curves. We devised a four-step analysis strategy&mdash;*explore*, *examine*, *explain*, and *expose*&mdash;to ensure holistic model transparency and testing. The open-source `Explabox` offers these analyses through well-documented, reproducible steps. Data scientists gain a unified, model-agnostic approach, developed and used in a high-stakes environment, applicable to any text classifier/regressor.

`Explabox` was developed in an organizational environment where models and data are analyzed repeatedly, and where internal and external stakeholders have varying explanatory needs and preferred formats. Several related tools exist, such as `AIX360` [@Arya2019], `alibi` explain [@Klaise2021], `dalex` [@Baniecki2021], `CheckList` [@Ribeiro2020], and `AIF360` [@Bellamy2018]. However, these tools may be incompatible with recent Python versions (3.8&ndash;3.12), have restricted functionality (testing or explainability focus), lack reproducibility, or lack flexibility communicating results. `Explabox` is an open-source Python toolkit supporting esponsible ML development with minimal workflow disruption for practitioners addressing this gap. Its four-step strategy applies to existing data/models and acts as a hub connecting research and best practices.

# Explore, Examine, Explain & Expose your ML models

`Explabox` transforms opaque *ingestibles* into transparent *digestibles* through four types of *analyses* to enhance explainability and aid fairness, robustness, and security audits.

## Ingestibles
Ingestibles provide a unified model/data import interface, where layers abstract away access (\autoref{fig:layers}) to allow optimized processing. `Explabox` uses `instancelib` [@instancelib] for fast model/data encapsulation. The model can be any Python `Callable` containing a regression or (binary and multi-class) classification model. `scikit-learn` or `onnx` models (e.g., PyTorch, TensorFlow/Keras) import directly with optimizations and automatic input/output interpretation. Data can be automatically downloaded, extracted and loaded. Data inputs include `NumPy`/`Pandas`/`huggingface`, raw files (e.g., HDF5, CSV or TSV), and (compressed) file folders. Data can be subdivided into named splits (e.g., train-test-validation), and instance vectors and tokens can be precomputed (and optionally saved) for fast inferencing.

![Logical separation of `Explabox` into layers with interfaces.\label{fig:layers}](figure1.png){width=50%}

## Analyses

`Explabox` turns these *ingestibles* into *digestibles* (transparency-increasing information on ingestibles) through four *analyses* types: **explore**, **examine**, **explain** and **expose**.

**Explore** allows data slicing/dicing/sorting, and provides descriptive statistics (dataset sizes, label distributions, and text string/token lengths).

**Examine** shows model performance metrics, summarized in a table or shown graphically, and include computation/interpretation references. For further analysis, **examine** also supports drilling down into (in)correct predictions.

**Explain** uses model-agnostic techniques [@Ribeiro2016b] to explain model behavior (*global*) and individual predictions (*local*). It summarizes model-labelled data, through prototypes (`K-Medoids`) or prototypes and criticisms (`MMDCritic` [@Kim2016]), and token distributions (`TokenFrequency`) and informativeness (`TokenInformation`). Local explanations use popular techniques: feature attribution scores (`LIME` [@Ribeiro2016a], `KernelSHAP` [@Lundberg2017]), feature subsets (`Anchors` [@Ribeiro2018]), local rule-based models (`LORE` [@Guidotti2018]), and counterfactual/contrastive explanations (`FoilTrees` [@Waa2018]). Built from generic components separating global and local explanation steps, these methods allow customization and enable scientific advances to be quickly integrated into operational processes (e.g., combine `KernelShap` sampling with `imodels` [@Singh2021] surrogate rules). Example configurations, such as `LIME` with default hyperparameters, ease adoption. **Explain** is provided by subpackage `text_explainability` [@text_explainability], which doubles as a standalone tool.

**Expose** gathers sensitivity insights via local/global testing. These insights can be used to, through relevant attributes, assess the *robustness* (e.g., the effect of typos on model performance), *security* (e.g., if inputs containing certain characters crash the model), and *fairness* (e.g., subgroup performance for protected attributes such as country of origin, gender, race or socioeconomic status) of the model. Relevant attributes can either be observed in the current data or generated from user-provided templates [@Ribeiro2020] filled with multi-language data generation [@Faker]. These attributes are then either summarized in performance metrics, compared to expected behavior [@Ribeiro2020], or assessed with fairness metrics for classification [@Mehrabi2021] and regression [@Agarwal2019]. Like **explain**, **expose** is also made from generic components, which allows users to customize data generation and tests. **Expose** is provided by the `text_sensitivity` subpackage [@text_sensitivity], which also doubles as a standalone tool.

## Digestibles

Digestibles serve stakeholders&mdash;such as creators, auditors, applicants, end-users or clients [@Tomsett2018]&mdash;via a Jupyter/web UI (\autoref{fig:ui}) (using `plotly` [@plotly] visuals), integrated API, and static reporting.

![UI elements of the Jupyter Notebook interface for interactive explainability and analyses.\label{fig:ui}](figure2.png)

# Acknowledgements

Development was supported by the Netherlands National Police. The authors thank contributors within the Police for development, testing, and usage, and participants from ICT.OPEN 2022, the UU NPAI, and UMC Utrecht demos for their valuable feedback.

# References
