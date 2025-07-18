import math

def calculate_simulation_parameters(conc_mg_ml, molecular_weight_kDa):
    """
    Calculate simulation parameters from experimental concentration.
    
    Args:
        conc_mg_ml (float): Experimental concentration in mg/mL
        molecular_weight_kDa (float): Molecular weight in kDa
        
    Returns:
        dict: Dictionary containing all calculated parameters
    """
    # Convert kDa to g/mol (1 kDa = 1000 g/mol)
    molecular_weight_g_mol = molecular_weight_kDa * 1000
    
    # Convert mg/mL to mol/L
    conc_mol_L = conc_mg_ml / molecular_weight_g_mol
    
    # Convert to molecules/L
    avogadro = 6.022e23
    molecules_L = conc_mol_L * avogadro
    
    # Convert to molecules/nm³
    molecules_nm3 = molecules_L / 1e24
    
    # Calculate volume per molecule (nm³)
    volume_per_molecule = 1 / molecules_nm3
    
    # Calculate box length (nm)
    box_length = volume_per_molecule ** (1/3)
    
    return {
        'concentration_mg_ml': conc_mg_ml,
        'molecular_weight_kDa': molecular_weight_kDa,
        'concentration_mol_L': conc_mol_L,
        'molecules_per_L': molecules_L,
        'molecules_per_nm3': molecules_nm3,
        'volume_per_molecule_nm3': volume_per_molecule,
        'box_length_nm': box_length
    }

def print_results(params):
    """Print the calculated parameters in a readable format"""
    print("Experimental Parameters:")
    print(f"- Concentration: {params['concentration_mg_ml']} mg/mL")
    print(f"- Molecular weight: {params['molecular_weight_kDa']} kDa\n")
    
    print("Conversion to Simulation-Compatible Units:")
    print(f"1. Convert mg/mL to mol/L: {params['concentration_mg_ml']}/{params['molecular_weight_kDa']*1000} = {params['concentration_mol_L']:.5f} mol/L")
    print(f"2. Convert to molecules/L: {params['concentration_mol_L']:.5f}×6.022×10^23 = {params['molecules_per_L']:.3f}×10^20 molecules/L")
    print(f"3. Convert to molecules/nm³: {params['molecules_per_L']:.3f}×10^20/10^24 = {params['molecules_per_nm3']:.3f}×10^-4 molecules/nm³\n")
    
    print("Volume per molecule (single nanocluster in a box):")
    print(f"1/{params['molecules_per_nm3']:.3f}×10^-4 = {params['volume_per_molecule_nm3']:.1f} nm³")
    print(f"Box length: ({params['volume_per_molecule_nm3']:.1f})^(1/3) = {params['box_length_nm']:.1f} nm")
    print(f"\nRecommended cubic simulation box size: {params['box_length_nm']:.1f} × {params['box_length_nm']:.1f} × {params['box_length_nm']:.1f} nm³")

# Example usage with the given parameters
params = calculate_simulation_parameters(20, 15)
print_results(params)
