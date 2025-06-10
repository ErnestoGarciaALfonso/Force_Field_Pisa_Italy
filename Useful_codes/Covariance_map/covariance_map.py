import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from scipy.ndimage import gaussian_filter, label
import argparse
import sys
from matplotlib.patches import Patch
from scipy.spatial import distance

def plot_energy_landscape(output_filename='energy_landscape_2d.png', smooth_sigma=0):
    # Read and parse input data
    energy_data = []
    while True:
        try:
            line = input()
            if "************" in line:
                continue
            parts = list(map(float, line.strip().split()))
            if len(parts) == 3:
                energy_data.append(parts)
        except EOFError:
            break

    if not energy_data:
        print("No energy data found in input")
        return

    # Convert list to array and extract columns
    energy_data = np.array(energy_data)
    x = energy_data[:, 0]
    y = energy_data[:, 1]
    z = energy_data[:, 2]

    # Find the global minimum and normalize
    min_z = np.min(z)
    max_z = np.max(z)
    z = z - min_z  # Normalize energies relative to deepest basin

    # Create grid for interpolation
    xi = np.linspace(x.min() - 0.02*(x.max()-x.min()), x.max() + 0.02*(x.max()-x.min()), 500)
    yi = np.linspace(y.min() - 0.02*(y.max()-y.min()), y.max() + 0.02*(y.max()-y.min()), 500)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
   
    # Create mask for valid interpolation region
    from scipy.spatial import Delaunay
    tri = Delaunay(np.column_stack((x, y)))
    mask = ~(tri.find_simplex(np.column_stack((xi_grid.ravel(), yi_grid.ravel()))) >= 0).reshape(xi_grid.shape)
   
    # Interpolate data
    zi = griddata((x, y), z, (xi_grid, yi_grid), method='linear')

    # Optional smoothing
    if smooth_sigma > 0:
        zi = gaussian_filter(zi, sigma=smooth_sigma)

    # Plotting
    plt.figure(figsize=(12, 9))
    #contour = plt.contourf(xi_grid, yi_grid, zi, levels=280, cmap='magma', vmin=min_z, vmax=max_z)
    
   # cbar = plt.colorbar(contour)
    vmin, vmax = min_z, max_z
    levels = np.linspace(vmin, vmax, 150)
    contour = plt.contourf(xi, yi, np.ma.masked_where(mask, zi), 
                          levels=levels, cmap=LinearSegmentedColormap.from_list("", [ "black", "red","wheat","white"]), extend='max')
    cbar = plt.colorbar(contour, pad=0.02, aspect=30)
     # Define colormaps
    cbar.set_ticks(np.linspace(vmin, vmax, 6))
    cbar.set_label('ΔG (kJ/mol)', fontsize=12)
    

    # Plot out-of-region areas first (light blue)
    plt.pcolormesh(xi, yi, np.ma.masked_where(~mask, mask), 
                  cmap=ListedColormap(['white']), shading='auto')
           # Create legend
    legend_elements = [
        Patch(facecolor='#ADD8E6', edgecolor='#ADD8E6', label='Outside Interpolation Region'),
    ]
    
    
    # Axis labels and title
    plt.xlabel('PC1 (nm)', fontsize=12)
    plt.ylabel('PC2 (nm)', fontsize=12)
    #plt.title('2D Free Energy Landscape', fontsize=14)

    # Save to file
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    print(f"2D plot saved as {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 2D energy landscape plot.")
    parser.add_argument('--output', type=str, default='energy_landscape_2d.png', 
                       help='Output PNG file name')
    parser.add_argument('--smooth', type=float, default=0, 
                       help='Sigma for Gaussian smoothing (0 = no smoothing)')
    args = parser.parse_args()
    plot_energy_landscape(output_filename=args.output, smooth_sigma=args.smooth)


