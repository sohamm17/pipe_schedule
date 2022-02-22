#!/bin/bash

set -o xtrace
set -e

source ~/.bashrc
python3.6 waters.py -n 3 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 3 -x 1.75 -l 0.99 >/dev/null

echo "" >> accepted_waters_copi.txt
echo "" >> accepted_waters_avge2e.txt

python3.6 waters.py -n 5 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 5 -x 1.75 -l 0.99 >/dev/null

echo "" >> accepted_waters_copi.txt
echo "" >> accepted_waters_avge2e.txt

python3.6 waters.py -n 8 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 8 -x 1.75 -l 0.99 >/dev/null

echo "" >> accepted_waters_copi.txt
echo "" >> accepted_waters_avge2e.txt

python3.6 waters.py -n 10 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 10 -x 1.75 -l 0.99 >/dev/null

echo "" >> accepted_waters_copi.txt
echo "" >> accepted_waters_avge2e.txt

python3.6 waters.py -n 12 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 12 -x 1.75 -l 0.99 >/dev/null

echo "" >> accepted_waters_copi.txt
echo "" >> accepted_waters_avge2e.txt

python3.6 waters.py -n 15 -x 1.4 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.45 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.5 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.55 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.6 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.65 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.7 -l 0.99 >/dev/null
python3.6 waters.py -n 15 -x 1.75 -l 0.99 >/dev/null
