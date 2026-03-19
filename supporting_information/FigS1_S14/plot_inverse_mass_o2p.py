import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("data_sorted_845_with_mass_bandgap.csv")

# Drop rows with missing hole mass or bandgap
df_valid = df.dropna(subset=["hole_mass_11", "hole_mass_22", "hole_mass_33", "bandgap"])

# Compute average hole mass
df_valid["hole_mass_avg"] = df_valid[["hole_mass_11", "hole_mass_22", "hole_mass_33"]].mean(axis=1)

# Compute inverse hole mass
df_valid["inv_hole_mass_avg"] = 1.0 / df_valid["hole_mass_avg"]

# Plot: inverse average hole mass vs bandgap
plt.figure(figsize=(8, 6))
# Sort by O-2p for clean plotting
plt.scatter(df_valid["O-2p"], df_valid["inv_hole_mass_avg"],
            color='royalblue', alpha=1, edgecolors='none')
plt.xlabel("O-2p")
plt.ylabel("Inverse Average Hole Mass (1 / mₕ*)")
plt.title("Inverse Average Hole Mass vs O-2p")
plt.grid(True, linestyle='--')  # Dashed grid line
plt.tight_layout()

# Save as EPS
plt.savefig("inverse_hole_mass_vs_bandgap_no_filter.eps", format='eps', bbox_inches='tight')
plt.show()
