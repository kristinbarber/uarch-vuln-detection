import pickle, Instruction, Microarchitecture, sys, collections, re

finUarch = open(sys.argv[1], 'rb')
finKey = open('scripts/keys/'+sys.argv[2]+'.key', 'r')
foutSets = open(sys.argv[3], 'wb')
instructions, loops, stateDeltas = pickle.load(finUarch)

loopsIdx = []
loopsUArch = []
for x in range(len(loops)-1):
    assert loops[x][-1].retire > 0
 
    fetch = loops[x][0].fetch
    retire = loops[x][-1].retire
    idx_f = min(range(len(stateDeltas)), key=lambda i: abs(stateDeltas[i].cycle-fetch))
    idx_r = min(range(len(stateDeltas)), key=lambda i: abs(stateDeltas[i].cycle-retire))

    loopsIdx.append((idx_f, idx_r))
    loopsUArch.append(stateDeltas[idx_f:idx_r])


##  Collect common elements across rounds with the same key bit value
loop_bit1 = None 
loop_bit0 = None
key = finKey.read()
key = re.sub('\s+', '', key)
key = format(bin(int(key, 16)))[2:]
print (key)
for idx in range(len(loops)-1):
    if key[idx] == '1':
        if loop_bit1 == None:
            loop_bit1 = loopsUArch[idx]
        else:
            loop_bit1 = [state for state in loopsUArch[idx] if state in loop_bit1]
    elif key[idx] == '0':
        if loop_bit0 == None:
           loop_bit0 = loopsUArch[idx]
        else:
            loop_bit0 = [state for state in loopsUArch[idx] if state in loop_bit0]
    else:
        print ("Bit can only be '0' or '1', aborting...\n")
        sys.exit(1)

#Microarchitecture.UArch.recordStats = True
diff = [state for state in loop_bit1+loop_bit0 if (state not in loop_bit1) or (state not in loop_bit0)]
#print (Microarchitecture.UArch.stats)

print (len(loop_bit1))
print (len(loop_bit0))
print (len(diff))

for state in diff:
    print (state)

pickle.dump((loopsUArch, loop_bit1, loop_bit0, diff), foutSets)

#for state in loop_bit1:
#    print (state, file=sys.stdout)
#for state in loop_bit0:
#    print (state, file=sys.stderr)

#pyplot.hist(keyZero, label='k=0', alpha=0.5)
#pyplot.hist(keyOne, label='k=1', alpha=0.5)
#pyplot.legend(loc='best')
#pyplot.xlabel('br_ccopy() execution time (cycles)')
#pyplot.savefig(sys.argv[3])

#print(len(keyZero), len(keyOne))
#pyplot.plot(keyZero)
#pyplot.plot(keyOne)
#pyplot.savefig('line.pdf')

print ('done.')
