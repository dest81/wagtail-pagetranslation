# Wagtail pagetranslation

Allows to translate specific pages without replicating all wagtail pages tree structure.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/wagtail-pagetranslation.svg)](https://badge.fury.io/py/wagtail-pagetranslation)
[![pagetranslation CI](https://github.com/dest81/wagtail-pagetranslation/actions/workflows/test.yml/badge.svg)](https://github.com/dest81/wagtail-pagetranslation/actions/workflows/test.yml)
[![Code coverage](https://coveralls.io/repos/github/dest81/wagtail-pagetranslation/badge.svg?branch=main)](https://coveralls.io/github/dest81/wagtail-pagetranslation)
[![Downloads](https://img.shields.io/pypi/dm/fusion-engine?color=blue)](https://pypi.org/project/wagtail-pagetranslation/)

## Links
-   [Documentation](https://github.com/dest81/wagtail-pagetranslation/blob/main/README.md)
-   [Changelog](https://github.com/dest81/wagtail-pagetranslation/blob/main/CHANGELOG.md)
-   [Contributing](https://github.com/dest81/wagtail-pagetranslation/blob/main/CONTRIBUTING.md)
-   [Discussions](https://github.com/dest81/wagtail-pagetranslation/discussions)
-   [Security](https://github.com/dest81/wagtail-pagetranslation/security)

## Motivation

There are multiple approaches to localizing content on your Wagtail site. Solutions such as `wagtail-localize` rely on copying the entire page tree for each language, which can be inefficient. `wagtail-modeltranslation` requires a specific project structure and patches models on the fly, which can be risky. If all you need is to translate a few fields, this library is for you. Simply add TranslationMixin to the Page model, list the fields you want translated, and you're good to go.

## Installation

```sh
python -m pip install wagtail-pagetranslation
```

## How to use

Add "wagtail_pagetranslation" to list of applications after all wagtail apps

```python
INSTALLED_APPS = [
    "your_wagtail_app_1",
    "your_wagtail_app_2",
    ...
    "wagtail_pagetranslation",
    ...
]
```

Set default language for wagtail_pagetranslation app

```python
WAGTAIL_PAGETRANSLATION_DEFAULT_LANGUAGE = "en"
```

by default settings.LANGUAGES will be used

```python
LANGUAGES = [
    ("en", "English"),
    ("nl", "Dutch"),
    ("uk", "Ukrainian")
]
```

or you can specify custom list

```python
WAGTAIL_PAGETRANSLATION_LANGUAGES = [
    ("en", "English"),
    ("nl", "Dutch"),
    ("uk", "Ukrainian")
]
```

To make available translation per page type add TranslationMixin to your custom Page class.
**Note:** mixin should be added before Page class.

```python
from wagtail_pagetranslation.translation import TranslationMixin

class HomePage(TranslationMixin, Page):
    # list of fields that should have translation
    translatable_fields = ["title", ...]

```

By default URL for translated page is page url + `?lang=<lang_code>`
This can be change by overriding get_language method:

```python
from wagtail_pagetranslation.translation import TranslationMixin as BaseTranslationMixin

class TranslationMixin(BaseTranslationMixin):
    # list of fields that should have translation
    translatable_fields = ["title", ...]

    def get_language(self, request):
        return request.GET.get("language")

```

## Contributing

### Install

To make changes to this project, first clone this repository:

```sh
git clone https://github.com/dest81/wagtail-pagetranslation.git
cd wagtail-pagetranslation
```

With your preferred virtualenv activated, install testing dependencies:

#### Using pip

```sh
python -m pip install --upgrade pip>=21.3
python -m pip install -e '.[testing]' -U
```

#### Using flit

```sh
python -m pip install flit
flit install
```

### Pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit).
It is included in the project testing requirements. To set up locally:

```sh
# go to the project directory
cd wagtail-pagetranslation
# initialize pre-commit
pre-commit install

# Optional, run all checks once for this, then the checks will run only on the changed files
git ls-files --others --cached --exclude-standard | xargs pre-commit run --files
```

### How to run tests

Now you can run tests as shown below:

```sh
tox
```

or, you can run them for a specific environment `tox -e python3.11-django4.2-wagtail5.1`

To run the test app interactively, use `tox -e interactive`, visit `http://127.0.0.1:8020/admin/` and log in with `admin`/`changeme`.
