import os

def extract_coordinates_from_log(log_file_path, output_format='xyz'):
    assert output_format in ('xyz', 'pdb'), "Output format must be 'xyz' or 'pdb'"

    base_filename = os.path.splitext(os.path.basename(log_file_path))[0]

    with open(log_file_path, 'r') as f:
        lines = f.readlines()

    # Try both orientation types
    for orientation_type in ["Standard orientation", "Input orientation"]:
        start_lines = [i for i, line in enumerate(lines) if orientation_type in line]
        if start_lines:
            break

    if not start_lines:
        print(f"No geometry blocks found in {log_file_path}.")
        return

    offset = 5  # Data starts 5 lines after orientation header

    for idx, start in enumerate(start_lines):
        coords = []
        for line in lines[start + offset:]:
            if '---------------------------------------------------------------------' in line:
                break
            tokens = line.split()
            if len(tokens) >= 6:
                atomic_number = int(tokens[1])
                x = float(tokens[3])
                y = float(tokens[4])
                z = float(tokens[5])
                coords.append((idx + 1, atomic_number, x, y, z))

        if output_format == 'xyz':
            write_xyz(base_filename, idx, coords, orientation_type)
        elif output_format == 'pdb':
            write_pdb(base_filename, idx, coords, orientation_type)

    print(f"Extracted {len(start_lines)} geometries from {log_file_path} as {output_format.upper()}.")

def write_xyz(base_filename, idx, coords, orientation_type):
    filename = f"{base_filename}_{idx:03d}.xyz"
    with open(filename, 'w') as out:
        out.write(f"{len(coords)}\n")
        out.write(f"# Extracted from {orientation_type} #{idx}\n")
        for _, atomic_number, x, y, z in coords:
            symbol = atomic_number_to_symbol(atomic_number)
            out.write(f"{symbol} {x:.6f} {y:.6f} {z:.6f}\n")

def write_pdb(base_filename, idx, coords, orientation_type):
    filename = f"{base_filename}_{idx:03d}.pdb"
    with open(filename, 'w') as out:
        out.write(f"REMARK Extracted from {orientation_type} #{idx}\n")
        for atom_id, atomic_number, x, y, z in coords:
            symbol = atomic_number_to_symbol(atomic_number)
            out.write(
                f"ATOM  {atom_id:5d} {symbol:>2s}   MOL     1    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {symbol:>2s}\n"
            )
        out.write("END\n")

def atomic_number_to_symbol(atomic_number):
    periodic_table = [
        "X", "H", "He", "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne",
        "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar", "K",  "Ca",
        "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",  "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U",  "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
        "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
        "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
    ]
    return periodic_table[atomic_number] if 1 <= atomic_number < len(periodic_table) else f"X{atomic_number}"

# --- CLI Usage ---
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_from_log.py yourfile.log [xyz|pdb]")
    else:
        log_file = sys.argv[1]
        out_format = sys.argv[2] if len(sys.argv) > 2 else 'xyz'
        extract_coordinates_from_log(log_file, out_format.lower())
