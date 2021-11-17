#keys=('0xaa' '0x44' 'rand-0.10_0.90' 'rand-0.20_0.80' 'rand-0.30_0.70' 'rand-0.40_0.60' 'rand-0.50_0.50' 'rand-0.60_0.40' 'rand-0.70_0.30' 'rand-0.80_0.20' 'rand-0.90_0.10') 
keys=('window-4bit-v1' 'window-4bit-v2' 'window-4bit-v3' 'window-4bit-v4' 'window-4bit-v5' 'window-4bit-v6' 'window-4bit-v7' 'window-4bit-v8' 'window-4bit-v9' 'window-4bit-v10')
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

iters=1000

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
		
		if [ "$mode" == "simulate" ]; then
			command="cd $SIM_ROOT/uarch-leakage-detection; mkdir -p logs/"$suite"/"${app}"/"${iters}"/"${key}"; nohup ./scripts/do_simulation.sh $key $suite $app $iters > logs/$suite/$app/$iters/$key/launch_simulation.log 2>&1 &"
		
		elif [ "$mode" == "parse" ]; then
                	if [ "$suite" == "bearssl" ] && [ "$app" == "vuln" ]; then
				command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x0000011d4e 0x000001034c 0x0000011e1c 0x0000012318 ""'0x000001232e 0x0000012332""' $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
                	elif [ "$suite" == "openssl" ] && [ "$app" == "vuln" ]; then
   				command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x00000109ae 0x0000010168 0x0000010a88 0x0000010a8c 0x0000010adc $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
			elif [ "$app" == "consttime" ]; then
   				command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x0000011d4e 0x000001034c 0x0000011e1c 0x0000012318 0x000001233a $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
			elif [ "$app" == "dummy" ]; then
                                command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x0000011d4e 0x000001034c 0x0000011e1e 0x000001231a 0x0000011e22 $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
                        elif [ "$app" == "fixedwin_vuln" ]; then
                                command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x0000011d44 0x000001034c 0x0000011f0c 0x0000011f0e 0x0000011f1a $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
                        elif [ "$app" == "fixedwin_ct" ]; then
                                command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_parse.sh "${key}" 0x00000121a4 0x00000108f8 0x00000123b6 0x00000123ba 0x00000123dc $suite $app $iters > logs/$suite/$app/$iters/$key/launch_parse.log 2>&1 &"
                        fi

		elif [ "$mode" == "stats" ]; then
			command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_stats.sh "$key" "$suite" "$app" "$phi" "$alpha" "$window" "$iters" > logs/$suite/$app/$iters/$key/launch_stats.log 2>&1 &"
		fi

		echo "Launching "$app":"$key" on arch"$node""
		sshpass -p "pleasechangethispasswordasap" ssh -o StrictHostKeyChecking=no barberk@arch$node.cse.ohio-state.edu "$command"

	done
done
