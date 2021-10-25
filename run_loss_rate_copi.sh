#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 opt_s2_lr.py -l 0 >/dev/null
python3 opt_s2_lr.py -l 0.25 >/dev/null
python3 opt_s2_lr.py -l 0.50 >/dev/null
python3 opt_s2_lr.py -l 0.75 >/dev/null
