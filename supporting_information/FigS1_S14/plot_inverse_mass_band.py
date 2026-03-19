import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("data_sorted_845_with_mass_bandgap.csv")

# Drop rows where hole mass or bandgap is missing
df_valid = df.dropna(subset=["hole_mass_11", "hole_mass_22", "hole_mass_33", "bandgap"])

# Compute average hole mass
df_valid["hole_mass_avg"] = df_valid[["hole_mass_11", "hole_mass_22", "hole_mass_33"]].mean(axis=1)

# Compute inverse of average hole mass
df_valid["inv_hole_mass_avg"] = 1.0 / df_valid["hole_mass_avg"]

# Plot 1 / hole_mass_avg vs bandgap
plt.figure(figsize=(8, 6))
plt.scatter(df_valid["bandgap"], df_valid["inv_hole_mass_avg"],
            color='seagreen', alpha=1, edgecolors='none')

plt.xlabel("Bandgap (eV)")
plt.ylabel("Inverse Average Hole Mass (1 / mₕ*)")
plt.title("1 / Average Hole Mass vs Bandgap")
#plt.grid(True, linestyle='--')  # Dashed grid line
plt.grid(True, linestyle='--')  # Dashed grid line
plt.tight_layout()

# Save as EPS (vector format)
plt.savefig("inverse_hole_mass_vs_bandgap.eps", format="eps")
plt.show()
