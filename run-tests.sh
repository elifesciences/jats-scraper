#!/bin/bash
source install.sh > /dev/null
#pylint -E tests/*.py # disabled 2015-11-30, bug in pylint
python -m unittest discover --verbose --catch --start-directory tests/ --pattern "*.py"
