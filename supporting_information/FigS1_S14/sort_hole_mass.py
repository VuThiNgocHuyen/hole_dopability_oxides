import pandas as pd

# Load the input file
df = pd.read_csv("data_sorted_845_with_mass_bandgap.csv")

# Drop rows with any missing hole mass values to compute the average reliably
df_valid = df.dropna(subset=["hole_mass_11", "hole_mass_22", "hole_mass_33"])

# Compute the average hole mass and add it as a new column
df_valid["hole_mass_avg"] = df_valid[["hole_mass_11", "hole_mass_22", "hole_mass_33"]].mean(axis=1)

# Sort the DataFrame by average hole mass
df_sorted = df_valid.sort_values(by="hole_mass_avg")

# Save to a new CSV file
df_sorted.to_csv("data_sorted_by_hole_mass.csv", index=False)

print("Saved: data_sorted_by_hole_mass.csv")
