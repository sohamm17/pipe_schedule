#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 ilp/ilp_gekko.py -l 0.0 -e 15 -w 1 -b 1 >/dev/null
python3 ilp/ilp_gekko.py -l 0.25 -e 15 -w 1 -b 1 >/dev/null
python3 ilp/ilp_gekko.py -l 0.5 -e 15 -w 1 -b 1 >/dev/null
python3 ilp/ilp_gekko.py -l 0.75 -e 15 -w 1 -b 1 >/dev/null
