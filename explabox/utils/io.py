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

"""Utility functions for input/output behavior."""

from pathlib import Path

from ..config import OUTPUT_DIR


def create_output_dir(path: str = OUTPUT_DIR):
    """Create the directory to write results to.

    Args:
        path (str, optional): Path of the directory where to write any results to. Defaults to OUTPUT_DIR.
    """
    path = str(path)

    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"Output folder located at {str(OUTPUT_DIR)}")
