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

import os
import uuid

import pytest
from genbase import MetaInfo

from explabox.utils import MultipleReturn
from explabox.utils.io import create_output_dir

FOLDER = f"TEST-{uuid.uuid4()}"


class TestDigestible(MetaInfo):
    def __init__(type="test", **kwargs):
        """Empty digestible for testing."""
        super().__init__(type=type, **kwargs)

    @property
    def content(self):
        """Content."""
        return {}


def test_new_dir():
    """Test: Folder is created with `utils.io.create_output_dir()`."""
    assert not os.path.exists(FOLDER)
    create_output_dir(FOLDER)
    assert os.path.exists(FOLDER)
    os.rmdir(FOLDER)


def test_existing_dir():
    """Test: Folder still exists after recreating the directory."""
    os.mkdir(FOLDER)
    assert os.path.exists(FOLDER)
    create_output_dir(FOLDER)
    assert os.path.exists(FOLDER)
    os.rmdir(FOLDER)


@pytest.mark.parametrize("n", range(1, 5))
def test_multiple_return(n):
    """Test: Valid contents of `utils.MultipleReturn`."""
    digestible = MultipleReturn(*[TestDigestible() for _ in range(n)])
    assert len(digestible) == n
    assert isinstance(repr(digestible), str)
    assert isinstance(str(digestible), str)
    assert isinstance(digestible.raw_html, str)
    assert isinstance(digestible.html, str)
    assert isinstance(digestible.to_config(), dict if n == 1 else list)


def test_values_in_multiplereturn():
    """Test: Valid contents of `utils.MultipleReturn` with one element (html & raw_html have unique IDs)."""
    digestible = MultipleReturn(TestDigestible())
    assert digestible[0] == digestible.return_values[0]
    assert repr(digestible) == repr(digestible[0])
    assert str(digestible) == str(digestible[0])
    assert digestible.to_config() == digestible[0].to_config()
