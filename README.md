# Django Template Project

Expected Python Version: 3.13.x

## Purpose

This project is intended as:

- a kick-off point for projects
- an evolving codebase which implements our best practices at the time
- a place where I can document decisions that have been made about practices
    - e.g.: why X was picked, why Y was avoided (+ pros & cons)

## Dependencies

To use this template and the resulting project, the only thing you need installed
initially is the Python package and project manager. [uv].

## Usage

Creating a new project from this template is done with the tool [cookiecutter]. The
simplest way to do this is to run it with [uvx], which comes with [uv].

```shell
uvx cookiecutter https://github.com/a-musing-moose/django_template.git
```

This will fetch the latest release of `cookiecutter`, download this template, and start
the project creation process. Cookiecutter will then guide you through the rest of the
process.

<!-- Links -->

[cookiecutter]: https://cookiecutter.readthedocs.io/en/stable/
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/
