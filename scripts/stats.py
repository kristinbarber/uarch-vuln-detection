import matplotlib.pyplot as plt
import pickle
import sys
import re
from matplotlib import rcParams
from Microarchitecture import *

component_names = {Component.LQ: 'Load Queue', Component.SQ: 'Store Queue', Component.ROB: 'Reorder Buffer', Component.LFB: 'Line Fill Buffer', \
                   Component.HWPREFETCHER: 'Next-Line Hardware Prefetcher', Component.IPRF: 'Integer Register File', Component.FPRF: 'Floating-Point Register File', \
                   Component.EXESTATUS: 'Execution Unit Utilization'}

def uarch_diff(component, lst1, lst2, axs, _phi, _alpha):
    fout = open(sys.argv[4]+'/stats-'+str(component)+'.csv', 'w')
    x, y = [], [] 

    states = lst2[component][:]
    for state in lst1[component]:
        sidx = find_index(states, lambda e: e[0].compare(component, state[0]))
        if sidx is None:
            states.append(state)

    s = [x for x in range(len(states))]
    diff = list()
    for state in states:
        sidx1 = find_index(lst1[component], lambda e: e[0].compare(component, state[0]))
        sidx2 = find_index(lst2[component], lambda e: e[0].compare(component, state[0]))
     
        if sidx1 is None:
            x.append(0)
        else:
            x.append(lst1[component][sidx1][1])
        if sidx2 is None:
            y.append(0)
        else:
            y.append(lst2[component][sidx2][1])

        if sidx1 and sidx2 is None:
            if lst1[component][sidx1][1] >= _phi:
                diff.append(state[0])
        elif sidx2 and sidx1 is None:
            if lst2[component][sidx2][1] >= _phi:
                diff.append(state[0])
        elif sidx1 and sidx2:
            if (lst1[component][sidx1][1] >= _phi and lst2[component][sidx2][1] <= _alpha) or (lst2[component][sidx2][1] >= _phi and lst1[component][sidx1][1] <= _alpha):
                diff.append(state[0])
    
    fout.write('bit0,'+','.join(['{:.2f}'.format(n) for n in x])+'\n') 
    fout.write('bit1,'+','.join(['{:.2f}'.format(n) for n in y])+'\n')
    fout.close()

    if component != Component.FPRF and component != Component.IPRF:
        axs.flat[component.value].axhspan(_phi, 1, color='green', alpha=0.15, label=r'$\phi$')
        axs.flat[component.value].axhspan(0, _alpha, color='red', alpha=0.15, label=r'$\alpha$')
    #plt.ylabel('Iteration Frequency')
    #plt.xlabel('States')
        axs.flat[component.value].set_title(component_names[component])
        axs.flat[component.value].scatter([s[j] for j in range(len(x)) if x[j] > 0.0], [x[j] for j in range(len(x)) if x[j] > 0.0], facecolors='none', color='blue', label='e=1')
        axs.flat[component.value].scatter([s[j] for j in range(len(y)) if y[j] > 0.0], [y[j] for j in range(len(y)) if y[j] > 0.0], marker='x', color='darkorange', label='e=0')
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.savefig(sys.argv[4]+'/stats-'+str(component)+'.pdf')

    return diff

finUarch = open(sys.argv[1], 'rb')
finKey = open(sys.argv[2], 'r')
instructions, loops, states = pickle.load(finUarch)
_phi = float(sys.argv[5])
_alpha = float(sys.argv[6])
print('phi: {}, alpha: {}'.format(_phi, _alpha))

keyhex = finKey.read()
print(keyhex)
key = ''
for c in range(26): #100/8*2
    key += '{:04b}'.format(int(keyhex[c], 16))
print(key)
key = key[::-1]
print(len(key))
print(key)

loop_bit0_cnt = key.count('0')
loop_bit1_cnt = key.count('1')

loopsUArch = []
loop_unique_states = []
states_bit1 = {}
states_bit0 = {}
diff = {}

# Cross-reference RoI from begin/end instructions with UArch objects
# for all cycles enclosed by the fetch/retire cycles for those RoI instructions.
print("Gathering loop state samples..")
for x in range(len(loops)-1):
    assert loops[x][-1].retire > 0

    fetch = loops[x][0].fetch
    retire = loops[x][-1].retire
    loopsUArch.append([state for state in states if state.cycle_begin >= fetch and state.cycle_begin <= retire])

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Verdana']
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(15,6))

