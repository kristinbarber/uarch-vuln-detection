import matplotlib.pyplot as plt 
import pickle
import sys
import re
from matplotlib import rcParams
from Microarchitecture import *

keyhex = open('scripts/keys/0xaa.key', 'r').read()
print(keyhex)
key = ''
for c in range(26): #100/8*2
    key += '{:04b}'.format(int(keyhex[c], 16))
print(key)
key = key[::-1]
print(len(key))
print(key)

app_names = ['vuln', 'dummy', 'consttime']
titles = ['(a)', '(b)', '(c)']
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12,8))

loop_timing = {}

for x in range(len(app_names)):
    loop_timing[x] = {'0': list(), '1': list()}
    instructions, loops, states = pickle.load(open('logs/bearssl/'+app_names[x]+'/0xaa/uarch.pickle', 'rb'))
    for j in range(len(loops)):
        loop_timing[x][key[j]].append(loops[j][-1].retire - loops[j][0].fetch)
    del instructions
    del loops
    del states

for x in range(len(app_names)):
    axs[x].hist([loop_timing[x]['1'], loop_timing[x]['0']], color=['blue', 'orange'], label=[r'$\theta_1$', r'$\theta_0$'], edgecolor='black')
    axs[x].set_xlabel('cycles', fontsize=14)
    axs[x].set_title(titles[x], fontsize=14)
axs[0].set_ylabel('No. Iterations', fontsize=14)

plt.tight_layout()
plt.subplots_adjust(top=0.9)
handles, titles = axs.flat[-1].get_legend_handles_labels()
fig.legend(handles, titles, loc='upper left', fancybox=True, shadow=True, ncol=3, mode='expand')

plt.savefig('logs/bearssl/timings.pdf', bbox_inches='tight')
