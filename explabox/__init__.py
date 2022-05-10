"""The Explabox aims to support data scientists and machine learning (ML) engineers in explaining, testing and
documenting AI/ML models, developed in-house or acquired externally. The explabox turns your ingestibles (AI/ML model
and/or dataset) into digestibles (statistics, explanations or sensitivity insights)!

To install run:
    $ pip3 install explabox

Currently, the main interface for working with the Explabox is Jupyter Notebook. For more help, read the documentation
at https://explabox.rtfd.io.

Explabox is developed by the Dutch National Police Lab AI (NPAI), and released under the GNU Lesser General Public
License v3.0 (GNU LGPLv3).
"""

from typing import Optional

from genbase import Readable, get_locale, set_locale

from explabox._version import __version__, __version_info__
from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.expose import Exposer
from explabox.ingestibles import Ingestible, import_data, import_model, rename_labels, train_test_split
from explabox.mixins import IngestiblesMixin


class Explabox(Readable, IngestiblesMixin):
    def __init__(self, ingestibles: Optional[Ingestible] = None, locale: str = "en", **kwargs):
        """Use the Explabox to `.explore`, `.examine`, `.expose` and `.explain` your AI model.

        Example:
            >>> from explabox import Explabox
            >>> box = Explabox(data=data, model=model)

        Args:
            ingestibles (Optional[Ingestible], optional): Ingestibles (data and model). Defaults to None.
            locale (str, optional): Language of dataset. Defaults to 'en'.
            **kwargs: Arguments used to construct an Ingestible (if the ingestibles argument is None).
        """
        if ingestibles is None:
            ingestibles = Ingestible(**kwargs)
        self.ingestibles = ingestibles
        self.check_requirements(["data", "model"])

        set_locale(locale)

        self.examine = Examiner(ingestibles=self.ingestibles)
        self.explore = Explorer(ingestibles=self.ingestibles)
        self.expose = Exposer(ingestibles=self.ingestibles)
        self.explain = Explainer(ingestibles=self.ingestibles)
