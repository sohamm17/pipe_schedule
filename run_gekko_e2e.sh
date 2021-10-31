#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 ilp/ilp_gekko.py -e 15 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 15 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 15 -w 0 >/dev/null
python3 ilp/ilp_gekko.py -e 15 -w 0 >/dev/null
