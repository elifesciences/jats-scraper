#!/bin/bash
source install.sh > /dev/null
pylint -E tests/*.py
python -m unittest discover --verbose --catch --start-directory tests/ --pattern "*.py"
