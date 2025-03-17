---
title: 'The Explabox: Model-Agnostic Machine Learning Transparency & Analysis'
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

We present the `Explabox`: an open-source toolkit for transparent and responsible machine learning (ML) model development and usage. `Explabox` aids in achieving explainable, fair and robust models by employing a four-step strategy: *explore*, *examine*, *explain* and *expose*. These steps offer model-agnostic analyses that transform complex `ingestibles` (models and data) into interpretable `digestibles`. The toolkit encompasses digestibles for descriptive statistics, performance metrics, model behavior explanations (local and global), and robustness, security, and fairness assessments. Implemented in Python, `Explabox` supports multiple interaction modes and builds on open-source packages. It empowers model developers and testers to operationalize explainability, fairness, auditability, and security. The initial release focuses on text data and models, with plans for expansion. `Explabox`'s code and documentation are available open-source at [https://explabox.readthedocs.io](https://explabox.readthedocs.io/en/stable).

# Statement of need

It is crucial that Machine Learning (ML) development and usage is done in a responsible and transparent manner. High-stakes organizational decisions may significantly impact individuals and society, with potential severe consequences stemming from biases or model errors. This is exemplified by the EU AI Act's regulatory framework, requiring high-risk systems to be properly tested, documented and assessed on their conformity before being applied in practice [@Edwards2022]. Yet, operationalizing transparency (explainable ML) and testing model behavior (fairness, robustness, and security auditing) remains a difficult and laborious task, given the myriad of techniques and their associated learning curves. In response, we have devised a comprehensive four-step analysis strategy&mdash;*explore*, *examine*, *explain*, and *expose*&mdash;ensuring holistic model transparency and testing. The open-source `Explabox` offers these analyses through well-documented, reproducible steps. Data scientists can now access a unified, model-agnostic approach developed and used in a high-stakes context&mdash;the Netherlands National Police&mdash;that is applicable to any text classifier or regressor.

We have developed the `Explabox` in an organizational environment where models and data are analyzed repeatedly, and where internal and external stakeholders have varying explanatory needs and preferred formats. Several related tools have been made available, such as `AIX360` [@Arya2019], `alibi` explain [@Klaise2021], `dalex` [@Baniecki2021], `CheckList` [@Ribeiro2020], and `AIF360` [@Bellamy2018]. However, these tools exhibit shortcomings such as incompatibility with recent Python versions (3.8&ndash;3.12), restricted software functionality primarily focused on testing or explainability, an absence of reproducible outcomes, or the lack of means to provide the flexibility regarding how results can be communicated to address stakeholder needs. To fill this gap, we propose the `Explabox`. The `Explabox` is an open-source Python toolkit that supports organizations with responsible ML development with minimal disruption to practitioners' workflows through a four-step analysis strategy easily embedded with existing datasets and models, and providing a central node for connecting with state-of-the-art research and sharing best practices.

# Explore, Examine, Explain & Expose your ML models

The `Explabox` transforms opaque *ingestibles* into transparent *digestibles* through four types of *analyses*. The digestibles provide insights into model behavior and data, enhancing model explainability and assisting in auditing the fairness, robustness, and security of ML systems.

## Ingestibles
Ingestibles serve as a unified interface for importing models and data. The layers (\autoref{fig:layers}) abstract away from how the model and data are accessed, and allow for optimized processing. The `Explabox` encapsulates the model and data with `instancelib` [@instancelib] to ensure fast processing. The model can be any Python `Callable` containing a regression or (binary and multi-class) classification model. Models developed with `scikit-learn` [@scikit-learn] or with inferencing through `onnx` (e.g., PyTorch and TensorFlow/Keras) can be imported directly with further optimizations and automatic extraction of how inputs/outputs are to be interpreted. Data can be automatically downloaded, extracted and loaded. Data can be provided as `NumPy` arrays, `Pandas` DataFrames, `huggingface` datasets, raw files (e.g., HDF5, CSV or TSV), or as (compressed) folders containing raw files. The data can be subdivided into named splits (e.g., train-test-validation), and instance vectors and tokens can be precomputed (and optionally saved on disk) to provide fast inferencing.

