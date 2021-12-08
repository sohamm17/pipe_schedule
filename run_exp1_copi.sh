#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
rm -rf accepted_sets_copi.txt
python3 copi_e2e.py -n 10 -x 1.1 >/dev/null
python3 copi_e2e.py -n 10 -x 1.2 >/dev/null
python3 copi_e2e.py -n 10 -x 1.4 >/dev/null
python3 copi_e2e.py -n 10 -x 1.5 >/dev/null
python3 copi_e2e.py -n 10 -x 1.6 >/dev/null
python3 copi_e2e.py -n 10 -x 1.8 >/dev/null
