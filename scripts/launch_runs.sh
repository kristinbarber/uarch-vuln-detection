keys=('0xaa' '0x44' 'rand-0.10_0.90' 'rand-0.20_0.80' 'rand-0.30_0.70' 'rand-0.40_0.60' 'rand-0.50_0.50' 'rand-0.60_0.40' 'rand-0.70_0.30' 'rand-0.80_0.20' 'rand-0.90_0.10') 
#keys=('window-4bit-v1' 'window-4bit-v2' 'window-4bit-v3' 'window-4bit-v4' 'window-4bit-v5' 'window-4bit-v6' 'window-4bit-v7' 'window-4bit-v8' 'window-4bit-v9' 'window-4bit-v10')
#'rand-0.10_0.90' 'rand-0.10_0.90.v1' 'rand-0.10_0.90.v2' 'rand-0.10_0.90.v3' 'rand-0.10_0.90.v4' 'rand-0.10_0.90.v5' 'rand-0.10_0.90.v6' 'rand-0.10_0.90.v7' 'rand-0.10_0.90.v8' 'rand-0.10_0.90.v9'
#'rand-0.20_0.80' 'rand-0.20_0.80.v1' 'rand-0.20_0.80.v2' 'rand-0.20_0.80.v3' 'rand-0.20_0.80.v4' 'rand-0.20_0.80.v5' 'rand-0.20_0.80.v6' 'rand-0.20_0.80.v7' 'rand-0.20_0.80.v8' 'rand-0.20_0.80.v9'
#'rand-0.30_0.70' 'rand-0.30_0.70.v1' 'rand-0.30_0.70.v2' 'rand-0.30_0.70.v3' 'rand-0.30_0.70.v4' 'rand-0.30_0.70.v5' 'rand-0.30_0.70.v6' 'rand-0.30_0.70.v7' 'rand-0.30_0.70.v8' 'rand-0.30_0.70.v9' 
#keys=('rand-0.40_0.60' 'rand-0.40_0.60.v1' 'rand-0.40_0.60.v2' 'rand-0.40_0.60.v3' 'rand-0.40_0.60.v4' 'rand-0.40_0.60.v5' 'rand-0.40_0.60.v6' 'rand-0.40_0.60.v7' 'rand-0.40_0.60.v8' 'rand-0.40_0.60.v9')
#keys=('rand-0.50_0.50' 'rand-0.50_0.50.v1' 'rand-0.50_0.50.v2' 'rand-0.50_0.50.v3' 'rand-0.50_0.50.v4' 'rand-0.50_0.50.v5' 'rand-0.50_0.50.v6' 'rand-0.50_0.50.v7' 'rand-0.50_0.50.v8' 'rand-0.50_0.50.v9')
#'rand-0.60_0.40' 'rand-0.60_0.40.v1' 'rand-0.60_0.40.v2' 'rand-0.60_0.40.v3' 'rand-0.60_0.40.v4' 'rand-0.60_0.40.v5' 'rand-0.60_0.40.v6' 'rand-0.60_0.40.v7' 'rand-0.60_0.40.v8' 'rand-0.60_0.40.v9'
#keys=('rand-0.70_0.30' 'rand-0.70_0.30.v1' 'rand-0.70_0.30.v2' 'rand-0.70_0.30.v3' 'rand-0.70_0.30.v4' 'rand-0.70_0.30.v5' 'rand-0.70_0.30.v6' 'rand-0.70_0.30.v7' 'rand-0.70_0.30.v8' 'rand-0.70_0.30.v9')
#'rand-0.80_0.20' 'rand-0.80_0.20.v1' 'rand-0.80_0.20.v2' 'rand-0.80_0.20.v3' 'rand-0.80_0.20.v4' 'rand-0.80_0.20.v5' 'rand-0.80_0.20.v6' 'rand-0.80_0.20.v7' 'rand-0.80_0.20.v8' 'rand-0.80_0.20.v9'
#'rand-0.90_0.10' 'rand-0.90_0.10.v1' 'rand-0.90_0.10.v2' 'rand-0.90_0.10.v3' 'rand-0.90_0.10.v4' 'rand-0.90_0.10.v5' 'rand-0.90_0.10.v6' 'rand-0.90_0.10.v7' 'rand-0.90_0.10.v8' 'rand-0.90_0.10.v9' 

suite='bearssl'
apps=('vuln' 'dummy' 'consttime')

snode=4

excluded_nodes=('10' '11' '12')

phi=".90"
alpha=".10"
window="1"
design="baseline"

iters=100

echo "#####################"
while [ "$1" != '' ]; do
	case $1 in
                -mode )
                        shift
                        mode=$1
                        echo "mode: "$mode
                        ;;  
		-keysi )
			shift
			keys=($1)
			;;
		-suite )
			shift
			suite=$1
			;;
		-appsi )
			shift
			apps=($1)
			;;
		-iters )
			shift
			iters=$1
			;;
		-snode )
			shift
			snode=$1
			echo "start arch node: "$snode""
			;;
		-phi )
			shift
			phi=$1
			;;
		-alpha )
			shift
			alpha=$1
			;;
		-window )
			shift
			window=$1
			;;
		-design )
			shift
			design=$1
			;;
	esac
	shift
done
echo "#####################"

node=$snode

if [ "$mode" == "kill" ]; then
        echo "Killing all processes..."
        while [ "$node" -lt 13 ]; do
                echo "node $node"
                command="pkill -u barberk"
                sshpass -p "pleasechangethispasswordasap" ssh -o StrictHostKeyChecking=no barberk@arch$node.cse.ohio-state.edu "$command"
                let node++
                until [[ ! " ${excluded_nodes[@]} " =~ " ${node} " ]]
                do
                    let node++
                done
        done
        exit 1
