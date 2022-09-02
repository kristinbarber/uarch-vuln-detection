
# Overview
With baremetal we don't have a way to pass input (keys). The key value needs to be hard-coded into the binary. That's why there is a binary for every key.

# Commands to Compile the Test for Baremetal (M-mode, no kernel or runtime env)

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
