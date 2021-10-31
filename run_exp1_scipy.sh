#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 ilp/ilp_scipy.py -e 11 >/dev/null
python3 ilp/ilp_scipy.py -e 12 >/dev/null
python3 ilp/ilp_scipy.py -e 14 >/dev/null
python3 ilp/ilp_scipy.py -e 15 >/dev/null
python3 ilp/ilp_scipy.py -e 16 >/dev/null
python3 ilp/ilp_scipy.py -e 18 >/dev/null
