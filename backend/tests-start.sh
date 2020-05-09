#! /usr/bin/env bash
set -e

python ./src/tests_pre_start.py

pytest $* ./src/tests/
