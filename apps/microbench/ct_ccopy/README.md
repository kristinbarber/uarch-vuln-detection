
# Overview
With baremetal we don't have a way to pass input (keys). The key value needs to be hard-coded into the binary. That's why there is a binary for every key.
This is essentially running in M-mode with no kernel or runtime env.

The ct_ccopy test includes the constant-time copy primitive from BearSSL and calls it in a loop. Doing so mimics the way it would be used in the basic square-and-multiply algorithm.
This test also includes a warm-up phase to prime the caches, etc. Warm-up is acheived by performing the test twice, back-to-back. 

Trace recording (state sampling) should only begin after the test is executed the second time. This is done by including a marker to indicate the second test has started. The marker is a specific instruction encoding and the instruction is added into the test explicitly using in-line assembly (__asm__ directives). The special encoding to look for is 00008013 (the addi x0, x1, 0 instruction in RISC-V).


# Commands to Compile the Test for Baremetal

<code> riscv64-unknown-elf-gcc -Os -fno-inline -fno-common -fno-builtin-printf -specs=htif_nano.specs -c ct.c </code>
<code> riscv64-unknown-elf-gcc -Os -static -specs=htif_nano.specs ct.o -o ct_ccopy_bare </code>

## Debugging

<code> riscv64-unknown-elf-objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data ct_ccopy_bare > ct_ccopy_bare.dump </code>


## Adding Assembly Instructions

1. Run the assembler, edit the assembly (.S) file directly to insert desired instructions for flushing, etc.
<code> riscv64-unknown-elf-gcc -Os -fno-inline -fno-common -fno-builtin-printf -specs=htif_nano.specs -S -o ct.S ct.c </code>

2. Make edits, then
<code> riscv64-unknown-elf-as ct.S -o ct.o </code>
<code> riscv64-unknown-elf-gcc -Os -static -specs=htif_nano.specs ct.o -o ct_ccopy_bare </code>
