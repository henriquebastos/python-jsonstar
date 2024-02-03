#!/usr/bin/env zsh
source $VENV_BIN/activate
pre-commit run isort --files $@
pre-commit run black --files $@
pre-commit run flake8 --files $@
exit $?
