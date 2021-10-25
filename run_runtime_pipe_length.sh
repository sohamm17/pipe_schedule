#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 runtime_measure.py -n 3 -x 1.5 >/dev/null
python3 runtime_measure.py -n 5 -x 1.5 >/dev/null
python3 runtime_measure.py -n 10 -x 1.5 >/dev/null
python3 runtime_measure.py -n 15 -x 1.5 >/dev/null
