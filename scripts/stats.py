import pickle
import sys
import re
from Microarchitecture import *

def find_index(lst, condition):
    idx = None
    for i, elem in enumerate(lst):
         if condition(elem):
             return i
    return idx

def uarch_diff(component, lst1, lst2):
    diff = []
    for state in lst1[component]:
        if not (sidx := find_index(lst2[component], lambda e: e.compare(component, state))):
            diff.append(state)
    for state in lst2[component]:
        if not (sidx := find_index(lst1[component], lambda e: e.compare(component, state))):
            diff.append(state)

    return diff

finUarch = open(sys.argv[1], 'rb')
finKey = open(sys.argv[2], 'r')
instructions, loops, states = pickle.load(finUarch)

key = finKey.read()
key = re.sub('\s+', '', key)
key = format(bin(int(key, 16)))[2:]
print(key)

loop_bit0_cnt = key[:len(loops)].count('0')
loop_bit1_cnt = key[:len(loops)].count('1')

loopsUArch = []
loop_unique_states = []
states_bit1 = {}
states_bit0 = {}
curated_states_bit1 = {}
curated_states_bit0 = {}
invariant_states_bit1 = {}
invariant_states_bit0 = {}
curated_diff = {}
invariant_diff = {}

# Cross-reference RoI from begin/end instructions with UArch objects
# for all cycles enclosed by the fetch/retire cycles for those RoI instructions.
print("Gathering loop state samples..")
for x in range(len(loops)-1):
    assert loops[x][-1].retire > 0

    fetch = loops[x][0].fetch
    retire = loops[x][-1].retire
    loopsUArch.append([state for state in states if state.cycle_begin >= fetch and state.cycle_begin <= retire])

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
        # We can say that, a state with a global tally >= 0.75 is representative of all iterations with k=1/0.
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


        else:
            print("Bit can only be '0' or '1', aborting...\n")
            sys.exit(1)

        del loop_unique_states[:]

    invariant_states_bit1[component] = [state[0] for state in states_bit1[component] if state[1]/loop_bit1_cnt == 1]    
    invariant_states_bit0[component] = [state[0] for state in states_bit0[component] if state[1]/loop_bit1_cnt == 1] 
    curated_states_bit1[component] = [state[0] for state in states_bit1[component] if state[1]/loop_bit1_cnt >= 0.87]
    curated_states_bit0[component] = [state[0] for state in states_bit0[component] if state[1]/loop_bit0_cnt >= 0.87]

    print("Finding different elements between iterations...")
    curated_diff[component] = uarch_diff(component, curated_states_bit1, curated_states_bit0) 
    invariant_diff[component] = uarch_diff(component, invariant_states_bit1, invariant_states_bit0)
                
    print(component)
    print()

    print('Counters for no. unique states')
    print([x[1] for x in states_bit1[component]])
    print([x[1] for x in states_bit0[component]])
    print('Invariant states')
    print(len(invariant_states_bit1[component]))
    print(len(invariant_states_bit0[component]))
    print('Curated states >= 0.87')
    print(len(curated_states_bit1[component]))
    print(len(curated_states_bit0[component]))
    print('Diff of invariants lists')
    print(len(invariant_diff[component]))
    print('Diff of curated lists')
    print(len(curated_diff[component]))


print('Size of the loop state lists')
print([len(loop) for loop in loopsUArch])
print('Counters for no. loops with each bit value')
print(loop_bit1_cnt)
print(loop_bit0_cnt)
print('no. cycles for each loop')
print([loop[-1].retire-loop[0].fetch for loop in loops])

with open(sys.argv[3], 'wb') as f:
    pickle.dump((loopsUArch, curated_states_bit1, curated_states_bit0, invariant_diff, curated_diff), f)

"""
pyplot.hist(keyZero, label='k=0', alpha=0.5)
pyplot.hist(keyOne, label='k=1', alpha=0.5)
pyplot.legend(loc='best')
pyplot.xlabel('br_ccopy() execution time (cycles)')
pyplot.savefig(sys.argv[3])

print(len(keyZero), len(keyOne))
pyplot.plot(keyZero)
pyplot.plot(keyOne)
pyplot.savefig('line.pdf')

"""

print('done.')
