import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Read data from the text file
file_path = 'captured-data-devices.txt'  # Replace with your actual file path
data = []
with open(file_path, 'r') as file:
    for line in file:
        if line.startswith('#'):
            continue
        mac, strength = line.strip().split()
        data.append((mac, int(strength)))

# Create a DataFrame
df = pd.DataFrame(data, columns=['MAC Address', 'Signal Strength'])

# Select the top 20 MAC addresses based on signal strength
top_n = 20
top_df = df.sort_values(by='Signal Strength', ascending=False).head(top_n)

# Create a heatmap
plt.figure(figsize=(15, 8))
heatmap = top_df.pivot_table(index='MAC Address', columns='Signal Strength', aggfunc='size', fill_value=0)
sns.heatmap(heatmap, cmap='YlGnBu', annot=True, fmt='g', linewidths=.5)
plt.title(f'MAC Addresses - Signal Strength Distribution')
plt.show()
