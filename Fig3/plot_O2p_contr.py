import pandas as pd
import matplotlib.pyplot as plt

# 1. Load CSV, skipping the spurious second‐line header if still present
df = pd.read_csv(
    'Data_sorted_60_order.csv',
    header=0,
    skiprows=[1]    # remove the "1,Formula,O-2p,Classify" dummy row
)

# 2. Ensure numeric types
df['No']       = pd.to_numeric(df['No'],      errors='raise', downcast='integer')
df['O-2p']     = pd.to_numeric(df['O-2p'],    errors='raise')
df['Classify'] = pd.to_numeric(df['Classify'],errors='raise', downcast='integer')

# 3. Marker mapping
marker_map = {
    1: 's',   # square
    0: '+',   # plus
    2: '^',   # triangle
    3: '*'    # star
}

# 4. Plot
fig, ax = plt.subplots(figsize=(10, 4))
for cls, marker in marker_map.items():
    sub = df[df['Classify'] == cls]
    ax.scatter(sub['No'], sub['O-2p'],
               marker=marker, s=100,
               label=f'Classify {cls}')

ax.set_xlabel('No')
ax.set_ylabel('O-2p contribution at VBM')
ax.set_xlim(df['No'].min() - 1, df['No'].max() + 1)
ax.legend(title='Classify', loc='upper right')
plt.tight_layout()

# 5. Save as EPS
plt.savefig('O2p_contr.eps', format='eps', bbox_inches='tight')
