# Module-granular Mutation Generation for RTL
Mutation generation script provided by our work "Exploring the Parameter Space for Constrained Random Verification of RISC-V CPUs"

## Requirements
Python >= 3.8 
Yosys >= 0.58 (git sha1 157aabb58)

## Usage

```
usage: mutate.py [-h] -wp workpath -f verilogFile -top toplevel -m module -n
                 numMutations [-gen]

Generate mutations of Verilog files using yosys mutate feature.

optional arguments:
  -h, --help       show this help message and exit
  -wp workpath     Work path in which temporary files and results will be saved to.
  -f verilogFile   Verilog file to be mutated.
  -top toplevel    Toplevel module of module hierarchy in Verilog file provided.
  -m module        Module to mutate.
  -n numMutations  Number of mutations to generate
  -gen             If true, the mutations are generated, if false, they are applied to the Verilog.
```

## How to cite

Further details of the approach are described in the folliwng [publication](#soon):

```
@inproceedings{ahmadipour2026verparam,
  title={Exploring the Parameter Space for Constrained Random Verification of RISC-V CPUs},
  author={Ahmadi-Pour, Sallar and Müller, Luca and Drechsler, Rolf},
  booktitle={2026 Forum on specification \& Design Languages (FDL)},
  pages={TBA},
  year={2026},
  organization={IEEE}
}

```

## Acknowledgements

TBA
