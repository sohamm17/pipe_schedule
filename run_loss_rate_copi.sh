#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 all_copi.py -l 0 >/dev/null
python3 copi_all.py.py -l 0.25 >/dev/null
python3 copi_all.py.py -l 0.50 >/dev/null
python3 copi_all.py.py -l 0.75 >/dev/null
