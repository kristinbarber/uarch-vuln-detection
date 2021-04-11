#!/bin/bash

echo 'Running state analysis....'
time python scripts/stats.py logs/$2/$3/$1/uarch.pickle scripts/keys/$1.key logs/$2/$3/$1/sets.pickle logs/$2/$3/$1 $4 $5 > logs/$2/$3/$1/stats-$4_$5.log 2>&1
