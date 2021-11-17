#!/bin/bash
echo 'Parsing micro-arch log, collecting state samples...'
time python scripts/parse_trace.py logs/$7/$8/$9/$1/out-all-asm.log.gz logs/$7/$8/$9/$1/uarch.pickle $2 $3 $4 $5 "$6" > logs/$7/$8/$9/$1/parser.log 2>&1; echo `cat logs/$7/$8/$9/$1/parser.log` | mail -s 'parsing complete' barber.m.kristin@gmail.com 
