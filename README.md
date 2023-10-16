# Introduction
This repo is meant to serve as a boilerplate template for creating a new publishable Python package based on the latest best practices with project structure, documentation files, and CI/CD workflows already in place. The template has been set up with a basic "pure Python" package in mind, but everything can be easily extended for more complicated projects or to meet specific needs. It is designed to be minimal and doesn't have any external dependencies other than `pytest` for testing.

# Project Structure
This project template uses the "src layout" folder structure where package code would live in `src/packagename`. More information on the benefits of this layout can be found [here](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).

The `packagename` folder beneath `src` should be updated to the desired package name for your project. By default, this folder contains an empty `__init__.py` (making the directory importable) and empty `package.py` file. These can each be repurposed or deleted as needed for your specific project.

# Unit Testing
Unit tests should be created within the `tests` directory. This template assumes that `pytest` and `pytest-mock` will be used to run and drive unit testing. The `tests/data` directory is intended to be used with any data that might be needed for unit tests, such as mock API responses, etc.

# CI/CD
The template includes basic CI/CD tools and scripts to accomplish the following tasks:
- Run linting for syntax and code style/formatting.
- Run unit tests.
- Automatic management of version bumps, Github release creation, and publishing to PyPi.

## Python Scripts

Two Python scripts are available to manage releases and merges into `main`. Because they rely on the local user's ability to merge directly into `development` and `main`, they are better suited to small teams with "admin" repo maintainers who manually determine when to trigger releases.

`scripts/release.py` manages package versioning and the creation of a new release. This script should be called with a positional `type` argument of "major", "minor", or "patch" to determine the version bump that should be performed.
- Performs the appropriate version bump on `pyproject.toml` in `development`.
- Commits the change.
- Merges `development` into `main` and pushes.
- Creates a new repo tag based on the incremented version.
- Merges `main` into `development` so histories are fully synced.
- Workflows pick up after the script runs to generate the release.

`scripts/merge_without_release.py` merges `development` into `main` without triggering a release by enforcing a merge commit with the "skip release" message, which causes the release jobs to skip. This is useful for merging changes into `main` that don't necessarily need to trigger a new release such as updates to tests, docs, or workflows.
- Merges `development` into `main` with a "skip release" merge commit message.
- Merges `main` into `development` so histories are fully synced.

## Github Workflows

Two Github workflows are included to manage testing, linting, and automatic creation and publishing of releases.

`.github/workflows/lint_checks_and_tests.yml` runs lint checks and unit tests that runs on pushs to `main` or `development`, or on open pull requests into `development`. The workflow performs linting for syntax with `flake8` and for formatting using `Black`. Unit tests are run using `pytest` (`pytest-mock` is included in the dependency installation step if needed but can be removed).

`.github/workflows/release.yml` manages the automatic creation and publishing of releases that runs on successful completion of the `lint_checks_and_tests` workflow on `main`. The workflow will skip if "skip release" is found in the last commit message and will proceed otherwise. 

This workflow generates a changelog based on PR's merged between the last two more recent repo tags and categorizes PR's based on their labels. The format and categorization of the changelog is fully customizable within `changelog_configuration.json`. More information about how to customize this file can be found [here](https://github.com/mikepenz/release-changelog-builder-action#configuration-specification). Once the changelog is generated, the latest repo tag is pulled and used to create a release entry in Github. The changelog is passed into the release description.

Finally, a build is created and published to PyPi. This step uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) with PyPi, so no username, password, or long lived API tokens are needed. For this step to work, the project and trusted publishing settings must already be set up on PyPi.

# Building
Because this template assumes a simple "pure Python" type of package, only `pyproject.toml` is included to hold specific build metadata as per [PEP 621](https://peps.python.org/pep-0621/). This allows the package to be built using the `python -m build` command. The existing `pyproject.toml` file should be edited to suit your individual project needs. For more complicated builds, additional scripting (such as the traditional `setup.py`) can be added as needed.

# Documentation
Some empty documentation files (README.md and CHANGELOG.md) are included to be filled out with project specific information.

# Other Files
- The LICENSE file contains the Apache 2.0 license. The name of the copyright holder should be added to the bottom of the file if this license is used.
- The `.gitignore` file has been set up with some sensible defaults for a Python project.