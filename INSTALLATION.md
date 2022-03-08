# Installation
Installation of the `explabox` requires `Python 3.8` or higher.

### 1. Python installation
Install Python on your operating system using the [Python Setup and Usage](https://docs.python.org/3/using/index.html) guide.

### 2. Installing `explabox`
`explabox` can be installed:

* _using_ `pip`: `pip3 install` (released on [PyPI](https://pypi.org/project/explabox))
* _locally_: cloning the repository and using `python3 setup.py install`

#### Using `pip`
1. Open up a `terminal` (Linux / macOS) or `cmd.exe`/`powershell.exe` (Windows)
2. Run the command:
    - `pip3 install explabox`, or
    - `pip install explabox`.

```console
user@terminal:~$ pip3 install explabox
Collecting explabox
...
Installing collected packages: explabox
Successfully installed explabox
```

#### Locally
1. Download the folder from `GitLab/GitHub`:
    - Clone this repository, or 
    - Download it as a `.zip` file and extract it.
2. Open up a `terminal` (Linux / macOS) or `cmd.exe`/`powershell.exe` (Windows) and navigate to the folder you downloaded `explabox` in.
3. In the main folder (containing the `setup.py` file) run:
    - `python3 setup.py install`,
    - `python setup.py install`,
    - `pip3 install .` or,
    - `pip install .`

```console
user@terminal:~$ cd ~/explabox
user@terminal:~/explabox$ python3 setup.py install
running install
running bdist_egg
running egg_info
...
Finished processing dependencies for explabox
```
