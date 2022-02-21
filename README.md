# pyproject-validate

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/ofek/pyproject-validate/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/pyproject-validate/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/pyproject-validate/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/pyproject-validate/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/pyproject-validate.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pyproject-validate/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyproject-validate.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/pyproject-validate/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyproject-validate.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/pyproject-validate/) |
| Meta | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |

-----

Validate and format `pyproject.toml` files.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Validators](#validators)
  - [Specs](#specs)
  - [Naming](#naming)
  - [Dependencies](#dependencies)
- [License](#license)

## Installation

```console
pip install pyproject-validate
```

## Usage

```console
usage: pyproject-validate [-h] [--fix] [--config CONFIG] [--version]

optional arguments:
  -h, --help       show this help message and exit
  --fix            whether to apply fixes for any encountered errors
  --config CONFIG  explicit path to the project config file
  --version        show program's version number and exit
```

## Validators

### Specs

Adhere to the data model defined by [PEP 517](https://www.python.org/dev/peps/pep-0517/#source-trees) and [PEP 621](https://www.python.org/dev/peps/pep-0621/#details).

### Naming

Ensure normalized project names.

Before:

```toml
[project]
name = "Foo.bAr"
```

After:

```toml
name = "foo-bar"
```

### Dependencies

Ensure normalized and sorted [PEP 508](https://www.python.org/dev/peps/pep-0508/) dependency definitions.

Before:

```toml
[project]
dependencies = [
    "python-dateutil",
    "bAr.Baz[TLS]   >=1.2RC5",
    'Foo;python_version<"3.8"',
]
```

After:

```toml
dependencies = [
    "bar-baz[tls]>=1.2rc5",
    "foo; python_version < '3.8'",
    "python-dateutil",
]
```

## License

`pyproject-validate` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
