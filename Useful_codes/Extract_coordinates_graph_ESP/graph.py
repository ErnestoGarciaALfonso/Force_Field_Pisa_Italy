import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from collections import defaultdict
from matplotlib.ticker import FormatStrFormatter

# === CONFIGURATION ===
esp_file = "molecule.dat"
atom_file = "esp_000.xyz"
grid_points = 500
output_prefix = "esp"

# === READ ESP DATA ===
esp_data = []
with open(esp_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4:
            try:
                esp_data.append([float(x) for x in parts])
            except ValueError:
                continue

esp_array = np.array(esp_data)
values = esp_array[:, 0]
x = esp_array[:, 1]
y = esp_array[:, 2]
z = esp_array[:, 3]

print(f"✅ Loaded {len(values)} ESP points")
print(f"ESP range: {values.min():.5f} to {values.max():.5f} au")

# === READ ATOMS FROM SIMPLE FORMAT ===
atoms = []
with open(atom_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4:
            elem = parts[0]
            pos = list(map(float, parts[1:4]))
            atoms.append({"type": elem, "x": pos[0], "y": pos[1], "z": pos[2]})

print(f"✅ Loaded {len(atoms)} atoms from {atom_file}")

# === ATOM COLORS ===
atom_colors = defaultdict(lambda: 'gray')
atom_colors.update({
    "O": "red",
    "H": "blue",
    "C": "black",
    "N": "green",
    "S": "orange"
})

# === PLOT FUNCTION ===
def plot_plane(coord1, coord2, atom_proj1, atom_proj2, plane_name, filename):
    points = np.column_stack((coord1, coord2))
    grid1 = np.linspace(coord1.min(), coord1.max(), grid_points)
    grid2 = np.linspace(coord2.min(), coord2.max(), grid_points)
    grid1, grid2 = np.meshgrid(grid1, grid2)
    grid_values = griddata(points, values, (grid1, grid2), method='cubic')

    plt.figure(figsize=(8, 6))
    contour = plt.contourf(grid1, grid2, grid_values, levels=300, cmap='seismic', zorder=2)
    
    # Create colorbar with custom formatting
    cbar = plt.colorbar(contour, label='Electrostatic Potential (au)')
    cbar.formatter = FormatStrFormatter('%g')  # Simple formatting that shows 0 as 0
    cbar.update_ticks()
    
    plt.title(f'ESP on {plane_name} plane')
    plt.xlabel(f'{plane_name[0]} [au]')
    plt.ylabel(f'{plane_name[1]} [au]')

    for atom in atoms:
        a1 = atom[atom_proj1]
        a2 = atom[atom_proj2]
        atype = atom["type"]
        color = atom_colors[atype]
        plt.scatter(a1, a2, s=100, c=color, edgecolors='black',
                    linewidths=1.5, alpha=1.0, zorder=20)
        plt.text(a1, a2, atype, fontsize=3, ha='center', va='center',
                 color='white', weight='bold', zorder=30)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"✅ Saved {filename}")

# === PLOT ALL PLANES ===
plot_plane(x, z, "x", "z", "xz", f"{output_prefix}_xz.png")
plot_plane(y, z, "y", "z", "yz", f"{output_prefix}_yz.png")
plot_plane(x, y, "x", "y", "xy", f"{output_prefix}_xy.png")