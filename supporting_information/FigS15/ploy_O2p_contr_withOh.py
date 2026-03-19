import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv('Data_formula_list_2nd.csv', header=None)
df.columns = ['Formula', 'O_2p_O', 'O_2p_Oh']
df['Index'] = range(1, len(df) + 1)

# 2. Convert to numeric to fix string issue
df['O_2p_O'] = pd.to_numeric(df['O_2p_O'], errors='coerce')
df['O_2p_Oh'] = pd.to_numeric(df['O_2p_Oh'], errors='coerce')

# 3. Compute common y-axis range
y_min = min(df['O_2p_O'].min(), df['O_2p_Oh'].min()) - 0.02
y_max = max(df['O_2p_O'].max(), df['O_2p_Oh'].max()) + 0.02

# 4. Plot
fig, ax = plt.subplots(figsize=(12, 5))

# Scatter plots
ax.scatter(df['Index'], df['O_2p_O'], marker='o', s=100, label='O-2p with O')
ax.scatter(df['Index'], df['O_2p_Oh'], marker='*', s=100, label='O-2p with Oₕ')

# Common y-axis
ax.set_ylim(y_min, y_max)

# Axes labels and ticks
ax.set_xlabel('Formula')
ax.set_ylabel('O-2p contribution at VBM')
ax.set_xticks(df['Index'])
ax.set_xticklabels(df['Formula'], rotation=45, ha='right')
ax.legend(title='Type', loc='upper right')
plt.tight_layout()

# 5. Save plot
plt.savefig('O2p_contr_O_Oh_with_formula_fixed.eps', format='eps', bbox_inches='tight')
plt.show()

