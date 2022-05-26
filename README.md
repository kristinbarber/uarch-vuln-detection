# Microarchitectural Vulnerability Detection
This project investigates how best to utilize traces from pre-silicon simulation for vulnerability detection at the microarchitectural level of abstraction during the IC design life-cycle.  In particular, the analysis is focused on traces from executions of security critical applications in order to validate claims of properties enabling confidentiality protections.

The RISC-V BOOM processor released with the Chipyard framework from UC Berkeley is used as a testbed, along with cryptographic primitives from the BearSSL library as applications to study.

The tool has three stages: simulation, parsing and calculation of vulnerability metrics.

### Simulation

#### Processor Simulator
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

#### Applications
The <code>apps</code> directory holds respositories for tests to be run with the simulator.

We have added several tests to the BearSSL unit tests suite to (1) incorporate vulnerabilities and (2) ease use with the simulation platform.
The unit tests can be found under <code>apps/bearssl-0.6/microsampler_tests</code> and can all be compiled using the provided Makefile. These tests take as input the the secret key value represented as a hexidecimal value and should be equal to the expected number of bytes (bits) for the cipher selected (e.g., 1024-bit for RSA (modpow)).

### State Construction
### Metric Calculation and Statistics Reporting

## Software Modules

The minimally modified version of the RISC-V BOOM core must be 
