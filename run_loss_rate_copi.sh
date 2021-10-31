#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 copi_all.py -l 0 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.25 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.50 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.75 -n 10 -e 15 >/dev/null
