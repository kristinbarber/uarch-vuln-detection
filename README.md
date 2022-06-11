# Microarchitectural Vulnerability Detection
This project investigates how best to utilize traces from pre-silicon simulation for vulnerability detection at the microarchitectural level of abstraction during the IC design life-cycle.  In particular, the analysis is focused on traces from executions of security critical applications in order to validate claims of properties enabling confidentiality protections.

The RISC-V BOOM processor released with the Chipyard framework from UC Berkeley is used as a testbed, along with cryptographic primitives from the BearSSL library as applications to study.

The tool has three stages: simulation, parsing and calculation of vulnerability metrics.

## Quick Start

Run <code>make</code> in <code>apps/bearssl-0.6/microsampler_tests</code> to compile all the tests.

The file <code>scripts/launch_runs.sh</code> is a job scheduling script for a local cluster. This can be used to launch multiple runs across nodes using SSH of the same application, selecting different inputs (keys) and hardware designs. This script is simply a helper-wrapper which then executes <code>do_simulation.sh</code>, <code>do_parse.sh</code> and <code>do_stats.sh</code> followed by <code>parse_trace.py</code> and <code>stats.py</code>, respectively.
The script should be called three times to launch the simulation, parsing and stats collection phases. Below are some examples of its use:  
> <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic -appsi v2 -design baseline -mode ssh</code>    

This will launch seperate simulations of the v2 application using each available key as input, defined in the <code>keys</code> array of <code>launch_runs.sh</code>

> <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic  **-appsi "v1 v2 v3"**  **-keysi 0xaa** -design baseline -mode ssh</code> 
   
This will launch a simulation only for the 0xaa input, for three applications (v1, v2 & v3)

> <code>./scripts/launch_runs.sh -action simulate -suite bearssl_synthetic -appsi v2 -design baseline **-mode dryrun**</code> 

Print the command that will be issued to the remote node over SSH, instead of running it

### General Steps

1. Set <code>SIM_ROOT</code> environment variable to point to the root directory of this repository
2. Set <code>USER</code> and <code>PASSWD_FILE</code> fields in launcher script. <code>PASSWD_FILE</code> is the name of a plain-text file containing the password to be used by SSH for node login. This should be created/kept in the root directory of this repo.
3. Launch runs with the procedure outlined above. Select suite, design, application(s) and key(s) using script parameters. This sets off simulations of all permutations from those selected. Once a set of parameters is selected, call script replacing <code>**-action**</code> with <code>simulate</code>, <code>parse</code> and <code>stats</code> to complete the full analysis loop.  The statistics reporting done corresponds to the analysis described in our Computer Architecture Letters publication, [A Pre-Silicon Approach to Discovering Microarchitectural Vulnerabilities in Security Critical Applications].
4. To create CSV files of uarch trace data as input to ML models use <code>scripts/generate_all_tables.sh</code>, passing the design and suite names. Columnar tables for each application,keys will be generated from this pair. The file will be placed under the <code>data</code> directory. An example:
   > <code> ./scripts/generate_all_tables.sh baseline bearssl_synthetic </code>

### Adding a Test
1. Add an application test by first compiling it with the riscv cross-compiler toolchain (within Chipyard install)
    1. Taking a look at the Makefile under <code>apps/bearssl-0.6/microsampler_tests</code> for examples
3. Using <code>objdump</code>, inspect the disassembly to identify security-critical regions of interest
4. Make note of program counter values associated with the starting and ending points of these regions
5. Enter PC values into launcher script under parsing section for each test, these are consulted during state sample creation
    1. There are five PC values which need to be entered: (a) state sample record begin, (b) state sample record end, (c) caller of SCR, (d) SCR callee, (e) SCR return
   
### Adding a Key
To execute tests using a new key, a plain-text file must be created under <code>scripts/keys/</code> with the value of the key in hexidecimal. This is used to pass the key to the simulator.
    
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
5. Checkout branch for the baseline design with Microsampler tracing: <code>git checkout baseline</code>
6. Change to the <code>sims/verilator</code> directory
    1. Run <code>CONFIG=SmallBoomConfig</code>, this command will generate the simulator executable

### Applications
The <code>apps</code> directory holds respositories for tests to be run with the simulator.

We have created several unit tests based on the BearSSL library primitives that are intended to (1) ease use with the simulation platform, (2) exercise known vulnerabilities and (3) test the robustness of software mitigation techniques.
The unit tests can be found under <code>apps/bearssl-0.6/microsampler_tests</code> and can all be compiled using the provided Makefile. These tests take as input the secret key represented as a hexidecimal value and should be equal to the expected number of bytes (bits) for the cipher selected (e.g., 1024-bit for RSA (modpow)).

## State Construction
    
## Metric Calculation and Statistics Reporting

## Software Modules

[A Pre-Silicon Approach to Discovering Microarchitectural Vulnerabilities in Security Critical Applications]: https://ieeexplore.ieee.org/document/9713708
