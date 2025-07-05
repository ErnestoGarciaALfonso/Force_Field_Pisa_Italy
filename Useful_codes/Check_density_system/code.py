from collections import defaultdict

# Define atomic masses (g/mol)
atomic_masses = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'P': 30.974, 'S': 32.06, 'NA': 22.990, 'Cl': 35.45,
    'K': 39.098, 'Ca': 40.078, 'Mg': 24.305, 'Zn': 65.38,
    'Fe': 55.845, 'AU': 196.96655,
}

def extract_element(atom_name):
    atom_name = atom_name.strip()
    if atom_name[:2] in atomic_masses:
        return atom_name[:2]
    elif atom_name[:1] in atomic_masses:
        return atom_name[:1]
    return None

def compute_densities_split(gro_path, target_density_kgm3=997):
    with open(gro_path) as f:
        lines = f.readlines()

    atom_lines = lines[2:-1]
    box_line = lines[-1].strip()
    box = list(map(float, box_line.split()))
    volume_nm3 = box[0] * box[1] * box[2]
    volume_m3 = volume_nm3 * 1e-27

    # Count atoms
    water_counts = defaultdict(int)
    system_counts = defaultdict(int)

    for line in atom_lines:
        resname = line[5:10].strip()   # residue name (e.g., SOL, PROT)
        atom_name = line[10:15].strip()
        element = extract_element(atom_name)
        if not element:
            continue
        if resname == "SOL":
            water_counts[element] += 1
        else:
            system_counts[element] += 1

    def compute_mass(counts):
        gmol = sum(atomic_masses[el] * count for el, count in counts.items())
        return gmol / 6.022e23 / 1000  # kg

    mass_system = compute_mass(system_counts)
    mass_water = compute_mass(water_counts)
    total_mass = mass_water + mass_system

    # Current densities
    density_water = mass_water / volume_m3
    density_system = mass_system / volume_m3
    density_total = total_mass / volume_m3

    # Calculate required water molecules to reach target density
    target_mass_total = target_density_kgm3 * volume_m3
    required_mass_water = target_mass_total - mass_system
    required_water_molecules = int((required_mass_water * 6.022e23 * 1000) / 18.015)  # 18.015  molar mass of water (H₂O) in grams per mole (g/mol)

    return {
        'water_counts': dict(water_counts),
        'system_counts': dict(system_counts),
        'density_water': density_water,
        'density_system': density_system,
        'density_total': density_total,
        'volume_m3': volume_m3,
        'current_water_molecules': sum(water_counts.values()) // 3,  # Assuming 3 atoms per water
        'required_water_molecules': required_water_molecules // 3,   # Return integer number of molecules
        'box_length_nm': (volume_nm3 ** (1./3)),
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python split_density.py <input.gro> [target_density_kgm3]")
        sys.exit(1)

     #python code.py system.gro 997  # For TIP3P water (default)
    
    gro_file = sys.argv[1]
    target_density = float(sys.argv[2]) if len(sys.argv) > 2 else 997.0  # Default for SPC/TIP3P
    result = compute_densities_split(gro_file, target_density)

    # Print results
    print("=== Atomic Composition ===")
    print("Water atom counts:")
    for el, count in result['water_counts'].items():
        print(f"  {el}: {count}")
    print("\nNon-water atom counts:")
    for el, count in result['system_counts'].items():
        print(f"  {el}: {count}")

    print("\n=== System Properties ===")
    print(f"Box volume        = {result['volume_m3']:.3e} m³")
    print(f"Box length        = {result['box_length_nm']:.3f} nm")
    print(f"Current water molecules = {result['current_water_molecules']}")
    print(f"Required water molecules to reach {target_density} kg/m³ = {result['required_water_molecules']}")

    print("\n=== Densities ===")
    print(f"Water density     = {result['density_water']:.1f} kg/m³")
    print(f"Non-water density = {result['density_system']:.1f} kg/m³")
    print(f"Total density     = {result['density_total']:.1f} kg/m³")