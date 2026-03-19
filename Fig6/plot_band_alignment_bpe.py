import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------- 1. read & re‑reference energies ---------- #
cols = ["Formula", "VBM", "CBM", "BPE"]          # header row in the screenshot
df   = pd.read_csv("oxides_pbe_nvb6_ncb3.dat",
                   sep=r"\s+",
                   names=cols,
                   skiprows=1)                   # first row is the header you showed

# shift so that BPE (PBE reference) = 0 eV
df["VBM_shift"] = df["VBM"] - df["BPE"]
df["CBM_shift"] = df["CBM"] - df["BPE"]

vbm = df["VBM_shift"].to_numpy()
cbm = df["CBM_shift"].to_numpy()

# ---------- 2. plotting ---------- #
fig, ax = plt.subplots(figsize=(4.5, 4.5))

x     = np.arange(len(df))
width = 0.8

# choose y‑limits that cover everything with a bit of margin
ymin  = np.floor(min(vbm.min(), -2)) - 0.5     # ↓ floor so bars aren’t clipped
ymax  = np.ceil (max(cbm.max(),  6)) + 0.5     # ↑ ceil  …

vb_color = "#9999ff"        # valence‑band fill
cb_color = "#ff9999"        # conduction‑band fill

# valence band (bottom‑coloured)
ax.bar(x,
       vbm - ymin,          # bar height
       width=width,
       bottom=ymin,
       color=vb_color,
       edgecolor="black")

# conduction band (top‑coloured)
ax.bar(x,
       ymax - cbm,
       width=width,
       bottom=cbm,
       color=cb_color,
       edgecolor="black")

# ---------- 3. cosmetics ---------- #
ax.axhline(0,  color="black", linestyle="--", linewidth=1,
           label="PBE reference (0 eV)")        # PBE zero line

ax.set_xticks(x)
ax.set_xticklabels(df["Formula"], rotation=90, fontsize=8)

ax.set_ylabel("Energy (eV)")
ax.set_title("Band alignment referenced to PBE", fontsize=14)
ax.set_xlim([-1, len(df)])
ax.set_ylim([ymin, ymax])
ax.grid(axis="y", linestyle=":", color="gray")

plt.tight_layout()
plt.savefig("band_alignment_pbe6_3.eps", format="eps", dpi=300)
plt.show()
