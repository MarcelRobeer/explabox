from configparser import ConfigParser
from distutils.util import convert_path
from os import path

import setuptools

main_ns = {}
with open(convert_path("explabox/_version.py")) as ver_file:
    exec(ver_file.read(), main_ns)  # nosec

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(
    path.join(path.abspath(path.dirname(__file__)), "requirements.txt"),
    encoding="utf-8",
) as f:
    requirements = f.read().splitlines()


cfg = ConfigParser()
cfg.read(path.join(path.abspath(path.dirname(__file__)), "tox.ini"))


def get_tox_reqs(keys):
    """Get requirements from `tox.ini`."""
    if isinstance(keys, str):
        keys = [keys]
    deps = []
    for key in keys:
        deps.extend(cfg.get(key, "deps").strip("\n").split("\n"))
    return list(set(deps))


extras = {}
extras["docs"] = [
    "m2r>=0.2.1",
    "sphinx>=4.1.1",
    "sphinx-autodoc-typehints>=1.17.0",
    "sphinxcontrib-apidoc>=0.3.0",
] + get_tox_reqs("testenv:doc8")
extras["quality"] = get_tox_reqs(
    ["testenv:black", "testenv:check-manifest", "testenv:doc8", "testenv:flake8", "testenv:isort"]
)
extras["test"] = get_tox_reqs("testenv")
extras["dev"] = list(set(extras["docs"] + extras["quality"] + extras["test"])) + ["make-to-batch>=0.2.3"]
extras["all"] = list(set([i for subi in extras.values() for i in subi]))


setuptools.setup(  # type: ignore
    name="explabox",
    version=main_ns["__version__"],
    description="Explore/examine/explain/expose your model with the explabox!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NPAI",
    license="GNU LGPL v3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    url="https://explabox.rtfd.io",
    packages=setuptools.find_packages(exclude=["test*.py"]),  # type : ignore
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.8",
)
