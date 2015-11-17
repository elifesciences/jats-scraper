#!/bin/bash
set -e
echo "running python tests"
./run-tests.sh
echo "...success! running article tests ..."
./article-test.sh
