"""
 parse_trace.py: [trace_filename] [output_pickle_filename] [br_i31_modpow_begin] [main_end] [br_i31_modpow_call_ccopy_addr]
                 [ccopy_begin_addr] [ccopy_end_addr]
"""

import sys
import Instruction
import Microarchitecture
import re
import pickle
import collections


def get_iterations(instr_dict, lookbehind_pc, begin_pc, terminal_pcs):
    # 2D list of all instructions (retired and speculative) for each loop iterartion
    # Def: RoI; region of interest
    iterations = []
    roi = False
    last_inst_pc = ""
    for seqnum, instr in instr_dict.items():
        if instr.pc == begin_pc and instr.retire > 0:
            if last_inst_pc == lookbehind_pc:
                roi = True
                iterations.append([])
        elif instr.pc in terminal_pcs and instr.retire > 0:
            if roi:
                iterations[-1].append(instr)
                roi = False

        if roi:
            iterations[-1].append(instr)

        last_inst_pc = instr.pc

    return iterations 


cycleRegex = re.compile('Cycle=\s*([0-9]+)')
loadQueueEntry = re.compile('LoadQueueEntry\[([0-9 ]+)\]: PC:([0-9a-fx]+) \(([BHT ])\) Address:([0-9a-fx]+) \(([V-])\), TLBMiss:([TF-]), Uncacheable:([TF-]+), Executed:([TF-]+), Ignored:([TF-]+), Succeeded:([TF-]+), OrderFail:([TF-]+), Observed:([TF-]+), STList:([0-9a-fx]+), STIdx:([0-9a-fx]+), STForwValid:([TF-]), STForwIdx:([0-9a-fx]+) \[SN:([ 0-9]+)\]')
storeQueueEntry = re.compile('StoreQueueEntry\[([0-9 ]+)\]: PC:([0-9a-fx]+) \(([BHT ])\)\(([C\s])\)\(([E\s])\) Address:([0-9a-fx]+) \([V-]\), TLBMiss:[TF-], Data:([0-9a-fx]+), Committed:[TF-], Succeeded:[TF-] \[SN:([ 0-9]+)\]')
robEntry = re.compile('ROB\[([0-9 ]+)\]: ([BHT ]) (P| ) \(\((V|-)\)\((B|-)\)\((U|-)\) ([x0-9a-f]+) \[([a-z.0-9 ,()+-_]+)\] (E|-) \(d:[fCX-] p[0-9 ]+, bm:[0-9a-f ]+ sdt:[ 0-9]+\) \[SN:([ 0-9]+)\]')
lineFillBufferEntry = re.compile('LineBufferEntry \[([ 0-9]+)\] = ([0-9a-f]+)')
hwprefetchEntry = re.compile('Prefetcher: Address:([0-9a-fx]+) Data:([0-9a-fx]+)')
timestamp = re.compile('([0-9]+); O3PipeView:([a-z]+):\s+([0-9]+)(:([0-9xa-f]+):[0-9]+:\s+([0-9]+):([a-z0-9\-\.\s\(\)\,\-\+]+))?')

instructions = collections.OrderedDict() 
states = [] 

finName = sys.argv[1]
fout = sys.argv[2]
fin = open(finName, 'r')

print('begin_roi: '+sys.argv[3]+', end_roi: '+sys.argv[4]+', lookbehind_pc: '+sys.argv[5]+', begin_pc: '+sys.argv[6]+', terminal_pcs: '+sys.argv[7])

cycle = -1
curCycle = None
begin_roi = False
for line in fin:

    # Encountering an O3 timestamp
    if (match := re.search(timestamp, line)):
        seqnum = int(match.group(1))
        stage = match.group(2)
        cycle = int(match.group(3))
        pc = match.group(5)
        inst = match.group(7)     

        if stage == "fetch":
            if pc == sys.argv[3]:
                if not begin_roi:
                    begin_roi = True
            elif pc == sys.argv[4]:
                break 

            if begin_roi:
                instructions[seqnum] = Instruction.Instr(seqnum, pc, inst, cycle)

        elif begin_roi:
            if stage == "decode":
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

    if not begin_roi:
        continue

    # Encountered a new cycle, create UArch object and continue looping over lines in file
    # until finding another cycle marker
    elif (match := re.search(cycleRegex, line)):
        cycle = int(match.group(1))

        if curCycle is None:
            curCycle = Microarchitecture.UArch(cycle)
            continue
        else:
            curCycle.cycle_end = cycle
            assert len(curCycle.lfb.data) == 16
            #if len(states) == 0 or not curCycle == states[next(reversed(states))]:
            states.append(curCycle)

        curCycle = Microarchitecture.UArch(cycle)

    elif (match := re.search(loadQueueEntry, line)):
        idx = int(match.group(1))
        sn = int(match.group(17))
        pc = match.group(2)
        ptr = match.group(3)
        address = match.group(4)

        curCycle.lq.sn.append(sn)
        curCycle.lq.ptr.append(ptr)
        curCycle.lq.pc.append(pc)
        curCycle.lq.address.append(address)

        if idx == 7:
            try:
                curCycle.lq.setmetaData()
            except Exception as e:
                print(str(e) + 'LQ; Cycle='+str(curCycle.cycle_begin), file=sys.stderr)
                sys.exit()

    elif (match := re.search(storeQueueEntry, line)):
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
            try:
                curCycle.sq.setmetaData() 
            except Exception as e:
                print(str(e) + 'SQ; Cycle='+str(curCycle.cycle_begin), file=sys.stderr)
                sys.exit()

    elif (match := re.search(robEntry, line)):
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
            try:
                curCycle.rob.setmetaData()
            except Exception as e:
                print(str(e) + 'ROB; Cycle='+str(curCycle.cycle_begin), file=sys.stderr)
                sys.exit()

    elif (match := re.search(lineFillBufferEntry, line)):
        idx = int(match.group(1))
        data = match.group(2)

        curCycle.lfb.data.append(data)

    elif (match := re.search(hwprefetchEntry, line)):
        address = match.group(1)
        data = match.group(2)

        curCycle.hwprefetcher.address = address
        curCycle.hwprefetcher.data = data

loops = get_iterations(instructions, sys.argv[5], sys.argv[6], sys.argv[7])

with open(fout, 'wb') as f:
    pickle.dump((instructions, loops, states), f)

print('no. loops recorded: '+str(len(loops)))
print('Total no. uarch states collected: '+str(len(states)-1))
print('Total no. cycles in RoI: '+str(states[-1].cycle_begin - states[0].cycle_begin))
