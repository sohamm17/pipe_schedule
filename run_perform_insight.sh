#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 copi_e2e.py -n 3 -x 1.1 >/dev/null
python3 copi_e2e.py -n 3 -x 1.2 >/dev/null
python3 copi_e2e.py -n 3 -x 1.3 >/dev/null
python3 copi_e2e.py -n 3 -x 1.4 >/dev/null
python3 copi_e2e.py -n 3 -x 1.5 >/dev/null
python3 copi_e2e.py -n 3 -x 1.6 >/dev/null
python3 copi_e2e.py -n 3 -x 1.7 >/dev/null
python3 copi_e2e.py -n 3 -x 1.8 >/dev/null

python3 copi_e2e.py -n 5 -x 1.1 >/dev/null
python3 copi_e2e.py -n 5 -x 1.2 >/dev/null
python3 copi_e2e.py -n 5 -x 1.3 >/dev/null
python3 copi_e2e.py -n 5 -x 1.4 >/dev/null
python3 copi_e2e.py -n 5 -x 1.5 >/dev/null
python3 copi_e2e.py -n 5 -x 1.6 >/dev/null
python3 copi_e2e.py -n 5 -x 1.7 >/dev/null
python3 copi_e2e.py -n 5 -x 1.8 >/dev/null

python3 copi_e2e.py -n 10 -x 1.1 >/dev/null
python3 copi_e2e.py -n 10 -x 1.2 >/dev/null
python3 copi_e2e.py -n 10 -x 1.3 >/dev/null
python3 copi_e2e.py -n 10 -x 1.4 >/dev/null
python3 copi_e2e.py -n 10 -x 1.5 >/dev/null
python3 copi_e2e.py -n 10 -x 1.6 >/dev/null
python3 copi_e2e.py -n 10 -x 1.7 >/dev/null
python3 copi_e2e.py -n 10 -x 1.8 >/dev/null

python3 copi_e2e.py -n 15 -x 1.1 >/dev/null
python3 copi_e2e.py -n 15 -x 1.2 >/dev/null
python3 copi_e2e.py -n 15 -x 1.3 >/dev/null
python3 copi_e2e.py -n 15 -x 1.4 >/dev/null
python3 copi_e2e.py -n 15 -x 1.5 >/dev/null
python3 copi_e2e.py -n 15 -x 1.6 >/dev/null
python3 copi_e2e.py -n 15 -x 1.7 >/dev/null
python3 copi_e2e.py -n 15 -x 1.8 >/dev/null

python3 copi_e2e.py -n 20 -x 1.1 >/dev/null
python3 copi_e2e.py -n 20 -x 1.2 >/dev/null
python3 copi_e2e.py -n 20 -x 1.3 >/dev/null
python3 copi_e2e.py -n 20 -x 1.4 >/dev/null
python3 copi_e2e.py -n 20 -x 1.5 >/dev/null
python3 copi_e2e.py -n 20 -x 1.6 >/dev/null
python3 copi_e2e.py -n 20 -x 1.7 >/dev/null
python3 copi_e2e.py -n 20 -x 1.8 >/dev/null
