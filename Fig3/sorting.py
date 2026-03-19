import pandas as pd

# 1. Load the original data (no header line)
df = pd.read_csv('Data_sorted_60.csv', names=['Formula','O-2p','Classify'])

# 2. Sort descending by O-2p
df_sorted = df.sort_values('O-2p', ascending=False)

# 3. Save to new CSV, same format (no header, no index)
df_sorted.to_csv('Data_sorted_60_order.csv',
                 header=False,
                 index=False)
