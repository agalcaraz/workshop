    #Ploting energies vs number of cycles 
    
    all_cycles = []
    
    for line in data:
        if 'GEOMETRY OPTIMIZATION CYCLE' in line:
            cycle_line = line
            cycle_line_split = cycle_line.split()
            numbers = float(cycle_line_split[-2])
            all_cycles.append(numbers)
    
    plt.figure()
    plt.xlabel('Number of cycles')
    plt.ylabel('Energy (Eh)')
    plt.plot(all_cycles, all_energies[:-1], '--o')
    plt.savefig(F'{fname}.png')