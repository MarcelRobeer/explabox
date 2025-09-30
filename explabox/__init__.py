# Copyright (C) 2022 Marcel Robeer for National Police Lab AI (NPAI).
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

from genbase import get_locale, set_locale

from explabox._version import __version__, __version_info__
from explabox.examine import Examiner
from explabox.explabox import Explabox
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.expose import Exposer
from explabox.ingestibles import Ingestible, import_data, import_model, rename_labels, train_test_split

__all__ = [
    "Explabox",
    "Examiner",
    "Explainer",
    "Explorer",
    "Exposer",
    "Ingestible",
    "get_locale",
    "import_data",
    "import_model",
    "rename_labels",
    "set_locale",
    "train_test_split",
    "__version__",
    "__version_info__",
]
