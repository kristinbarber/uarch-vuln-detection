keys=('0xaa' '0x44' '0x7f' '0x4f' 'rand0')
apps=('vuln' 'consttime')

snode=4

excluded_nodes=('11')

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
		-snode )
			shift
			snode=$1
			echo "start arch node: "$node""
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

                if [ "$app" == "vuln" ]; then
			command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_stats.sh "${key}" 0x0000024fcc 0x000001039a 0x000002509a 0x00000305b6 ""'0x00000305cc 0x00000305d0""' bearssl vuln > logs/bearssl/$app/$key/launch.log 2>&1 &"
			echo "Launching "$app":"$key" on arch"$node""
			sshpass -p "pleasechangethispasswordasap" ssh -o StrictHostKeyChecking=no barberk@arch$node.cse.ohio-state.edu "$command"

		elif [ "$app" == "consttime" ]; then
   			command="cd $SIM_ROOT/uarch-leakage-detection; nohup ./scripts/do_stats.sh "${key}" 0x0000024fcc 0x000001039a 0x000002509a 0x00000305b6 0x00000305d8 bearssl consttime > logs/bearssl/$app/$key/launch.log 2>&1 &"
                        echo "Launching "$app":"$key" on arch"$node""
                        sshpass -p "pleasechangethispasswordasap" ssh -o StrictHostKeyChecking=no barberk@arch$node.cse.ohio-state.edu "$command"
		else
			echo "Unknown application, exiting.."
			exit 1
		fi

	done
done
