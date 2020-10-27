###
### parse_trace.py: [trace_filename] [output_pickle_filename] [br_i31_modpow_call_ccopy_addr] [ccopy_begin_addr] [ccopy_end_addr] 
###

import sys, Instruction, Microarchitecture, re, pickle, collections

def getIterations(instList, lookbehind_pc, begin_pc, terminal_pcs):
    # 2D list of all instructions (retired and speculative) for each loop iterartion
    # Def: RoI; region of interest
    iterations = []
    RoI = False
    last_inst_pc = ""
    for instr in instList:
        if instr.pc == begin_pc and instr.retire > 0:
            if last_inst_pc == lookbehind_pc:
                RoI = True
                iterations.append([])
        elif instr.pc in terminal_pcs and instr.retire > 0:
            if RoI:
                iterations[-1].append(instr)
                RoI = False

        if RoI:
            iterations[-1].append(instr)

        last_inst_pc = instr.pc

    return iterations 

cycleRegex = re.compile('Cycle=\s*([0-9]+)')
loadQueueEntryRegex = re.compile('LoadQueueEntry\[([0-9 ]+)\]: PC:([0-9a-fx]+) \(([BHT ])\) Address:([0-9a-fx]+) \(([V-])\), TLBMiss:([TF-]), Uncacheable:([TF-]+), Executed:([TF-]+), Ignored:([TF-]+), Succeeded:([TF-]+), OrderFail:([TF-]+), Observed:([TF-]+), STList:([0-9a-fx]+), STIdx:([0-9a-fx]+), STForwValid:([TF-]), STForwIdx:([0-9a-fx]+) \[SN:([ 0-9]+)\]')
storeQueueEntryRegex = re.compile('StoreQueueEntry\[([0-9 ]+)\]: PC:([0-9a-fx]+) \(([BHT ])\)\(([C\s])\)\(([E\s])\) Address:([0-9a-fx]+) \([V-]\), TLBMiss:[TF-], Data:([0-9a-fx]+), Committed:[TF-], Succeeded:[TF-] \[SN:([ 0-9]+)\]')
robEntryRegex = re.compile('ROB\[([0-9 ]+)\]: ([BHT ]) (P| ) \(\((V|-)\)\((B|-)\)\((U|-)\) ([x0-9a-f]+) \[([a-z.0-9 ,()+-]+)\] (E|-) \(d:[fCX-] p[0-9 ]+, bm:[0-9a-f ]+ sdt:[ 0-9]+\) \[SN:([ 0-9]+)\]')
timestampRegex = re.compile('([0-9]+); O3PipeView:([a-z]+):\s+([0-9]+)(:([0-9xa-f]+):[0-9]+:\s+([0-9]+):([a-z0-9\-\.\s\(\)\,\-\+]+))?')

instructions = []
stateDeltas = []

finName = sys.argv[1]
fout = sys.argv[2]
fin = open(finName, 'r')

cycle = -1
curCycle = None
for line in fin:

    # Encountering an O3 timestamp
    if (match := re.search(timestampRegex, line)):
        seqnum = int(match.group(1))
        stage = match.group(2)
        cycle = int(match.group(3))
        pc = match.group(5)
        inst = match.group(7)     

        if stage == "fetch":
            instructions.append(Instruction.Instr(seqnum, pc, inst, cycle))
            assert len(instructions)-1 == int(seqnum), 'Assertion failed: '+str(len(instructions)-1)+' '+seqnum
        elif stage == "decode":
            instructions[seqnum].decode = cycle
        elif stage == "rename":
            instructions[seqnum].rename = cycle
        elif stage == "dispatch":
            instructions[seqnum].dispatch = cycle
        elif stage == "issue":
            instructions[seqnum].issue = cycle
        elif stage == "complete":
            instructions[seqnum].complete = cycle
        elif stage == "retire":
             instructions[seqnum].retire = cycle

    # Encountered a new cycle, create UArch object and continue looping over lines in file
    # until finding another cycle marker
    if (match := re.search(cycleRegex, line)):
        cycle = int(match.group(1))
        if curCycle is None:
            curCycle = Microarchitecture.UArch(cycle)
            continue
        elif len(stateDeltas) == 0 or curCycle != stateDeltas[-1]:
            stateDeltas.append(curCycle)

        curCycle = Microarchitecture.UArch(cycle)


    elif (match := re.search(loadQueueEntryRegex, line)):
        idx = int(match.group(1))
        sn = int(match.group(17))
        pc = match.group(2)
        ptr = match.group(3)
        address = match.group(4)

        curCycle.lq.sn.append(sn)
        curCycle.lq.ptr.append(ptr)
        curCycle.lq.pc.append(pc)
        curCycle.lq.address.append(address)
        #curCycle.lq.storeIdx.append(storeIdx) 

        if idx == 7:
            curCycle.lq.setmetaData()

    elif (match := re.search(storeQueueEntryRegex, line)):
        idx = int(match.group(1))
        sn = int(match.group(8))
        pc = match.group(2)
        ptr = match.group(3)
        address = match.group(6)

        curCycle.sq.sn.append(sn)
        curCycle.sq.ptr.append(ptr)
        curCycle.sq.pc.append(pc)
        curCycle.sq.address.append(address)

        if idx == 7:
            curCycle.sq.setmetaData() 

    elif (match := re.search(robEntryRegex, line)):
        idx = int(match.group(1))
        sn = int(match.group(10))
        ptr = match.group(2)
        pc = match.group(7)
        inst = match.group(8)

        curCycle.rob.sn.append(sn)
        curCycle.rob.ptr.append(ptr)
        curCycle.rob.pc.append(pc)
        curCycle.rob.inst.append(inst)

        if idx == 31:
            curCycle.rob.setmetaData()

loops = getIterations(instructions, sys.argv[3], sys.argv[4], sys.argv[5])

with open(fout, 'wb') as f:
   pickle.dump((instructions, loops, stateDeltas), f)

print('# loops recorded: '+str(len(loops)), file=sys.stderr)
print('Total cycles examined: '+str(cycle-stateDeltas[0].cycle)+'\n', file=sys.stderr)
print('Last cycle there was a change in uarch: '+str(stateDeltas[-1].cycle)+'\n', file=sys.stderr)
print('Total # of uarch state changes: '+str(len(stateDeltas))+'\n', file=sys.stderr)
