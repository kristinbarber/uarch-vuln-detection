import os, sys, pickle, Microarchitecture

blob = os.popen('ls -llarth logs/bearssl/vuln/*/sets.pickle')
lines = blob.readlines()

diffs = []
comparison = None 
for line in lines:
    fname = line.split(' ')[-1].strip()
    print ('Processing state from '+fname+'...')
    loopsUarch, loop_bit1, loop_bit0, diff = pickle.load(open(fname, 'rb'))
    diffs.append(diff)

    if comparison == None:
        comparison = diff
    else:
        comparison = [state for state in diff if state in comparison]
    print (len(comparison))

print (len(comparison))

for state in comparison:
    print (state)

