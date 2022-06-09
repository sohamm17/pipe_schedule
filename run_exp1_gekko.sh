#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
rm -rf accepted_sets_gekko.txt failed_time_gekko.txt accepted_time_gekko.txt
python3 ilp/ilp_gekko.py -e 11 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 12 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 14 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 15 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 16 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 18 -w 0 >/dev/null
