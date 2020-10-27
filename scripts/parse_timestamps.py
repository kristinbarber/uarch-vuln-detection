import re, sys, pickle, Instruction

#######
### parse_timestamps.py: [trace_filename] [output_pickle_filename] [br_i31_modpow_call_ccopy_addr] [ccopy_begin_addr] [ccopy_end_addr] 
######

instructions = [] 

regex = re.compile('([0-9]+); O3PipeView:([a-z]+):\s+([0-9]+)(:([0-9xa-f]+):[0-9]+:\s+([0-9]+):([a-z0-9\-\.\s\(\)\,\-\+]+))?')
fin = open(sys.argv[1], 'r')
fout = sys.argv[2]
terminal_pcs = sys.argv[5].split()

for line in fin:
    match = re.search(regex, line)
    if match:
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
loops = []
in_ccopy = False
last_inst_pc = ""
for instr in instructions:
    print (instr, file=sys.stderr)
    if instr.pc == sys.argv[4] and instr.retire > 0:
        if last_inst_pc == sys.argv[3]:
            in_ccopy = True
            loops.append([])
    elif instr.pc in terminal_pcs and instr.retire > 0:
        if in_ccopy:
            loops[-1].append(instr)
            in_ccopy = False

    if in_ccopy:
        loops[-1].append(instr)

    last_inst_pc = instr.pc

with open(fout, 'wb') as f:
   pickle.dump((instructions, loops), f)

print('# loops recorded: '+str(len(loops)), file=sys.stderr)
