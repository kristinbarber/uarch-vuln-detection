#!/bin/bash

#echo 'Compiling BOOM.....'
#make CONFIG=SmallBoomConfig
#mv simulator-chipyard-SmallBoomConfig simulator-chipyard-SmallBoomConfig-printall
echo 'Starting simulation....'
keyval=`cat scripts/keys/$1.key`
if [ "$2" == "bearssl" ]; then
	if [ "$3" == "fixedwin_ct" ]; then 
		bin_args="$SIM_ROOT/uarch-leakage-detection/apps/bearssl-0.6/build/testcrypto $3 $keyval $4"
	else
		bin_args="$SIM_ROOT/uarch-leakage-detection/apps/bearssl-0.6/build/testcrypto-$3 $keyval"
	fi
elif [ "$2" == "openssl" ]; then
	bin_args="$HOME/local/openssl/test/microsampler_test/exptest $3 $keyval"
fi
time $SIM_ROOT/simulator-chipyard-SmallBoomConfig-printall +verbose $RISCV/riscv64-unknown-elf/bin/pk $bin_args > logs/$2/$3/$4/$1/stdout.txt 2> logs/$2/$3/$4/$1/out-all.log
cat logs/$2/$3/$4/$1/out-all.log | spike-dasm > logs/$2/$3/$4/$1/out-all-asm.log
gzip -f logs/$2/$3/$4/$1/out-all-asm.log
rm logs/$2/$3/$4/$1/out-all.log
echo `cat logs/$2/$3/$4/$1/stdout.txt` | mail -s 'simulation complete' barber.m.kristin@gmail.com 
