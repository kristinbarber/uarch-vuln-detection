# Configuration for a native build on a generic Unix-like system.

# Build directory.
BUILD = build

# Extension for executable files.
E =

# Extension for object files.
O = .o

# Prefix for library file name.
LP = lib

# Extension for library file name.
L = .a

# Prefix for DLL file name.
DP = lib

# Extension for DLL file name.
D = .so

# Output file names can be overridden directly. By default, they are
# assembled using the prefix/extension macros defined above.
# BEARSSLLIB = libbearssl.a
# BEARSSLDLL = libbearssl.so
# BRSSL = brssl
# TESTCRYPTO = testcrypto
# TESTSPEED = testspeed
# TESTX509 = testx509

# File deletion tool.
RM = rm -f

# Directory creation tool.
MKDIR = mkdir -p

# C compiler and flags.
CC=riscv64-unknown-linux-gnu-gcc -Os
CFLAGS = --static
CCOUT = -c -o 

# Static library building tool.
AR = riscv64-unknown-linux-gnu-ar
ARFLAGS = -rcs
AROUT =

# DLL building tool.
LDDLL = $(CC)
LDDLLFLAGS =
LDDLLOUT = -o 

# Static linker.
LD = $(CC) 
LDFLAGS = --static 
LDOUT = -o 

# C# compiler; we assume usage of Mono.
MKT0COMP = mk$PmkT0.sh
RUNT0COMP = mono T0Comp.exe

# Set the values to 'no' to disable building of the corresponding element
# by default. Building can still be invoked with an explicit target call
# (e.g. 'make dll' to force build the DLL).
#STATICLIB = no
DLL = no
#TOOLS = no
#TESTS = no
