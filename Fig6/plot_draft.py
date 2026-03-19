import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define column names manually
columns = [
    "Formula", "VBM", "CBM", "BPE"
]

# Load the data file
df = pd.read_csv("oxides_pbe.dat", sep=r'\s+', names=columns, skiprows=1)

# Plot settings
fig, ax = plt.subplots(figsize=(10, 4.5))
x = np.arange(len(df))
width = 0.8

# Fixed energy range
ymin = -2
ymax = 6

# Colors
vb_color = '#9999ff'
cb_color = '#ff9999'


ax.bar(x, vbm-ymin, width=width,
        bottom=ymin, color=vb_color, edgecolor='black')

ax.bar(x, ymax-cbm, width=width,
        bottom=cbm, color=cb_color, edgecolor='black')

# Customize axes and labels
ax.set_xticks(x)
ax.set_xticklabels(df["Formula"], rotation=90, fontsize=8)
ax.set_ylim([ymin, ymax])
ax.set_xlim([-1, len(df)])
ax.set_ylabel("Energy (eV)")
ax.set_title("Band Alignment with White Band Gaps", fontsize=14)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.grid(axis='y', linestyle=':', color='gray')

plt.tight_layout()
plt.savefig("band_alignment_bpe.eps", format='eps', dpi=300)
plt.show()