#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 copi_e2e.py -n 10 -x 1.3 >/dev/null
python3 copi_e2e.py -n 10 -x 1.35 >/dev/null
python3 copi_e2e.py -n 10 -x 1.4 >/dev/null
python3 copi_e2e.py -n 10 -x 1.45 >/dev/null
python3 copi_e2e.py -n 10 -x 1.5 >/dev/null
