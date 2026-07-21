#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys, argparse, shutil, random

def run_yosys(command):
    return os.system("yosys -q -q -p '{command}'".format(command = command))

def main():
    
    parser = argparse.ArgumentParser(
            description='Generate mutations of Verilog files using yosys mutate feature.',
            epilog = '',
            formatter_class = argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('-wp', type = str, help = 'Work path in which temporary files and results will be saved to.', required = True, metavar = 'workpath', dest = 'workpath')
    parser.add_argument('-f', type = str, help = 'Verilog file to be mutated.', required = True, metavar = 'verilogFile', dest = 'verilogFile')
    parser.add_argument('-top', type = str, help = 'Toplevel module of module hierarchy in Verilog file provided.', required = True, metavar = 'toplevel', dest = 'toplevel')
    parser.add_argument('-m', type = str, help = 'Module to mutate.', required = True, metavar = 'module', dest = 'module')
    parser.add_argument('-n', type = int, help = 'Number of mutations to generate', required = True, metavar = 'numMutations', dest = 'numMutations')
    parser.add_argument('-gen', action = 'store_true', help = 'If true, the mutations are generated, if false, they are applied to the Verilog.',  dest = 'gen')
    
    args = parser.parse_args()
    
    fileName = os.path.basename(args.verilogFile)
    fileNameNoExt = os.path.splitext(fileName)[0]
    
    if(not os.path.isdir(args.workpath)):
        os.makedirs(args.workpath) 

    # Prepare directories and files for mutations
    moduleDir = os.path.join(args.workpath, args.module)
    mutationPath = os.path.join(args.workpath, args.module, "mutation.txt")
    baseFile = os.path.join(args.workpath, fileName)

    if args.gen:
        
        # Copy original into workpath
        shutil.copy(args.verilogFile, os.path.join(args.workpath, fileName))
        if not os.path.isdir(moduleDir):
            os.makedirs(moduleDir) 

        # Generate mutation using yosys
        print("Generate " + str(args.numMutations) + " mutations for module " + args.module + " of design " + args.toplevel)
        # Pseudo-random seed
        seed = random.randint(1, 1000000)
        # "None mutation" is generated with -none flag
        generateCommand = "read_verilog {baseFile}; hierarchy -top {toplevel}; mutate -none -list {numMutations} -seed {seed} -o {mutationPath} {module}".format(
        baseFile = baseFile, toplevel = args.toplevel, numMutations=args.numMutations, seed = seed, mutationPath = mutationPath, module = args.module)
        if run_yosys(generateCommand):
            print("Yosys Error")
            exit(1)

    else:
        mutDir = os.path.join(moduleDir, "generated_mutations")
        # Clean generated mutations
        if os.path.isdir(mutDir):
            shutil.rmtree(mutDir)
        os.makedirs(mutDir)
        
        # Apply mutation and write out design
        with open(mutationPath) as mutationsFile:
            mutations = mutationsFile.read().splitlines()
        for mutIdx, mut in enumerate(mutations):
            if mutIdx >= args.numMutations:
                break
            print("Apply mutation " + str(mutIdx) + " to module " + args.module + " of design " + args.toplevel)
            mutFile = fileNameNoExt + "_mut_" + str(mutIdx)
            mutPath = os.path.join(mutDir, mutFile)
            mutateCommand = "read_verilog {fileName}; hierarchy -top {toplevel}; {mutation}; proc; write_verilog -noattr {mutPath}.v".format(
            fileName = baseFile, toplevel = args.toplevel, mutation = mut, mutPath = mutPath)
            if run_yosys(mutateCommand):
                print("Yosys Error")
                exit(1)

    return 0

if __name__ == "__main__":
    main()
