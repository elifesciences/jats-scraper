#!/bin/bash
source install.sh > /dev/null
pylint -E elife_ga_metrics/*.py elife_ga_metrics/test/*.py
python -m unittest discover --verbose --catch --start-directory tests/ --pattern "*.py"
