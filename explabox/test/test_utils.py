import os
import uuid

from explabox.utils.io import create_output_dir

FOLDER = f"TEST-{uuid.uuid4()}"


def test_new_dir():
    """Test: Folder is created with utils.io.create_output_dir()."""
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
