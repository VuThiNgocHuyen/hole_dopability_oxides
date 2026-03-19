import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define column names manually
columns = [
    "No", "Formula", "O1-potential", "O2-potential", "O-average",
    "VBM", "CBM", "VBM-O", "CBM-O"
]

# Load the data file
df = pd.read_csv("oxides_core_potential_sorted0.dat", sep=r'\s+', names=columns, skiprows=1)

# Reference energy level
reference = 66.8605
df["VBM_relative"] = df["VBM-O"] - reference
df["CBM_relative"] = df["CBM-O"] - reference
df["Band_gap"] = df["CBM_relative"] - df["VBM_relative"]

# Plot settings
fig, ax = plt.subplots(figsize=(4.5, 4.5))
x = np.arange(len(df))
width = 0.8

# Fixed energy range
ymin = -2
ymax = 6

# Colors
vb_color = '#9999ff'
cb_color = '#ff9999'

# Plot valence and conduction band rectangles
#for i, row in df.iterrows():
vbm = df["VBM_relative"]
cbm = df["CBM_relative"]

    # Valence band: from -2 eV to VBM-O
ax.bar(x, vbm-ymin, width=width,
        bottom=ymin, color=vb_color, edgecolor='black')

    # Conduction band: from CBM-O to 6 eV
ax.bar(x, ymax-cbm, width=width,
        bottom=cbm, color=cb_color, edgecolor='black')

# Customize axes and labels
ax.set_xticks(x)
ax.set_xticklabels(df["Formula"], rotation=90, fontsize=8)
ax.set_ylim([ymin, ymax])
ax.set_xlim([-1, len(df)])
ax.set_ylabel("Energy (eV)")
ax.set_title("Band Alignment core potential", fontsize=14)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.grid(axis='y', linestyle=':', color='gray')

plt.tight_layout()
plt.savefig("band_alignment_core.eps", format='eps', dpi=300)
plt.show()
