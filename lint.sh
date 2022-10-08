#!/usr/bin/env zsh
pre-commit run isort --files $@
pre-commit run black --files $@
pre-commit run flake8 --files $@
exit $?
