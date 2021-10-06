# Microarchitectural Vulnerability Detection
This project investigates how best to utilize traces from pre-silicon simulation for vulnerability detection at the microarchitectural level of abstraction during the IC design life-cycle.  In particular, the analysis is focused on traces from executions of security critical applications in order to validate claims of properties enabling confidentiality protections.

The RISC-V BOOM processor released with the Chipyard framework from UC Berkeley is used as a testbed, along with cryptographic primitives from the BearSSL library as applications to study.

The tool has three stages: simulation, parsing and calculation of vulnerability metrics.

### Simulation
The first stage is to simulate the processor-under-test, executing the selected application. We use the Verilator backend, which is a cycle-accurate C++ model of the hardware.

1. Clone the Chipyard repository from Github: <code>git clone https://github.com/ucb-bar/chipyard.git</code>
2. Checkout version 1.2.0: <code>git checkout tags/1.2.0</code>
3. Change the submodule path for the BOOM processor to point to our modified implementation:
    1. Open .gitmodules from the root directory of Chipyard
    2. Under <code>[submodule "generators/boom"]</code>, change to <code>url = https://github.com/kristinbarber/riscv-boom.git</code>
4. Follow instructions for repository initialization from Chipyard documentation
5. Change to the <code>sims/verilator</code> directory
    a. Run <code>CONFIG=SmallBoomConfig</code>, this command will generate the simulator executable

### State Construction
### Metric Calculation and Statistics Reporting

## Software Modules

The minimally modified version of the RISC-V BOOM core must be 
