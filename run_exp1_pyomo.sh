#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
rm -rf accepted_sets_pyomo.txt
python3 ilp/ilp_pyomo.py -e 11 >/dev/null
python3 ilp/ilp_pyomo.py -e 12 >/dev/null
python3 ilp/ilp_pyomo.py -e 14 >/dev/null
python3 ilp/ilp_pyomo.py -e 15 >/dev/null
python3 ilp/ilp_pyomo.py -e 16 >/dev/null
python3 ilp/ilp_pyomo.py -e 18 >/dev/null