fi

for app in "${apps[@]}"
do
	for key in "${keys[@]}"
	do
                let node++
		until [[ ! " ${excluded_nodes[@]} " =~ " ${node} " ]]
		do
			let node++
		done
		if [ "$node" -gt 12 ]; then
			node=$snode
		fi
	
		command="cd $SIM_ROOT/uarch-leakage-detection; "
		if [ "$mode" == "simulate" ] || [ "$mode" == "all" ]; then
			command+="mkdir -p logs/"$design"/"$suite"/"$app"/"$iters"/"$key"; nohup ./scripts/do_simulation.sh "$key" "$suite" "$app" "$iters" "$design" > logs/"$design"/"$suite"/"$app"/"$iters"/"$key"/launch_simulation.log 2>&1 &"
		fi
		
		if [ "$mode" == "parse" ] || [ "$mode" == "all" ]; then
			command+="nohup ./scripts/do_parse.sh "$key 
			if [ "$suite" == "microbench" ] && [ "$app" == "bad_ccopy_bare" ]; then
				command+=" 0x00800000ce 0x00800001e2 0x008000013e 0x0080000142 0x00800001d4 "
			elif [ "$suite" == "microbench" ] && [ "$app" == "ct_ccopy_bare" ]; then
				command+=" 0x008000010e 0x0080000124 0x0080000196 0x0080000130 0x008000019a "
			elif [ "$suite" == "microbench" ] && [ "$app" == "ct_ccopy_bare_nops" ]; then
				command+=" 0x0080000126 0x0080000146 0x0080000208 0x0080000160 0x008000020c "
			elif [ "$suite" == "microbench" ] && [ "$app" == "ct_ccopy_bare_nops_fence" ]; then
				command+=" 0x0080000126 0x0080000146 0x008000020c 0x0080000160 0x0080000210 "
			elif [ "$suite" == "microbench" ] && [ "$app" == "ct_ccopy_bare_double_fence" ]; then
				command+=" 0x0080000126 0x0080000146 0x0080000210 0x0080000160 0x0080000214 "
                	elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "vuln_warmup" ]; then
				command+=" 0x00000103a0 0x00000103a4 0x00000108a4 0x00000104d6 0x00000108a8 "
                	elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "vuln" ]; then
   				command+=" 0x000001037e 0x0000010382 0x0000010884 0x00000104b6 0x0000010888 "
                	elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "vuln_fence" ]; then
				command+=" 0x000001037e 0x0000010382 0x0000010956 0x00000104b6 0x000001095a "
                	elif [ "$suite" == "bearssl_comb" ] && [ "$app" == "vuln_warmup" ]; then
   				command+=" 0x0000010726 0x000001072a 0x0000012218 0x0000012fcc 0x000001221c "
                	elif [ "$suite" == "bearssl_comb" ] && [ "$app" == "vuln" ]; then
				command+=" 0x00000106e8 0x00000106ec 0x000001215c 0x0000012f10 0x0000012160 "  
                	elif [ "$suite" == "bearssl_single" ] && [ "$app" == "vuln" ]; then
				command+=" 0x00000105a4 0x00000105a8 0x0000011e1c 0x0000012318 0x0000011e20 " 
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "consttime" ]; then
   				command+=" 0x000001037e 0x0000010382 0x00000107b6 0x00000104c6 0x00000107ba "
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "consttime_warmup" ]; then
				command+=" 0x00000103a0 0x00000103a4 0x00000107d6 0x00000104e6 0x00000107da "
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "consttime_fence" ]; then
				command+=" 0x000001037e 0x0000010382 0x000001088a 0x00000104c6 0x000001088e "  
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "dummy_warmup" ]; then
				command+=" 0x00000103a8 0x00000103ac 0x0000010a58 0x00000104c8 0x0000010a5c "
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "dummy" ]; then
				command+=" 0x0000010382 0x0000010386 0x0000010a34 0x00000104a4 0x0000010a38 "
			elif [ "$suite" == "bearssl_synthetic" ] && [ "$app" == "dummy_fence" ]; then
				command+=" 0x0000010382 0x0000010386 0x0000010b10 0x00000104a4 0x0000010b14 " 
                	elif [ "$suite" == "bearssl_comb" ] && [ "$app" == "dummy" ]; then
				command+=" 0x00000107bc 0x00000107c0 0x000001222c 0x0000012efa 0x0000012230 "
                	elif [ "$suite" == "bearssl_single" ] && [ "$app" == "dummy" ]; then
				command+=" 0x00000105a4 0x00000105a8 0x0000011e1e 0x000001231a 0x0000011e22 "
                        elif [ "$app" == "fixedwin_ct" ]; then
                                command+=" 0x0000010864 0x0000010756 0x0000012532 0x0000012534 0x0000012540 "
                       fi

			command+=$suite" "$app" "$iters" "$design" > logs/"$design"/"$suite"/"$app"/"$iters"/"$key"/launch_parse.log 2>&1 &"
		fi

		if [ "$mode" == "stats" ] || [ "$mode" == "all" ]; then
			command+="nohup ./scripts/do_stats.sh "$key" "$suite" "$app" "$phi" "$alpha" "$window" "$iters" "$design" > logs/"$design"/"$suite"/"$app"/"$iters"/"$key"/launch_stats.log 2>&1 &"
		fi

		echo "Launching "$design":"$app":"$key" on arch"$node""
		#echo $command
		sshpass -p "pleasechangethispasswordasap" ssh -o StrictHostKeyChecking=no barberk@arch$node.cse.ohio-state.edu "$command"

	done
done
