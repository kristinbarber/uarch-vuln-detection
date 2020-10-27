#!/bin/bash

source ~/venv-py3.8.6/bin/activate
echo 'Running state analysis...'
time python scripts/parse_trace.py logs/$5/$6/$1/out-all-asm.log logs/$5/$6/$1/uarch.pickle $2 $3 "$4" 2> logs/$5/$6/$1/parser.log
time python scripts/stats.py logs/$5/$6/$1/uarch.pickle $1 logs/$5/$6/$1/sets.pickle > logs/$5/$6/$1/stats.log
