#!/bin/bash
set -e
rm -rf venv/
echo "running python tests"
./run-tests.sh
echo "...success! running article tests ..."
./article-test.sh
