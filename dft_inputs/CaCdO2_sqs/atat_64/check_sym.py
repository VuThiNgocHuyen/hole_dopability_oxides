from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Load the structure from a POSCAR or CONTCAR file
filename = "POSCAR"  # Change to "CONTCAR" if needed

try:
    structure = Structure.from_file(filename)
    analyzer = SpacegroupAnalyzer(structure, symprec=1e-3)  # Adjust symprec for tolerance

    # Get symmetry information
    space_group = analyzer.get_space_group_symbol()
    space_group_number = analyzer.get_space_group_number()
    symmetry_operations = analyzer.get_symmetry_operations()
    
    # Print the symmetry information
    print(f"File: {filename}")
    print(f"Space group: {space_group} (No. {space_group_number})")
    print(f"Number of symmetry operations: {len(symmetry_operations)}")
    print("Symmetry operations:")
    for op in symmetry_operations:
        print(op)
        
    # Optionally, check if the structure is primitive or conventional
    conventional_structure = analyzer.get_conventional_standard_structure()
    primitive_structure = analyzer.get_primitive_standard_structure()
    print("\nConventional Structure:")
    print(conventional_structure)
    print("\nPrimitive Structure:")
    print(primitive_structure)

except Exception as e:
    print(f"Error reading {filename}: {e}")

