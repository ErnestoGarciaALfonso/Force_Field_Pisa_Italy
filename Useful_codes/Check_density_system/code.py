from collections import defaultdict

# Define atomic masses (g/mol)
atomic_masses = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'P': 30.974, 'S': 32.06, 'NA': 22.990, 'Cl': 35.45,
    'K': 39.098, 'Ca': 40.078, 'Mg': 24.305, 'Zn': 65.38,
    'Fe': 55.845, 
    'AU': 196.96655,
}
from collections import defaultdict


def extract_element(atom_name):
    atom_name = atom_name.strip()
    if atom_name[:2] in atomic_masses:
        return atom_name[:2]
    elif atom_name[:1] in atomic_masses:
        return atom_name[:1]
    return None

def compute_densities_split(gro_path):
    with open(gro_path) as f:
        lines = f.readlines()

    atom_lines = lines[2:-1]
    box_line = lines[-1].strip()
    box = list(map(float, box_line.split()))
    volume_nm3 = box[0] * box[1] * box[2]
    volume_m3 = volume_nm3 * 1e-27

    # Water is usually named "SOL"
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

    mass_water = compute_mass(water_counts)
    mass_system = compute_mass(system_counts)
    total_mass = mass_water + mass_system

    density_water = mass_water / volume_m3
    density_system = mass_system / volume_m3
    density_total = total_mass / volume_m3

    return {
        'water_counts': dict(water_counts),
        'system_counts': dict(system_counts),
        'density_water': density_water,
        'density_system': density_system,
        'density_total': density_total,
        'volume_m3': volume_m3
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python split_density.py <input.gro>")
        sys.exit(1)

    gro_file = sys.argv[1]
    result = compute_densities_split(gro_file)

    print("Water atom counts:")
    for el, count in result['water_counts'].items():
        print(f"  {el}: {count}")
    print("\nNon-water atom counts:")
    for el, count in result['system_counts'].items():
        print(f"  {el}: {count}")

    print(f"\nBox volume        = {result['volume_m3']:.3e} m³")
    print(f"Water density     = {result['density_water']:.1f} kg/m³")
    print(f"Non-water density = {result['density_system']:.1f} kg/m³")
    print(f"Total density     = {result['density_total']:.1f} kg/m³")
    print(f"Box length = {((result['volume_m3']) ** (1./3)*10**9):.3f} nm")

