# types-boto3

[![PyPI - botocore-stubs](https://img.shields.io/pypi/v/botocore-stubs.svg?color=blue)](https://pypi.org/project/botocore-stubs)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/botocore-stubs.svg?color=blue)](https://pypi.org/project/botocore-stubs)
[![Docs](https://img.shields.io/readthedocs/boto3-stubs.svg?color=blue)](https://youtype.github.io/boto3_stubs_docs/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/botocore-stubs?color=blue)](https://pypistats.org/packages/botocore-stubs)

![boto3.typed](https://github.com/youtype/mypy_boto3_builder/raw/main/logo.png)

Proxy package for [boto3-stubs](https://pypi.org/project/boto3-stubs/).
Install submodules for `boto3` services type annotations.

Type annotations for
[botocore](https://github.com/boto/botocore)
compatible with
[VSCode](https://code.visualstudio.com/),
[PyCharm](https://www.jetbrains.com/pycharm/),
[Emacs](https://www.gnu.org/software/emacs/),
[Sublime Text](https://www.sublimetext.com/),
[mypy](https://github.com/python/mypy),
[pyright](https://github.com/microsoft/pyright)
and other tools.

See how it helps to find and fix potential bugs:

![boto3-stubs demo](https://github.com/youtype/mypy_boto3_builder/raw/main/demo.gif)

## How to install

### VSCode extension

Add [AWS Boto3](https://marketplace.visualstudio.com/items?itemName=Boto3typed.boto3-ide)
extension to your VSCode and run `AWS boto3: Quick Start` command.

### From PyPI with pip

Install `botocore-stubs` to add type annotations for `botocore` package.
Install `boto3-stubs` to add type annotations for `boto3` package.

```bash
# install type annotations only for botocore
python -m pip install botocore-stubs

# install type annotations only for boto3 and botocore
python -m pip install botocore-stubs boto3-stubs

# install `boto3` type annotations
# for ec2, s3, rds, lambda, sqs, dynamo and cloudformation
# Consumes ~7 MB of space
python -m pip install 'boto3-stubs[essential]'

# Lite version does not provide session.client/resource overloads
# it is more RAM-friendly, but requires explicit type annotations
python -m pip install 'boto3-stubs-lite[essential]'

# or install annotations for services you use
python -m pip install 'boto3-stubs[acm,apigateway]'
```

### From conda-forge

Installing `boto3-stubs` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Once the `conda-forge` channel has been enabled, `boto3-stubs` and `boto3-stubs-essential` can be installed with:

```bash
conda install boto3-stubs boto3-stubs-essential
```

It is possible to list all of the versions of `boto3-stubs` available on your platform with:

```bash
conda search boto3-stubs --channel conda-forge
```

## How to uninstall

```bash
# uninstall boto3-stubs
python -m pip uninstall -y boto3-stubs botocore-stubs

# uninstall submodules
python -m pip freeze | grep mypy-boto3 | xargs python -m pip uninstall -y
```

## Usage

### VSCode

- Install [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Install [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- Set `Pylance` as your Python Language Server
- Install `boto3-stubs` with services you use in your environment: `python -m pip install 'boto3-stubs[s3,ec2]'`

Both type checking and code completion should work for installed `boto3` services.
No explicit type annotations required, write your `boto3` code as usual.

### PyCharm

- Install `boto3-stubs-lite` with services you use in your environment:

```bash
python -m pip install 'boto3-stubs-lite[s3,ec2]'
```

Both type checking and code completion should work for installed services.
Explicit type annotations **are required**. Use `boto3-stubs` package instead for implicit type discovery.

### Emacs

- Install `boto3-stubs` with services you use in your environment: `python -m pip install 'boto3-stubs[s3,ec2]'`
- Install
  [use-package](https://github.com/jwiegley/use-package),
  [lsp](https://github.com/emacs-lsp/lsp-mode/),
  [company](https://github.com/company-mode/company-mode) and
  [flycheck](https://github.com/flycheck/flycheck) packages
- Install [lsp-pyright](https://github.com/emacs-lsp/lsp-pyright) package

```elisp
(use-package lsp-pyright
  :ensure t
  :hook (python-mode . (lambda ()
                          (require 'lsp-pyright)
                          (lsp)))  ; or lsp-deferred
  :init (when (executable-find "python3")
          (setq lsp-pyright-python-executable-cmd "python3"))
  )
```

- Make sure emacs uses the environment where you have installed `boto3-stubs`

### Sublime Text

- Install `boto3-stubs` with services you use in your environment: `python -m pip install 'boto3-stubs[s3,ec2]'`
- Install [LSP-pyright](https://github.com/sublimelsp/LSP-pyright) package
- Make sure emacs uses the environment where you have installed `boto3-stubs`

### Other IDEs

Not tested, but as long as your IDE supports `mypy` or `pyright`, everything should work.

### mypy

- Install `mypy`: `python -m pip install mypy`
- Install `boto3-stubs` with services you use in your environment: `python -m pip install 'boto3-stubs[s3,ec2]'`
- Run `mypy` as usual

Type checking should work for installed `boto3` services.
No explicit type annotations required, write your `boto3` code as usual.

### pyright

- Install `pyright`: `npm i -g pyright`
- Install `boto3-stubs` with services you use in your environment: `python -m pip install 'boto3-stubs[s3,ec2]'`
- Optionally, you can install `boto3-stubs` to `typings` folder.

Type checking should work for installed `boto3` services.
No explicit type annotations required, write your `boto3` code as usual.

## How it works

Fully automated [mypy-boto3-builder](https://github.com/youtype/mypy_boto3_builder) carefully generates
type annotations for each service, patiently waiting for `boto3` updates. It delivers
drop-in type annotations for you and makes sure that:

- All available `boto3` services are covered.
- Each public class and method of every `{{ package.library_name }}` service gets valid type annotations
  extracted from `botocore` schemas.
- Type annotations include up-to-date documentation.
- Link to documentation is provided for every method.
- Code is processed by [black](https://github.com/psf/black)
  and [isort](https://github.com/PyCQA/isort) for readability.

## What's new

### Implemented features

- Fully type annotated `boto3`, `botocore`, `aiobotocore` and `aioboto3` libraries
- `mypy`, `pyright`, `VSCode`, `PyCharm`, `Sublime Text` and `Emacs` compatibility
- `Client` type annotations for each service
- `ServiceResource` type annotations for each service
- `Resource` type annotations for each service
- `Waiter` type annotations for each service
- `Paginator` type annotations for each service
- Generated `TypeDefs` for each service
- Generated `Literals` for each service
- Auto discovery of types for `boto3.client` and `boto3.resource` calls
- Auto discovery of types for `session.client` and `session.resource` calls
- Auto discovery of types for `client.get_waiter` and `client.get_paginator` calls
- Auto discovery of types for `ServiceResource` and `Resource` collections

### Latest changes

Builder changelog can be found in [Releases](https://github.com/youtype/mypy_boto3_builder/releases).

## Versioning

`botocore-stubs` version is the same as related `botocore` version and follows
[PEP 440](https://www.python.org/dev/peps/pep-0440/) format.

## Thank you

- [Allie Fitter](https://github.com/alliefitter) for
  [boto3-type-annotations](https://pypi.org/project/boto3-type-annotations/),
  this package is based on top of his work
- [black](https://github.com/psf/black) developers for an awesome formatting tool
- [Timothy Edmund Crosley](https://github.com/timothycrosley) for
  [isort](https://github.com/PyCQA/isort) and how flexible it is
- [mypy](https://github.com/python/mypy) developers for doing all dirty work for us
- [pyright](https://github.com/microsoft/pyright) team for the new era of typed Python

## Documentation

All services type annotations can be found in [boto3-stubs docs](https://youtype.github.io/boto3_stubs_docs/)

## Support and contributing

This package is auto-generated. Please reports any bugs or request new features in
[mypy-boto3-builder](https://github.com/youtype/mypy_boto3_builder/issues/) repository.
