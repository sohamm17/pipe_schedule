#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
rm accepted_multiproc_2_3.txt accepted_multiproc_2_5.txt accepted_multiproc_2_10.txt
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -m 1 -o 1 >/dev/null
