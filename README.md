# Microarchitectural Vulnerability Detection
This project investigates how best to utilize traces from pre-silicon simulation for vulnerability detection at the microarchitectural level of abstraction during the IC design life-cycle.  In particular, the analysis is focused on traces from executions of security critical applications in order to validate claims of properties enabling confidentiality protections.

The RISC-V BOOM processor released with the Chipyard framework from UC Berkeley is used as a testbed, along with cryptographic primitives from the BearSSL library as applications to study.

The tool has three stages: simulation, parsing and calculation of vulnerability metrics.

## Quick Start

The file <code>scripts/launch_runs.sh</code> is a job scheduling script for a local cluster. This can be used to launch multiple runs across nodes with SSH for the same application with different inputs (keys) and hardware design. This scripts calls <code>do_simulation.sh</code>, <code>do_parse.sh</code> and <code>do_stats.sh</code>. The script should be called three times to launch the simulation, parsing and stats collection phases. Below are some examples of its use:

1. <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic -appsi v2 -design baseline -mode ssh</code>   
    This will launch seperate simulations of the v2 application using each available key as input, defined in the <code>keys</code> array of <code>launch_runs.sh</code>.  
2. <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic -appsi v2 **-keysi 0xaa** -design baseline -mode ssh</code>   
    This will launch a simulation only for the 0xaa input  
3. <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic -appsi v2 -design baseline **-mode dryrun**</code>    
    Print the command that will be issued to the remote node over SSH, instead of running it  
    
Run this script with the same parameters replacing <code>**-action**</code> with <code>simulate</code>, <code>parse</code> and <code>stats</code> to complete the full analysis loop.  
To create CSV files to be feed into ML models use <code>scripts/generate_all_tables.sh</code>, which calls <code>scripts/generate_table.py<script>.</code>
    
### Debugging
There are other tools available to help with debugging and quickly finding information. The <code>pc_finder.py</code> script will locate the program counter (PC) values which lie on the boundaries of identified security-critical regions (SCRs). It takes SCR function names/labels as input.
Also, <code>inspect_instructions.py</code> can be helpful in an interactive python session to search the list of instructions fed into the pipeline and view the timestamps for which an instruction occupied various pipeline stages. If no timestamp is found for a particular stage, it means the instruction was speculative and squashed before entering that stage.


## Simulation

### Processor Simulator
The first stage is to simulate the processor-under-test, executing the selected application. We use the Verilator backend, which is a cycle-accurate C++ model of the hardware.

1. Clone the Chipyard repository from Github: <code>git clone https://github.com/ucb-bar/chipyard.git</code>
2. Checkout version 1.2.0: <code>git checkout tags/1.2.0</code>
3. Change the submodule path for the BOOM processor to point to our modified implementation:
    1. Open .gitmodules from the root directory of Chipyard
    2. Under <code>[submodule "generators/boom"]</code>, change to <code>url = https://github.com/kristinbarber/riscv-boom.git</code>
4. Follow instructions for repository initialization from Chipyard documentation
5. Checkout 'kmb' branch: <code>git checkout kmb</code>
6. Change to the <code>sims/verilator</code> directory
    1. Run <code>CONFIG=SmallBoomConfig</code>, this command will generate the simulator executable

### Applications
The <code>apps</code> directory holds respositories for tests to be run with the simulator.

We have created several unit tests based on the BearSSL library primitives that are intended to (1) ease use with the simulation platform, (2) exercise known vulnerabilities and (3) test the robustness of software mitigation techniques.
The unit tests can be found under <code>apps/bearssl-0.6/microsampler_tests</code> and can all be compiled using the provided Makefile. These tests take as input the secret key represented as a hexidecimal value and should be equal to the expected number of bytes (bits) for the cipher selected (e.g., 1024-bit for RSA (modpow)).

## State Construction
    
## Metric Calculation and Statistics Reporting

## Software Modules
