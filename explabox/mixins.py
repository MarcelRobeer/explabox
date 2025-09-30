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

"""Extensions to classes."""


class ModelMixin:
    @property
    def is_classifier(self) -> bool:
        """Whether the included model is a classifier (True) or not (False)."""
        return "classifier" in str(self.model.__class__).lower()


class IngestiblesMixin:
    def check_requirements(self, elements=["data", "model"]) -> bool:
        """Check if the required elements are in the ingestibles.

        Args:
            elements (List[str], optional): Elements to check. Defaults to ['data', 'model'].

        Raises:
            ValueError: The required element is not in the ingestibles.

        Returns:
            bool: True if all requirements are included.
        """
        return self.ingestibles.check_requirements(elements)

    @property
    def data(self):
        """All data."""
        return self.ingestibles.data

    @property
    def labels(self):
        """Labelprovider."""
        return self.ingestibles.labels

    @property
    def labelset(self):
        """Names of labels."""
        return self.ingestibles.labelset

    @property
    def model(self):
        """Predictive model."""
        return self.ingestibles.model

    @property
    def splits(self):
        """Named splits."""
        return self.ingestibles.splits
