#!/bin/bash

set -o xtrace
set -e

awk '{s+=$1}END{print "",s/NR}' RS=" " $1
