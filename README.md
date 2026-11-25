# Digitalhub Installer

`digitalhub-installer` is a Python meta-package for installing the Digitalhub
SDK and its runtime extensions. It contains no importable modules or
installer-specific commands; its purpose is to declare the dependencies for
the selected installation tier.

## Installation

Install the SDK with its full optional dependencies:

```bash
pip install digitalhub-installer
```

Install the SDK and the basic runtime set (Python, Container, and Modelserve):

```bash
pip install "digitalhub-installer[basic]"
```

Install the SDK and all Digitalhub runtimes:

```bash
pip install "digitalhub-installer[all]"
```

The `all` extra includes the three basic runtimes plus DBT, Flower, Hera, Hydra,
Ray, Servicegraph, and TVM.

The package supports Python `>=3.10, <3.15`. Uninstalling this meta-package does
not automatically uninstall its dependencies.
