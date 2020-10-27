#!/bin/bash

#echo 'Compiling BOOM.....'
#make CONFIG=SmallBoomConfig
#mv simulator-chipyard-SmallBoomConfig simulator-chipyard-SmallBoomConfig-printall
echo 'Starting simulation....'
time $SIM_ROOT/simulator-chipyard-SmallBoomConfig-printall +verbose pk /home/barberk/local/bearssl-0.6/build/testcrypto-Os-$3-$1 modpow_i31_single > logs/$2/$3/$1/stdout.txt 2> logs/$2/$3/$1/out-all.log
cat logs/$2/$3/$1/out-all.log | spike-dasm > logs/$2/$3/$1/out-all-asm.log
