# Atoms_distribution_as_CHGCAR
This little script takes the output of a VASP AIMD simulation as XDATCAR and loops over all the frames counting the number of times a specific atom occurs in a specific volume of the unit cell. The number of volumes are user defined in terms of subdivision of the 3 base vector of the unit cell by means of the nx, ny, nz variables. 
The atom to search for is hard coded at line 34.

POSSIBLE IMPROVEMENTS:
- atom to search for as user's input
- find a way to automatically determine the amount of volumes as a balance between definition and computational time
- parallelise the code on multiple CPUS in terms of volumes 
