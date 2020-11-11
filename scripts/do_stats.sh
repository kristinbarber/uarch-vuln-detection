#!/bin/bash

source ~/venv-py3.8.6/bin/activate
echo 'Running state analysis....'
time python scripts/parse_trace.py logs/$7/$8/$1/out-all-asm.log logs/$7/$8/$1/uarch.pickle $2 $3 $4 $5 "$6" > logs/$7/$8/$1/parser.log
time python scripts/stats.py logs/$7/$8/$1/uarch.pickle scripts/keys/$1.key logs/$7/$8/$1/sets.pickle > logs/$7/$8/$1/stats.log
