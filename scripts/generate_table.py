import os
import pickle
import sys
import re
from Microarchitecture import *

diff_regex = re.compile('logs/bearssl/([a-z]+)/([\.\_\-x0-9a-z]+)/sets.pickle')

blob = os.popen('ls logs/bearssl/'+sys.argv[1]+'/*/sets.pickle')
traces = blob.readlines()
table = open('table-'+sys.argv[1]+'.csv', 'w+')

diffs = {}
testnames = {}
seckeybin = {}

for trace in traces:
    fname = trace.strip()
    match = re.search(diff_regex, fname)
    keystr = match.group(2)
    print('Loading from '+fname+'...')
    loopsUArch, theta_lst, diff, keybin = pickle.load(open(fname, 'rb'))
    testnames[keystr] = loopsUArch
    seckeybin[keystr] = keybin
    diffs[keystr] = diff

header = 'LQ-OCPNCY,LQ-PC,LQ-ADDR,SQ-OCPNY,SQ-PC,SQ-ADDR,ROB-OCPNY,ROB-PC,LFB-DATA,EUU-BITVEC,PREF-ADDR,PREF-DATA,CLASS,ITER,KEY' 
row = ''
table.write(header+'\n')
for keystr in testnames:
    for loop in range(len(testnames[keystr])):
        for state in testnames[keystr][loop]:
            row += str(state.lq.occupancy) + ','
            for x in range(8):
                try: row += str(hex(state.lq.pc[x])) + ','
                except: row += ','
            row = row[:-1] +','
            for x in range(8):
                try: row += str(hex(state.lq.address[x])) + ',' 
                except: row += ',' 
            row = row[:-1] +','
            row += str(state.sq.occupancy) + ','
            for x in range(8):
                try: row += str(hex(state.sq.pc[x])) + ',' 
                except: row += ',' 
            row = row[:-1] +','
            for x in range(8):
                try: row += str(hex(state.sq.address[x])) + ','
                except: row += ',' 
            row = row[:-1] +','
            row += str(state.rob.occupancy) + ','
            for x in range(32):
                try: row += str(hex(state.rob.pc[x])) + ',' 
                except: row += ',' 
            row = row[:-1] +','
            for x in range(16):
                try: row += str(hex(state.lfb.data[x])) + ',' 
                except: row += ',' 
            row = row[:-1] +','
            for x in range(4):
                try: row += str(state.executionUnitsBusy.reqs[x]) + ',' 
                except: row += ',' 
            row = row[:-1] +','
            row += hex(state.hwprefetcher.address) + ',' 
            row += hex(state.hwprefetcher.data) + ','
            row += seckeybin[keystr][loop] + ','
            row += str(loop) + ','
            row += keystr
            table.write(row+'\n')
            row = ''
