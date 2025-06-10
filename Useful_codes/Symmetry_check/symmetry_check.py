import numpy as np
from math import isclose, sqrt, pi
from collections import defaultdict

# Full periodic table of atomic masses
ATOMIC_MASSES = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'F': 18.998, 'Ne': 20.180, 'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06,
    'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078, 'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996,
    'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.63,
    'As': 74.922, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.95, 'Tc': 98, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41,
    'In': 114.82, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33,
    'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93,
    'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05, 'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95,
    'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Tl': 204.38,
    'Pb': 207.2, 'Bi': 208.98, 'Po': 209, 'At': 210, 'Rn': 222
}

def read_xyz(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        raise ValueError("Empty file")
    
    try:
        num_atoms = int(lines[0])
    except ValueError:
        raise ValueError("First line must contain atom count")
    
    if len(lines) < num_atoms + 2:
        raise ValueError("Insufficient lines for declared atom count")
    
    atoms = []
    coords = []
    
    for line in lines[2:2+num_atoms]:
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid atom line: {line}")
        
        atoms.append(parts[0].capitalize())
        try:
            coords.append([float(x) for x in parts[1:4]])
        except ValueError:
            raise ValueError(f"Invalid coordinates in line: {line}")
    
    return atoms, np.array(coords)

def center_molecule(atoms, coords):
    total_mass = 0
    weighted_coords = np.zeros(3)
    
    for atom, coord in zip(atoms, coords):
        mass = ATOMIC_MASSES.get(atom)
        if mass is None:
            raise ValueError(f"Unknown atomic mass for element '{atom}'")
        weighted_coords += mass * coord
        total_mass += mass

    com = weighted_coords / total_mass
    print("Center of Mass (COM):", com)
    centered = coords - com

    inertia = np.zeros((3, 3))
    for coord in centered:
        inertia += np.outer(coord, coord)
    _, eigvecs = np.linalg.eigh(inertia)
    aligned = np.dot(centered, eigvecs)

    return aligned

def distance_matrix(coords):
    n = len(coords)
    dist_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_mat[i,j] = np.linalg.norm(coords[i] - coords[j])
    return dist_mat

def is_equivalent(a, b, tolerance=1e-4):
    return all(isclose(x, y, abs_tol=tolerance) for x, y in zip(a, b))

def check_symmetry_operation(atoms, coords, transformed, orig_dist, tolerance):
    n = len(atoms)
    new_dist = distance_matrix(transformed)
    
    if not np.allclose(np.sort(orig_dist, axis=None), np.sort(new_dist, axis=None), atol=tolerance):
        return False
    
    matched = [False] * n
    for i in range(n):
        for j in range(n):
            if not matched[j] and atoms[i] == atoms[j]:
                if is_equivalent(transformed[i], coords[j], tolerance):
                    matched[j] = True
                    break
        else:
            return False
    return True

def generate_test_directions():
    directions = []
    directions.extend([(1,0,0), (0,1,0), (0,0,1)])
    directions.extend([(1,1,0), (1,0,1), (0,1,1), (1,-1,0), (1,0,-1), (0,1,-1)])
    directions.extend([(1,1,1), (1,1,-1), (1,-1,1), (-1,1,1)])
    directions.extend([(1,2,0), (2,1,0), (1,0,2), (2,0,1), (0,1,2), (0,2,1)])
    return [np.array(d)/np.linalg.norm(d) for d in directions]

def find_symmetry_elements(atoms, coords, tolerance=1e-4):
    orig_dist = distance_matrix(coords)
    test_directions = generate_test_directions()
    
    symmetry_ops = {'E': np.eye(3)}
    
    inverted = -coords
    if check_symmetry_operation(atoms, coords, inverted, orig_dist, tolerance):
        symmetry_ops['i'] = -np.eye(3)
    
    for order in [2, 3, 4, 5, 6]:
        angle = 2*pi/order
        for axis in test_directions:
            rotated = rotate(coords, axis, angle)
            if check_symmetry_operation(atoms, coords, rotated, orig_dist, tolerance):
                op_name = f'C{order}'
                symmetry_ops[op_name] = rotation_matrix(axis, angle)
    
    for order in [2, 4, 6]:
        angle = 2*pi/order
        for axis in test_directions:
            rotated = rotate(coords, axis, angle)
            reflected = reflect(rotated, axis)
            if check_symmetry_operation(atoms, coords, reflected, orig_dist, tolerance):
                op_name = f'S{order}'
                symmetry_ops[op_name] = np.dot(reflection_matrix(axis), rotation_matrix(axis, angle))
    
    for normal in test_directions:
        reflected = reflect(coords, normal)
        if check_symmetry_operation(atoms, coords, reflected, orig_dist, tolerance):
            op_name = 'σ'
            symmetry_ops[op_name] = reflection_matrix(normal)
    
    return symmetry_ops

def rotate(coords, axis, angle):
    return np.dot(coords, rotation_matrix(axis, angle).T)

def rotation_matrix(axis, angle):
    axis = axis/np.linalg.norm(axis)
    ux, uy, uz = axis
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    return np.array([
        [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
        [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
        [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
    ])

def reflect(coords, normal):
    return np.dot(coords, reflection_matrix(normal).T)

def reflection_matrix(normal):
    normal = normal/np.linalg.norm(normal)
    return np.eye(3) - 2 * np.outer(normal, normal)

def classify_point_group(symmetry_ops):
    has_inversion = 'i' in symmetry_ops
    has_reflection = any(k.startswith('σ') for k in symmetry_ops)
    rotations = [k for k in symmetry_ops if k.startswith('C')]
    improper_rotations = [k for k in symmetry_ops if k.startswith('S')]
    
    if any(int(op[1:]) > 6 for op in rotations):
        return 'D∞h' if has_inversion else 'C∞v'
    
    if 'C5' in rotations and has_reflection:
        return 'D5h'
    if 'C6' in rotations and has_reflection:
        return 'D6h'
    if 'C4' in rotations and has_reflection:
        return 'D4h'
    if 'C3' in rotations and has_reflection:
        return 'D3h'
    
    if len([op for op in rotations if op == 'C2']) >= 3:
        if has_inversion:
            return 'D2h'
        elif has_reflection:
            return 'D2d'
        else:
            return 'D2'
    
    if has_inversion and len(rotations) >= 1:
        return 'D2h'
    if 'S4' in improper_rotations:
        return 'S4'
    if 'S6' in improper_rotations:
        return 'S6'
    if has_reflection and 'C2' in rotations:
        return 'C2v'
    if has_reflection:
        return 'Cs'
    if 'C2' in rotations:
        return 'C2'
    if has_inversion:
        return 'Ci'
    
    return 'C1'

def analyze_molecule(filename, tolerance=1e-4):
    try:
        atoms, coords = read_xyz(filename)
        coords = center_molecule(atoms, coords)
        symmetry_ops = find_symmetry_elements(atoms, coords, tolerance)
        point_group = classify_point_group(symmetry_ops)
        
        print(f"\nAnalysis of {filename}")
        print(f"Number of atoms: {len(atoms)}")
        print(f"Point group: {point_group}")
        
        print("\nSymmetry operations found:")
        for op in sorted(symmetry_ops.keys()):
            print(f" - {op}")
        
        return {
            'atoms': atoms,
            'coordinates': coords,
            'point_group': point_group,
            'symmetry_operations': symmetry_ops
        }
    except Exception as e:
        print(f"Error analyzing {filename}: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python symmetry.py <filename.xyz>")
        sys.exit(1)
    
    analyze_molecule(sys.argv[1])
