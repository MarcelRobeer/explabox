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

"""Ingestibles are your model and data, which can be turned into digestibles that explore/examine/explain/expose
your data and/or model."""

from .data import import_data, rename_labels, train_test_split
from .ingestible import Ingestible
from .model import import_model

__all__ = ["Ingestible", "import_data", "import_model", "rename_labels", "train_test_split"]
