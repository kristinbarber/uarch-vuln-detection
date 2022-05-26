#!/bin/bash

declare -a apps=("vuln" "vuln_warmup" "vuln_fence" "dummy" "dummy_warmup" "dummy_fence" "consttime" "consttime_warmup" "consttime_fence")

for val in "${apps[@]}"; do
	python3 scripts/generate_table.py $val $2 $1
	echo 'Finished with table for '$val
done