![Logical separation of the `Explabox` into layers with interfaces.\label{fig:layers}](figure1.png){width=50%}

## Analyses

The `Explabox` turns these *ingestibles* into *digestibles*: pieces of information that increase the transparency of the ingestibles. Turning ingestibles into digestibles is done through four types of analyses: **explore**, **examine**, **explain** and **expose**.

**Explore** allows slicing, dicing and sorting data, and provides descriptive statistics, grouped by named split. Relevant statistics include data set sizes and label distributions, and modality-relevant information, such as string lengths and tokenized lengths for textual data.

**Examine** shows performance metrics of the ML model on the data, summarized in a table or shown graphically. Metrics are accompanied by references on how they are computed and how they should be interpreted. For further analysis, **examine** also supports to drill-down into which instances were predicted correctly and incorrectly.

**Explain** uses model-agnostic techniques [@Ribeiro2016b] to explain model behavior (*global*) and individual predictions (*local*). It summarizes model-labelled data, through prototypes (`K-Medoids`) or prototypes and criticisms (`MMDCritic` [@Kim2016]), and token distributions (`TokenFrequency`) and informativeness (`TokenInformation`) for the text modality. Local explanations are given by popular techniques for feature attribution scores (`LIME` [@Ribeiro2016a], `KernelSHAP` [@Lundberg2017]), relevant feature subsets (`Anchors` [@Ribeiro2018]), local rule-based models (`LORE` [@Guidotti2018]), and counterfactual/contrastive explanations (`FoilTrees` [@Waa2018]). These methods are constructed from generic components that split the relevant steps in global and local explanation generation. This allows customizability and for scientific advancements to quickly end up in operational processes. For example, they may combine the data sampling from `KernelSHAP` and summarize these with a surrogate rule-based model provided by the `imodels` package [@Singh2021]. However, to ease users into adoption we provide example configurations, such as `LIME` with default hyperparameters. **Explain** is provided by subpackage `text_explainability` [@text_explainability], which doubles as a standalone tool.

**Expose** gathers sensitivity insights through local/global testing regimes. These insights can be used to, through relevant attributes, assess the *robustness* (e.g., the effect of typos on model performance), *security* (e.g., if inputs containing certain characters crash the model) and *fairness* (e.g., subgroup performance for protected attributes such as country of origin, gender, race or socioeconomic status) of the model. Relevant attributes can either be observed in the current data or generated from user-provided templates [@Ribeiro2020] filled with multi-language data generation [@Faker]. These attributes are then either summarized in performance metrics, compared to expected behavior [@Ribeiro2020], or assessed with fairness metrics for classification [@Mehrabi2021] and regression [@Agarwal2019]. Like **explain**, **expose** is also made from generic components, which allows users to customize data generation and tests. **Expose** is provided by the `text_sensitivity` subpackage [@text_sensitivity], which also doubles as a standalone tool.

## Digestibles

To serve diverse stakeholders' needs&mdash;such as auditors, applicants, end-users or clients [@Tomsett2018]&mdash;in consuming model and data insights, the digestibles are accessible through different channels like an interactive user interface (UI) for Jupyter Notebook or webpages (\autoref{fig:ui}) with `plotly` [@plotly] visualizations, an API for integration with other tooling, and static reporting.

![UI elements of the Jupyter Notebook interface for interactive explainability and analyses.\label{fig:ui}](figure2.png)

# Acknowledgements

Development of the Explabox was supported by the Netherlands National Police. The authors would like to thank all anonymous contributors within the Netherlands National Police for their contributions to software development, testing and active usage. In addition, the authors would like to thank the participants of the demos at ICT.OPEN 2022, the National Police Lab AI at Utrecht University, and the University Medical Center Utrecht for their valuable feedback.

# References
