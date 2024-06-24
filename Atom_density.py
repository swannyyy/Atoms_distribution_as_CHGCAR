from ase.io import read
import numpy as np
from ase.io.vasp import read_vasp_xdatcar
from ase.io.vasp import write_vasp
from ase.io.trajectory import Trajectory
from ase.build import make_supercell
from collections import defaultdict

def create_volumes(cell, nx, ny, nz):
    # Calculate volume dimensions
    lx, ly, lz = cell.lengths()
    dx, dy, dz = lx / nx, ly / ny, lz / nz

    volumes = []
    for i in range(nz):
        for j in range(ny):
            for k in range(nx):
                
                volume = {'x': (k * dx, (k + 1) * dx),
                          'y': (j * dy, (j + 1) * dy),
                          'z': (i * dz, (i + 1) * dz),
                          'count': 0}
                
                volumes.append(volume)
    return volumes

def count_hydrogens(atoms, volumes):
    counts = defaultdict(int)
    for atom in atoms:
        for volume in volumes:
            x_in_range = volume['x'][0] <= atom.position[0] < volume['x'][1]
            y_in_range = volume['y'][0] <= atom.position[1] < volume['y'][1]
            z_in_range = volume['z'][0] <= atom.position[2] < volume['z'][1]
            if x_in_range and y_in_range and z_in_range and atom.symbol == 'H':
                volume['count'] += 1
                counts[id(volume)] += 1
            else:
                counts[id(volume)] = counts[id(volume)] + 0
    return counts

def normalize_counts(counts):
    total_count = sum(counts.values())
    for key in counts:
        counts[key] /= total_count
    return counts

# Load XDATCAR
atoms = read('XDATCAR', index=':')
cell = atoms[0].cell
nx=30
ny=30
nz=10
# Create volumes
volumes = create_volumes(cell,nx,ny,nz)
# Count hydrogen atoms in volumes across all configurations
total_counts = defaultdict(int)
i=1
for atom in atoms:
    counts = count_hydrogens(atom, volumes)
    i=i+1
    j=1
    for key, value in counts.items():
        total_counts[key] += value
        j=j+1
# Normalize counts
normalized_counts = normalize_counts(total_counts)
#print((normalized_counts))

# Create density array
density = np.zeros(len(volumes))
print(len(density))
i=0
for volume_id, volume_count in normalized_counts.items():
    print (volume_id,volume_count)
    density[i] = volume_count
    i=i+1

# Write density to cube file
origin=np.array([np.array(volumes[0]['x']), np.array(volumes[0]['y']), np.array(volumes[0]['z'])])

print(density)

write_vasp('atom_dist.vasp',atoms=atoms[0])
# Write CHGCAR-like file
with open('atom_dist.vasp', 'a') as f:
     # Empty line
    f.write("\n")
    
    # Write divisions
    f.write(f"{nx} {ny} {nz}\n")
    
    for d in density:f.write(f"{d}\n")

