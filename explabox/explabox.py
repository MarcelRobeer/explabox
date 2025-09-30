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

"""Main Explabox class."""

from typing import Optional

from genbase import Readable, set_locale

from explabox.examine import Examiner
from explabox.explain import Explainer
from explabox.explore import Explorer
from explabox.expose import Exposer
from explabox.ingestibles import Ingestible
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
