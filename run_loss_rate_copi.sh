#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
rm -f accepted_lr_copi.txt accepted_time_lr.txt failed_time_lr.txt
python3 copi_all.py -l 0 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.25 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.50 -n 10 -e 15 >/dev/null
python3 copi_all.py -l 0.75 -n 10 -e 15 >/dev/null
