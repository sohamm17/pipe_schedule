#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc

rm -rf normutil_*.txt multi_util_result.txt
# For pipelength of 3
python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 >/dev/null
./avg.sh normutil_3.txt >> multi_util_result.txt
rm -rf normutil_3.txt

python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -o 1 >/dev/null
./avg.sh normutil_3.txt >> multi_util_result.txt
rm -rf normutil_3.txt

python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -m 1 >/dev/null
./avg.sh normutil_3.txt >> multi_util_result.txt
rm -rf normutil_3.txt

python3 multi_pipeline.py -p 5 -t 3 -c 2 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 3 -c 4 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 3 -c 8 -r 10 -o 1 -m 1 >/dev/null
./avg.sh normutil_3.txt >> multi_util_result.txt
rm -rf normutil_3.txt

# For pipelength of 5
python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 >/dev/null
./avg.sh normutil_5.txt >> multi_util_result.txt
rm -rf normutil_5.txt

python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -o 1 >/dev/null
./avg.sh normutil_5.txt >> multi_util_result.txt
rm -rf normutil_5.txt

python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -m 1 >/dev/null
./avg.sh normutil_5.txt >> multi_util_result.txt
rm -rf normutil_5.txt

python3 multi_pipeline.py -p 5 -t 5 -c 2 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 5 -c 4 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 5 -c 8 -r 10 -o 1 -m 1 >/dev/null
./avg.sh normutil_5.txt >> multi_util_result.txt
rm -rf normutil_5.txt

# For pipelength of 10
python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 >/dev/null
./avg.sh normutil_10.txt >> multi_util_result.txt
rm -rf normutil_10.txt

python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 -o 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -o 1 >/dev/null
./avg.sh normutil_10.txt >> multi_util_result.txt
rm -rf normutil_10.txt

python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -m 1 >/dev/null
./avg.sh normutil_10.txt >> multi_util_result.txt
rm -rf normutil_10.txt

python3 multi_pipeline.py -p 5 -t 10 -c 2 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 10 -t 10 -c 4 -r 10 -o 1 -m 1 >/dev/null
python3 multi_pipeline.py -p 20 -t 10 -c 8 -r 10 -o 1 -m 1 >/dev/null
./avg.sh normutil_10.txt >> multi_util_result.txt
rm -rf normutil_10.txt
