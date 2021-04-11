#!/bin/bash

#echo 'Compiling BOOM.....'
#make CONFIG=SmallBoomConfig
#mv simulator-chipyard-SmallBoomConfig simulator-chipyard-SmallBoomConfig-printall
echo 'Starting simulation....'
keyval=`cat scripts/keys/$1.key`
time $SIM_ROOT/simulator-chipyard-SmallBoomConfig-printall +verbose $RISCV/riscv64-unknown-elf/bin/pk /home/barberk/local/bearssl-0.6/build/testcrypto-$3 $keyval > logs/$2/$3/$1/stdout.txt 2> logs/$2/$3/$1/out-all.log
cat logs/$2/$3/$1/out-all.log | spike-dasm > logs/$2/$3/$1/out-all-asm.log
gzip -f logs/$2/$3/$1/out-all-asm.log
rm logs/$2/$3/$1/out-all.log
