#!/bin/bash

checkbashisms *.sh
flake8 --ignore E501 *.py
pylint *.py
pyflakes *.py
mypy  *.py
