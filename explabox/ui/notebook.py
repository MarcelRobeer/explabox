"""User interface for Jupyter notebook."""

from genbase.ui.notebook import Render as GBRender
from text_explainability.ui.notebook import Render as TERender
from text_explainability.ui.notebook import get_meta_descriptors
from text_sensitivity.ui.notebook import Render as TSRender
from text_sensitivity.ui.notebook import metrics_renderer

from ..utils import MultipleReturn

MAIN_COLOR = "#004682"
PACKAGE_LINK = "https://git.science.uu.nl/m.j.robeer/explabox/"
PACKAGE_NAME = "explabox"


class RestyleMixin:
    """Adds `self.restyle()` function to apply main_color and package_link."""

    def restyle(self):
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


class Render(GBRenderRestyled):
    def __init__(self, *configs):
        """Custom renderer for `explabox`."""
        super().__init__(*configs)
        self.extra_css = """
        #--var(tabs_id) .table-wrapper td:nth-child(2),
        #--var(tabs_id) .table-wrapper th:nth-child(2) {
            width: auto;
        }
        """

    def get_renderer(self, meta: dict):
        """Get a render function (Callable taking `meta`, `content` and `**renderargs` and returning a `str`).

        Args:
            meta (dict): Meta information to decide on appropriate renderer.
        """

        def default_renderer(meta, content, **renderargs):
            return f"<p>{content}</p>"

        def descriptives_renderer(meta, content, **renderargs):
            return f"<p>{content}</p>"

        type, _, _ = get_meta_descriptors(meta)

        if type == "descriptives":
            return descriptives_renderer
        elif type == "model_performance":
            return metrics_renderer

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


def restyle(function):
    """Apply a decorator for restyling the returned renderer."""

    def inner(*args, **kwargs):
        res = function(*args, **kwargs)
        if isinstance(res, MultipleReturn):
            res.return_values = [replace_renderer(r) for r in res.return_values]
            return res
        return replace_renderer(res)

    return inner
