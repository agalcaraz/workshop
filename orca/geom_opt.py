﻿# -------------------------------------------------
#
# Script for parsing main information of a geometry
# optimization (with vibrational frequencies calculation) 
# done in orca 4.2.1 using as input a .log file
#
# The input format is: 'python geom_opt.py filename.log'
#
# Output information: electronic parameters and 
# energy vs number of optimization cycles representation
# -------------------------------------------------
# =================================================
# Written by Antonio Garcia Alcaraz 11/2021
# =================================================

import os
import argparse
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":

    #Create the argument parser
    parser = argparse.ArgumentParser("This script parses optimization files done in orca to extract final single point energy, zero point energy and g correction")
    parser.add_argument("path", help="The filepath to the file to be analyzed")
    
    args = parser.parse_args()
    filename =args.path
    
    #Read the data from the specified file
    outfile = open(filename)
    data = outfile.readlines()
    outfile.close()
    
    #Figure out the file name for writing the output
    fname = os.path.basename(args.path).split('.')[0]
    
    #Checking if the calculation was correctly finished
    
    found = False
    for line in data:
        if 'OPTIMIZATION RUN DONE' in line:
            found = True
    if not found:
        sys.exit('Optimization not completed, need more cycles')
        
    found = False
    for line in data:
        if 'ORCA TERMINATED NORMALLY' in line:
            found = True
    if not found:
        sys.exit('Calculation not completed. Something went wrong in the termochemistry analysis')

    #Printing energy, zpe and g correction
    
    all_energies = []

    for line in data:
        if 'FINAL SINGLE POINT ENERGY' in line:
            energy_line = line
            energy_line_split = energy_line.split()
            energy_values = float(energy_line_split[-1])
            all_energies.append(energy_values)  
        if 'Zero point energy' in line:
            zero_line = line
            zero_line_split = zero_line.split()
            zero_value = float(zero_line_split[4])
        if 'G-E(el)' in line:
            g_line = line
            g_line_split = g_line.split()
            g_value = float(g_line_split[2])

    print('Final single point energy (Eh) : {}'.format(all_energies[-1]))
    print('Zero point energy (Eh) : {}'.format(zero_value))
    print('G-E(el) (Eh) : {}'.format(g_value))
    
    #Printing the first three vibrational frequencies
    
    for linenum, line in enumerate(data):
        if 'Scaling factor for frequencies' in line:
            scaling_line = linenum
    
    vibration_lines = data[scaling_line+8:scaling_line+11]
    
    vibration_values = []

    for line in vibration_lines:
        vibration_line_split = line.split()
        values = vibration_line_split[1]
        vibration_values.append(values)
    
    joined_values = ", ".join(vibration_values)
    
    print('First 3 vibrational frequencies (cm**-1) : {}'.format(joined_values)) 
    
    #Printing number of atoms
    
    for linenum, line in enumerate(data):
        if '*xyz' in line:
            xyz_line = linenum
        if '****END OF INPUT****' in line:
            end_line = linenum
    first_atom = xyz_line + 2
    last_atom = end_line - 1
    num_atom = last_atom - first_atom
    
    #Printing molecular orbitals
    
    orbital_lines = []
    mulliken_lines = []
    
    for linenum, line in enumerate(data):
        if 'ORBITAL ENERGIES' in line:
            orbital_line = linenum
            orbital_lines.append(orbital_line)
        if '* MULLIKEN POPULATION ANALYSIS *' in line:
            mulliken_line = linenum
            mulliken_lines.append(mulliken_line)
    
    final_orbital_line = orbital_lines[-1]
    final_mulliken_line = mulliken_lines[-1]
    
    orbital_list = data[final_orbital_line+4:final_mulliken_line-2]
    
    occupancy_list = []
    orbital_energies_list = []
    
    for line in orbital_list:
        orbital_list_split = line.split()
        occupancy_values = float(orbital_list_split[1])
        occupancy_list.append(occupancy_values)
        orbital_energies_values = float(orbital_list_split[3])
        orbital_energies_list.append(orbital_energies_values)
        
    occupied_list = []
    
    for number in occupancy_list:
        if number == 2:
            occupied_list.append(number)
    
    length_occupied_list = len(occupied_list)
    
    HOMO = orbital_energies_list[length_occupied_list-1]
    LUMO = orbital_energies_list[length_occupied_list]
    gap = LUMO - HOMO
    
    print('Energy HOMO (eV) : {} / MO nº: {}'.format(HOMO, length_occupied_list-1))
    print('Energy LUMO (eV) : {} / MO nº: {}'.format(LUMO, length_occupied_list))
    print('gap HOMO-LUMO (eV) : {}'.format(gap))
    
    
            
   

        
        
    
            

    

    