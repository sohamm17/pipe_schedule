#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc

rm -rf migrations_*.txt

python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -m 1 >/dev/null
./avg.sh migrations_2.txt >> migrations_result.txt
rm -rf migrations_2.txt

python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -m 1 -o 1 >/dev/null
./avg.sh migrations_2.txt >> migrations_result.txt
rm -rf migrations_2.txt

python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 -m 1 >/dev/null
./avg.sh migrations_4.txt >> migrations_result.txt
rm -rf migrations_4.txt

python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 -m 1 -o 1 >/dev/null
./avg.sh migrations_4.txt >> migrations_result.txt
rm -rf migrations_4.txt

python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -m 1 >/dev/null
./avg.sh migrations_8.txt >> migrations_result.txt
rm -rf migrations_8.txt

python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -m 1 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -m 1 -o 1 >/dev/null
./avg.sh migrations_8.txt >> migrations_result.txt
rm -rf migrations_8.txt
