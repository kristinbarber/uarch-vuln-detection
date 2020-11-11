import os
import pickle
import sys
import re
from Microarchitecture import *

diff_regex = re.compile('logs/bearssl/([a-z]+)/([x0-9a-z]+)/sets.pickle')
uarch_regex = re.compile('logs/bearssl/([a-z]+)/([x0-9a-z]+)/uarch.pickle')

blob = os.popen('ls -llarth logs/bearssl/'+sys.argv[1]+'/*/sets.pickle')
lines = blob.readlines()

diffs = {}
loop_states = {}
states = {}

for line in lines:
    fname = line.split(' ')[-1].strip()
    match = re.search(diff_regex, fname)
    key = match.group(2)
    print('Loading from '+fname+'...')
    loopsUArch, curated_states_bit1, curated_states_bit0, invariant_diff, curated_diff = pickle.load(open(fname, 'rb'))
    loop_states[key] = loopsUArch
    diffs[key] = curated_diff

blob = os.popen('ls -llarth logs/bearssl/'+sys.argv[1]+'/*/uarch.pickle')
lines = blob.readlines()
for line in lines:
    fname = line.split(' ')[-1].strip()
    match = re.search(uarch_regex, fname)
    key = match.group(2)
    print('Loading from '+fname+'...')
    instructions, loops, _states = pickle.load(open(fname, 'rb'))
    states[key] = _states 

"""for key in diffs:
    print(key)
    for component in diffs[key]:
        print(component)
        for state in diffs[key][component]:
            if component == Component.LQ:
                print(state.lq.__str__())
            elif component == Component.SQ:
                print(state.sq.__str__())
            elif component == Component.ROB:
               print(state.rob.__str__())
               continue
            elif component == Component.LFB:
              print(state.lfb.__str__())
            elif component == Component.HWPREFETCHER:
              print(state.hwprefetcher.__str__())
"""
diff_cnt = {}
diff_states = {}
key1 = '0x4f'
key2 = '0x7f'
for component in Component:
    diff_cnt[component] = 0
    diff_states[component] = []
    for loop in range(len(loopsUArch)-1):
        assert len(loop_states[key1][loop]) == len(loop_states[key2][loop])
        for idx in range(len(loop_states[key1][loop])-1):
            #assert loop_states[key1][loop][idx].cycle_begin == loop_states[key2][loop][idx].cycle_begin, 'key1='+key1+'; key2='+key2+'; loop='+str(loop)+'; idx='+str(idx)+'; component='+str(component)+'; cycle1='+str(loop_states[key1][loop][idx].cycle_begin)+'; cycle2='+str(loop_states[key2][loop][idx].cycle_begin)
            if not loop_states[key1][loop][idx].compare(component, loop_states[key2][loop][idx]):
                diff_cnt[component] = diff_cnt[component] + 1
                diff_states[component].append((loop, loop_states[key1][loop][idx], loop_states[key2][loop][idx]))

print(diff_cnt)

assert len(states[key1]) == len(states[key2])
for component in Component:
    diff_cnt[component] = 0
    diff_states[component] = []
    print('Analyzing component '+str(component))
    for idx in range(len(states[key1])-1):
        if not states[key1][idx].compare(component, states[key2][idx]):
            diff_cnt[component] = diff_cnt[component] + 1
            diff_states[component].append((states[key1][idx], states[key2][idx]))

print(diff_cnt)
