#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -m 1 -o 1 >/dev/null
