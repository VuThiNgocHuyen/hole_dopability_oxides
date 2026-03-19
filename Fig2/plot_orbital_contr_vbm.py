import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def bin_and_replace(df, col='O-2p', bin_width=0.02):
    max_val   = df[col].max()
    bins      = np.arange(0, max_val + bin_width, bin_width)
    centers   = (bins[:-1] + bins[1:]) / 2
    out       = df.copy()
    out[col]  = pd.cut(df[col], bins=bins, labels=centers,
                       include_lowest=True).astype(float)
    return out, bins

# ── LOAD ────────────────────────────────────────────────────────────────────────
df_all  = pd.read_csv('Data_sorted_845.csv')
df_152  = pd.read_csv('Data_sorted_152.csv')

# ── BIN ────────────────────────────────────────────────────────────────────────
df_all_binned,  bins = bin_and_replace(df_all)
df_152_binned, _     = bin_and_replace(df_152)

counts_all = df_all_binned['O-2p'].value_counts().sort_index()
counts_152 = df_152_binned['O-2p'].value_counts().sort_index()

bin_centers = counts_all.index.values
y_all       = counts_all.values
y_152       = counts_152.reindex(bin_centers, fill_value=0).values

# (optional) smoothing
#smoothed_all = gaussian_filter1d(y_all, sigma=3)
#smoothed_152 = gaussian_filter1d(y_152, sigma=3)

# ── PLOT ────────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(
    nrows=2, ncols=1, sharex=True,
    figsize=(4, 5),
    gridspec_kw={'height_ratios': [1, 1]}  # Reduce y-axis height for second plot
)

# Plot for 845
ax1.bar(bin_centers, y_all, width=0.02, color='#17becf', alpha=0.8,
        edgecolor='none')
#ax1.plot(bin_centers, smoothed_all, color='blue', linewidth=2, label='Smoothed 845')
ax1.set_ylabel('N (845)')
ax1.set_ylim(0, 160)
ax1.set_yticks(np.arange(0, 161, 40))
#ax1.set_title('Orbital Contribution to VBM')

# Plot for 152
ax2.bar(bin_centers, y_152, width=0.02, color='orange', alpha=0.6,
        edgecolor='none')
#ax2.plot(bin_centers, smoothed_152, color='orangered', linewidth=2, linestyle='--', label='Smoothed 152')
ax2.set_ylabel('N (152)')
ax2.set_ylim(0, 10)  # Half of 175
ax2.set_yticks(np.arange(0, 10.1, 2))
#ax2.set_xlabel('O-2p Contribution')

# Grid and legend
ax1.grid(True, linestyle='--', linewidth=0.5)
ax2.grid(True, linestyle='--', linewidth=0.5)

ax1.legend(loc='upper right', frameon=False)
ax2.legend(loc='upper right', frameon=False)

ax2.set_xticks(np.arange(0.0, 0.82, 0.1))

fig.tight_layout()
fig.savefig('Orbital_contribution_separate.pdf')
plt.show()
