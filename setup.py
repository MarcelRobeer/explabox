from distutils.util import convert_path
from os import path

import setuptools

main_ns = {}
with open(convert_path('explate/_version.py')) as ver_file:
    exec(ver_file.read(), main_ns)  # nosec

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setuptools.setup( # type: ignore
    name = 'explate',
    version = main_ns['__version__'],
    description = 'Let me explate your AI model!',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'NPAI',
    license = 'GNU LGPL v3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    url = 'https://git.science.uu.nl/m.j.robeer/explicate',
    packages = setuptools.find_packages(), # type : ignore
    install_requires = requirements,
    python_requires = '>=3.8',
)