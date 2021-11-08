import os
import glob
import argparse

if __name__ == "__main__":

    #Create the argument parser
    parser = argparse.ArgumentParser("This script parses amber mdout files to extract the total energy.")
    parser.add_argument("path", help="The filepath to the file(s) to be analyzed.")
    
    args = parser.parse_args()
    filename = args.path
    
    #Read the data from the specified file
    f = open(filename)
    data = f.readlines()
    f.close()
    
    #Figure out the file name for writing the output
    fname = os.path.basename(args.path).split('.')[0]
    
    etot = []
    
    # Loop through the lines
    for line in data:
        split_line = line.split()
        if 'Etot' in line:
            etot.append(float(split_line[2]))
            
    # Get rid of values we don't need.
    values = etot[:-2]

    # Open a file for writing
    outfile_location = F'{fname}_Etot.txt'
    outfile = open(outfile_location, 'w+')
    
    for value in values:
        outfile.write(f'{value}\n')

outfile.close()
