# Copyright (C) 2021-2022 National Police Lab AI (NPAI).
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

"""Utility functions and classes."""

from .io import create_output_dir


class MultipleReturn:
    """Holds multiple return values (e.g. from `return_types`) in one iterable return value."""

    def __init__(self, *return_values):
        self.return_values = return_values

    def _repr_html_(self):
        return "".join(v._repr_html_() for v in self.return_values)

    def __repr__(self):
        return ", ".join(v.__repr__() for v in self.return_values)

    def __str__(self):
        return ", ".join(v.__str__() for v in self.return_values)

    def __getitem__(self, i):
        return self.return_values[i]

    def __len__(self):
        return len(self.return_values)

    def to_config(self):
        if len(self.return_values) == 1:
            return self.return_values[0].to_config()
        return [v.to_config() for v in self.return_values]
