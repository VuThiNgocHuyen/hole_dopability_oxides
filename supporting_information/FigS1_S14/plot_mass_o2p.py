import pandas as pd
import matplotlib.pyplot as plt

# Load the output CSV
df = pd.read_csv("data_sorted_845_with_mass_bandgap.csv")

# Drop rows with missing hole mass or O-2p
df_valid = df.dropna(subset=["hole_mass_11", "hole_mass_22", "hole_mass_33", "O-2p"])

# Compute average hole mass
df_valid["hole_mass_avg"] = df_valid[["hole_mass_11", "hole_mass_22", "hole_mass_33"]].mean(axis=1)

# Compute inverse average hole mass
df_valid["inv_hole_mass_avg"] = 1.0 / df_valid["hole_mass_avg"]

# Sort by O-2p for clean plotting
df_sorted = df_valid.sort_values("O-2p")

# Plotting
plt.figure(figsize=(8, 6))
plt.scatter(df_sorted["O-2p"], df_sorted["inv_hole_mass_avg"],
            color='blue', alpha=0.7, edgecolors='k')
plt.xlabel("O-2p")
plt.ylabel("Inverse Average Hole Mass (1 / mₕ*)")
plt.title("Inverse Average Hole Mass vs O-2p")
plt.grid(True)
plt.tight_layout()
plt.savefig('inv_hole_mass_vs_O2p.eps', format='eps', bbox_inches='tight')

plt.show()
