#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 copi_e2e.py -n 3 -x 1.5 >/dev/null
python3 copi_e2e.py -n 5 -x 1.5 >/dev/null
python3 copi_e2e.py -n 7 -x 1.5 >/dev/null
python3 copi_e2e.py -n 10 -x 1.5 >/dev/null
python3 copi_e2e.py -n 13 -x 1.5 >/dev/null
python3 copi_e2e.py -n 15 -x 1.5 >/dev/null
