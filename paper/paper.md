---
title: 'Explabox: A Python Toolkit for Standardized Auditing and Explanation of Text Models'
tags:
    - Python
    - AI auditing
    - explainable AI (XAI)
    - interpretability
    - fairness
    - robustness
    - AI safety
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
date: 29 August 2025
bibliography: paper.bib
---

# Summary

Developed to meet the practical machine learning (ML) auditing requirements of the Netherlands National Police, `Explabox` is an open-source Python toolkit that implements a standardized four-step analysis workflow: *explore*, *examine*, *explain* and *expose*. The framework transforms models and data (*ingestibles*) into interpretable reports and visualizations (*digestibles*), covering everything from data statistics and performance metrics to local and global explanations, and sensitivity testing for fairness, robustness and security. Designed for developers, testers, and auditors, `Explabox` operationalizes the entire audit lifecycle in a reproducible manner. The initial release is focused on text classification and regression models, with plans for future expansion. Code and documentation are available open-source at [https://explabox.readthedocs.io](https://explabox.readthedocs.io/en/stable).

# Statement of need

In high-stakes environments like law enforcement, machine learning (ML) models are subject to intense scrutiny and must comply with emerging regulations like the EU AI Act [@Edwards2022]. `Explabox` was developed to address the operational challenges of ML auditing at the Netherlands National Police, where models for text classification and regression require standardized, reproducible, and holistic evaluation to satisfy diverse stakeholders&mdash;from developers and internal auditors to legal and ethical oversight bodies. Existing tools, while powerful, were often fragmented, focusing on a single aspect of analysis (e.g., only explainability or testing) and lacking a unified framework for conducting a complete audit from data exploration to final reporting.

To solve this workflow problem, we developed Explabox around a four-step analysis strategy&mdash;*explore*, *examine*, *explain* and *expose*&mdash;inspired by similar conceptualizations of the analytical process [@Biecek2021]. While comprehensive libraries like `OmniXAI` [@Yang2022] offer a broad, multi-modal collection of explainers and `dalex` [@Baniecki2021] provides a mature, research-driven framework for model exploration, `Explabox` was developed to fill a specific operational gap. Practitioners seeking to conduct a full audit in a model-agnostic manner often have to combine multiple, highly-specialized libraries, such as `AIF360` [@Bellamy2018] for fairness metrics, `alibi explain` [@Klaise2021] or `AIX360` [@Arya2019] for local explanations, and `CheckList` [@Ribeiro2020] for behavioral testing.

This fragmentation introduces significant challenges, particularly regarding *reproducibility* and *flexibility in communicating results*. `Explabox` addresses the reproducibility challenge by providing a unified pipeline that not only offers centralized control over random seeds, but also tracks the specific data subsets and parameters used for each function call, ensuring full traceability. Furthermore, it provides flexibility through our *digestible* object system, which is designed to generate outputs tailored to diverse stakeholders. By integrating these critical components into a single, cohesive workflow, `Explabox` provides a practical framework that enhances the efficiency and methodological rigor of the ML auditing lifecycle, making it directly applicable to other high-stakes domains where model validation is critical, such as finance, healthcare, and law.

# Explore, Examine, Explain & Expose your ML models

`Explabox` transforms opaque *ingestibles* into transparent *digestibles* through four types of *analyses* to enhance explainability and aid fairness, robustness, and security audits.

## Ingestibles
Ingestibles provide a unified import interface for data and models, where layers abstract away access (\autoref{fig:layers}) to allow optimized processing. `Explabox` uses `instancelib` [@instancelib] for fast model and data encapsulation. The model can be any Python `Callable` containing a regression or (binary and multi-class) classification model. While this interface is model-agnostic, the current release provides data handling and analysis modules optimized specifically for text-based tasks. `scikit-learn` or `ONNX` models (e.g., `PyTorch`, `TensorFlow`, or `Keras`) import directly with optimizations and automatic input/output interpretation. Data can be automatically downloaded, extracted and loaded. Data inputs include `NumPy`, `Pandas`, `Hugging Face`, raw files (e.g., HDF5, CSV or TSV), and (compressed) file folders. Data can be subdivided into named splits (e.g., train-test-validation), and instance vectors and tokens can be precomputed and optionally saved for fast inferencing.

![Logical separation of `Explabox` into layers with interfaces.\label{fig:layers}](figure1.png){width=50%}

## Analyses

`Explabox` turns these *ingestibles* into *digestibles* (transparency-increasing information on ingestibles) through four *analyses* types: **explore**, **examine**, **explain** and **expose**.

**Explore** allows data slicing, dicing and sorting, and provides descriptive statistics (dataset sizes, label distributions, and text string/token lengths).

**Examine** shows model performance metrics, summarized in a table or shown graphically, with computation and interpretation references. For further analysis, **examine** also supports drilling down into (in)correct predictions.

**Explain** uses model-agnostic techniques [@Ribeiro2016b] to explain model behavior (*global*) and individual predictions (*local*). It summarizes model-labelled data, through prototypes (`K-Medoids`) or prototypes and criticisms (`MMDCritic` [@Kim2016]), and token distributions (`TokenFrequency`) and informativeness (`TokenInformation`). Local explanations use popular techniques: feature attribution scores (`LIME` [@Ribeiro2016a], `KernelSHAP` [@Lundberg2017]), feature subsets (`Anchors` [@Ribeiro2018]), local rule-based models (`LORE` [@Guidotti2018]), and counterfactual or contrastive explanations (`FoilTrees` [@Waa2018]). Built from generic components separating global and local explanation steps, these methods allow customization and enable scientific advances to be quickly integrated into operational processes (e.g., combine `KernelShap` sampling with `imodels` [@Singh2021] surrogate rules). Example configurations, such as `LIME` with default hyperparameters, ease adoption. **Explain** is provided by subpackage `text_explainability` [@text_explainability], which doubles as a standalone tool.

**Expose** gathers sensitivity insights via local and global testing regimes. These insights can be used to, through relevant attributes, assess the *robustness* (e.g., the effect of typos on model performance), *security* (e.g., if inputs containing certain characters crash the model), and *fairness* (e.g., subgroup performance for protected attributes such as country of origin, gender, race or socioeconomic status) of the model. Relevant attributes can either be observed in the current data or generated from user-provided templates [@Ribeiro2020] filled with multi-lingual data generation [@Faker]. These attributes are then either summarized in performance metrics, compared to expected behavior [@Ribeiro2020], or assessed with fairness metrics for classification [@Mehrabi2021] and regression [@Agarwal2019]. Like **explain**, **expose** is also made from generic components, which allows users to customize data generation and tests. **Expose** is provided by the `text_sensitivity` subpackage [@text_sensitivity], which also doubles as a standalone tool.

## Digestibles

Digestibles serve stakeholders&mdash;such as creators, auditors, applicants, end-users or clients [@Tomsett2018]&mdash;via a Jupyter Notebook or Web UI (\autoref{fig:ui}) (using `plotly` [@plotly] visuals), integrated API, and static reporting.

![UI elements from the Jupyter Notebook interface, designed to present audit results to diverse stakeholders.\label{fig:ui}](figure2.png)

# Acknowledgements

Development was supported by the Netherlands National Police. The authors thank contributors within the Police for development, testing, and usage, and participants from ICT.OPEN 2022, the UU NPAI, and UMC Utrecht demos for their valuable feedback.

# References
