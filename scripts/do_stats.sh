#!/bin/bash

echo 'Running state analysis....'
time python scripts/stats.py logs/$2/$3/$7/$1/uarch.pickle scripts/keys/$1.key logs/$2/$3/$7/$1/sets.pickle logs/$2/$3/$7/$1 $4 $5 $6 $7 > logs/$2/$3/$7/$1/stats-$4_$5.log 2>&1; echo `cat logs/$2/$3/$7/$1/stats-$4_$5.log` | mail -s 'stats collection complete' barber.m.kristin@gmail.com 
