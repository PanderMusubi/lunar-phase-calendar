#!/usr/bin/env sh

echo '* CHECKBASISMS'
checkbashisms *.sh

FILES=*.py
echo '*PYDOCSTYLE'
pydocstyle --convention=numpy $FILES
echo '* FLAKE8'
flake8 --ignore E501 $FILES
echo '* PYLINT'
pylint $FILES
echo '* PYFLAKES'
pyflakes $FILES
echo '* MYPY'
mypy $FILES
