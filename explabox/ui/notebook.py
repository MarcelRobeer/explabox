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

"""User interface for Jupyter notebook.

Attributes:
    MAIN_COLOR (str): Default color for the notebook UI.
    PACKAGE_LINK (str): URL to package.
    PACKAGE_NAME (str): Name of package.
"""

from functools import wraps
from typing import Callable

from genbase.ui.notebook import Render as GBRender
from genbase.ui.notebook import format_instances, format_list
from text_explainability.ui.notebook import Render as TERender
from text_explainability.ui.notebook import get_meta_descriptors
from text_sensitivity.ui.notebook import Render as TSRender
from text_sensitivity.ui.notebook import metrics_renderer

from ..utils import MultipleReturn

MAIN_COLOR = "#004682"
PACKAGE_LINK = "https://explabox.rtfd.io"
PACKAGE_NAME = "explabox"


class RestyleMixin:
    """Adds `self.restyle()` function to apply main_color and package_link."""

    def restyle(self):  # noqa: D102
        self.main_color = MAIN_COLOR
        self.package_link = PACKAGE_LINK
        self.package_name = PACKAGE_NAME
        self.default_title = "Digestible"


class GBRenderRestyled(GBRender, RestyleMixin):
    def __init__(self, *configs):
        """Restyle the `genbase` renderer."""
        super().__init__(*configs)
        self.restyle()


class TERenderRestyled(TERender, RestyleMixin):
    def __init__(self, *configs):
        """Restyle the `text_explainability` renderer."""
        super().__init__(*configs)
        self.restyle()


class TSRenderRestyled(TSRender, RestyleMixin):
    def __init__(self, *configs):
        """Restyle the `text_sensitivity` renderer."""
        super().__init__(*configs)
        self.restyle()


def format_table(header, content):
    """Format a HTML table based on header and content."""
    if isinstance(header, list):
        header = "".join(str(h) for h in header)
    if isinstance(content, list):
        content = "".join(str(c) for c in content)
    return f'<div class="table-wrapper"><table><tr>{header}</tr>{content}</table></div>'


def wrongly_classified_renderer(meta, content, **renderargs):
    """Rendered for `explabox.digestibles.WronglyClassified`."""
    html = ""

    for c in content["wrongly_classified"]:
        html += f'<h3>Should be <kbd>{c["ground_truth"]}</kbd> but predicted as <kbd>{c["predicted"]}</kbd>'
        html += f' (n={len(c["instances"])})</h3>'
        html += format_instances(c["instances"])
    return html


def dataset_renderer(meta, content, **renderargs):
    """Renderer for `explabox.digestibles.Dataset`."""
    instances = content.pop("instances", None)
    labels = content.pop("labels", None)

    kwargs = {}
    if labels is not None:
        kwargs["Annotated label"] = [f"<kbd>{next(iter(label))}</kbd>" for label in labels]

    html = format_instances(instances, **kwargs)
    return html


def descriptives_renderer(meta, content, **renderargs):
    """Renderer for `explabox.digestibles.Descriptives`."""
    labels = content["labels"]

    html = f"<h3>Labels ({len(labels)})</h3>"
    html += format_list(labels, format_fn="kbd")

    def fmt(x):
        if isinstance(x, float):
            x = round(x, 3)
        return f"<td>{x}</td>"

    html += "<h3>Label counts</h3>"
    label_counts = [
        "<tr>" + "".join(fmt(a) for a in [k] + [v[label] for label in labels]) + "</tr>"
        for k, v in content["label_counts"].items()
    ]
    html += format_table(
        ["<th>Split</th>"] + [f"<th><kbd>{label}</kbd></th>" for label in labels],
        label_counts,
    )

    html += "<h3>Tokenized lengths</h3>"
    metrics = list(list(content["tokenized_lengths"].values())[0].keys())
    tokenized_lengths = [
        "<tr>" + "".join(fmt(a) for a in [k] + [v[metric] for metric in metrics]) + "</tr>"
        for k, v in content["tokenized_lengths"].items()
    ]
    html += format_table(
        ["<th>Split</th>"] + [f"<th>{metric}</th>" for metric in metrics],
        tokenized_lengths,
    )

    return html


class Render(GBRenderRestyled):
    def __init__(self, *configs):
        """Custom renderer for `explabox`."""
        super().__init__(*configs)
        self.extra_css = """
        #--var(tabs_id) .table-wrapper td:nth-child(2),
        #--var(tabs_id) .table-wrapper th:nth-child(2) {
            width: auto;
        }
        #--var(tabs_id) kbd,
        p > kbd,
        h3 > kbd,
        table td > kbd {
            background-color: #333;
            border: 1px solid #fff;
            color: #fff;
            padding: 2px 4px;
        }
        #--var(tabs_id) ul > li:not(:last-child) {
           margin-bottom: 3px;
        }
        """

    def get_renderer(self, meta: dict):
        """Get a render function (Callable taking `meta`, `content` and `**renderargs` and returning a `str`).

        Args:
            meta (dict): Meta information to decide on appropriate renderer.
        """

        def default_renderer(meta, content, **renderargs):
            return f"<p>{content}</p>"

        type, _, _ = get_meta_descriptors(meta)

        if type == "dataset":
            return dataset_renderer
        elif type == "descriptives":
            return descriptives_renderer
        elif type == "model_performance":
            return metrics_renderer
        elif type == "wrongly_classified":
            return wrongly_classified_renderer

        return default_renderer

    def format_title(self, title: str, h: str = "h1", **renderargs) -> str:
        """Format title in HTML format.

        Args:
            title (str): Title contents.
            h (str, optional): h-tag (h1, h2, ...). Defaults to 'h1'.

        Returns:
            str: Formatted title.
        """
        return f'<{h}>{title.replace("_", " ").title()}</{h}>'

    def render_subtitle(self, meta: dict, content: dict, **renderargs) -> str:  # noqa: D102
        html = ""
        if "callargs" in meta and "split" in meta["callargs"] and isinstance(meta["callargs"]["split"], str):
            html += f'Digestible for split "{meta["callargs"]["split"]}".'

        return self.format_subtitle(html) if html else ""


def replace_renderer(res):
    """Replace a renderer from a function result with a restyled one."""
    if hasattr(res, "_renderer"):
        renderer = str(res._renderer).split("'")[1]
        if renderer.startswith("genbase"):
            res._renderer = GBRenderRestyled
        elif renderer.startswith("text_explainability"):
            res._renderer = TERenderRestyled
        elif renderer.startswith("text_sensitivity"):
            res._renderer = TSRenderRestyled
    return res


def restyle(function: Callable):
    """Apply a decorator for restyling the returned renderer."""

    @wraps(function)
    def inner(*args, **kwargs):
        res = function(*args, **kwargs)
        if isinstance(res, MultipleReturn):
            res.return_values = [replace_renderer(r) for r in res.return_values]
            return res
        return replace_renderer(res)

    return inner