for component in Component:
    #  Collect common elements across rounds with the same key bit value
    states_bit1[component] = []
    states_bit0[component] = []
    print("Finding unique and common elements for "+str(component))
    for idx in range(len(loops)-1):
        # For each UArch state object associated with the current loop iteration...
        for state in loopsUArch[idx]:
            # If this state object differs from any of the state objects we have seen so far,
            # in terms of the given 'component', add it to the list of unqiue state objects encountered for that component.
            # This is accomplished by comparing the equivalence criterion for 'component' with all of the 
            # previously collected state objects for that component. 'sidx' indicates if a match was found for an "equivalent" state,
            # and a tally is updated to reflect how many repititions of the given (component,state) have been seen for this iteration.
            sidx = find_index(loop_unique_states, lambda e: e[0].compare(component, state))
            if sidx is None:
                loop_unique_states.append([state, 1])
            else:
                loop_unique_states[sidx][1] = loop_unique_states[sidx][1] + 1
        # Now, update global tallies in states_bit1/0 for all unique states, with respect to 'component',
        # across all iterations. The tally per state must be <= 100, as there are 100 rounds being analyzed,
        # and is performed seperately for rounds with k=0 and k=1.
        # State tallies > 1 indicate that a given state is found in more than one iteration.
        # When comparing state across rounds with k=1/0, we may want to consider all states where
        # the tally count among iterations is beyond a certain threshold, say 75%.
        # We can say that, a state with a global tally >= 0.90 is representative of all iterations with k=1/0.
        if key[idx] == '1':
             for state in loop_unique_states:
                sidx = find_index(states_bit1[component], lambda e: e[0].compare(component, state[0]))
                if sidx is None:
                    states_bit1[component].append([state[0], 1])
                else:
                    states_bit1[component][sidx][1] = states_bit1[component][sidx][1] + 1

        elif key[idx] == '0':
            for state in loop_unique_states:
                sidx = find_index(states_bit0[component], lambda e: e[0].compare(component, state[0]))
                if sidx is None:
                    states_bit0[component].append([state[0], 1])
                else:
                    states_bit0[component][sidx][1] = states_bit0[component][sidx][1] + 1

        del loop_unique_states[:]

    for state in states_bit1[component]:
        state[1] = state[1]/loop_bit1_cnt
    for state in states_bit0[component]:
        state[1] = state[1]/loop_bit0_cnt

    diff[component] = uarch_diff(component, states_bit1, states_bit0, axs, _phi, _alpha)
                
    print(component)
    print()

    print('Unique states for bit 1')
    print(len(states_bit1[component]))
    for state in states_bit1[component]:
        print(state[1])
        print(state[0])

    print('Unique states for bit 0')
    print(len(states_bit0[component]))
    for state in states_bit0[component]:
        print(state[1])
        print(state[0])

    print("Diff of states")
    print(len(diff[component]))

    for state in diff[component]:
        print(state)


for i, row in enumerate(axs):
    for j, cell in enumerate(row):
        if i == len(axs) - 1:
            cell.set_xlabel("States")
        if j == 0:
            cell.set_ylabel("Iteration Frequency")
plt.tight_layout()
plt.subplots_adjust(top=0.9)
handles, labels = axs.flat[-1].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left', fancybox=True, shadow=True, ncol=4, mode='expand')
plt.savefig(sys.argv[4]+'/stats.pdf', bbox_inches='tight')

print('Size of the loop state lists')
print([len(loop) for loop in loopsUArch])
print('Counters for no. loops with each bit value')
print(loop_bit1_cnt)
print(loop_bit0_cnt)
print('no. cycles for each loop')
print([loop[-1].retire-loop[0].fetch for loop in loops])

print(sum([len(loopsUArch[idx]) for idx in range(len(loops)-1) if key[idx] == '1'])/loop_bit1_cnt)
print(sum([len(loopsUArch[idx]) for idx in range(len(loops)-1) if key[idx] == '0'])/loop_bit0_cnt)

for component in Component:
    print(str(component)+','+ \
          str(len(states_bit1[component]))+','+ \
          str(len(states_bit0[component]))+','+ \
          str(len([x for x in states_bit1[component] if x[1] >= _phi]))+','+ \
          str(len([x for x in states_bit0[component] if x[1] >= _phi]))+','+ \
          str(len([x for x in states_bit1[component] if x[1] <= _alpha]))+','+ \
          str(len([x for x in states_bit0[component] if x[1] <= _alpha]))+','+ \
          str(len(diff[component])))

with open(sys.argv[3], 'wb') as f:
    pickle.dump((loopsUArch, states_bit1, states_bit0, diff), f)

print('done.')
