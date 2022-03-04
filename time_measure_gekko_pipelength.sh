#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 ilp/ilp_gekko.py -n 3 -e 4.5 >/dev/null
python3 ilp/ilp_gekko.py -n 5 -e 7.5 >/dev/null
python3 ilp/ilp_gekko.py -n 7 -e 10.5 >/dev/null
python3 ilp/ilp_gekko.py -n 10 -e 15 >/dev/null
python3 ilp/ilp_gekko.py -n 13 -e 19.5 >/dev/null
python3 ilp/ilp_gekko.py -n 15 -e 22.5 >/dev/null
