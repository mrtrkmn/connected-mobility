import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the path to your capture file
cap_file_path = 'data/<path-to-pcap-file>.pcap'

# Use tshark to extract probe requests' source-destination pairs and packet sizes
tshark_command = [
    'tshark',
    '-r', cap_file_path,
    '-Y', 'wlan.fc.type_subtype == 0x04',  # Filter for probe requests
    '-T', 'fields', '-e', 'wlan.sa', '-e', 'wlan.da', '-e', 'frame.len'
]

# Run tshark and capture output
result = subprocess.run(tshark_command, capture_output=True, text=True)
output_lines = result.stdout.strip().split('\n')

# Parse tshark output into a DataFrame
data = [line.split() for line in output_lines]
df = pd.DataFrame(data, columns=['Source', 'Destination', 'Packet Size'])

# Convert 'Packet Size' column to integers
df['Packet Size'] = pd.to_numeric(df['Packet Size'], errors='coerce')

# Get the top 20 source-destination pairs based on packet size
top_pairs = df.groupby(['Source', 'Destination']).sum()['Packet Size'].nlargest(20).reset_index()

# Create a heatmap for the top 20 pairs
heatmap_data = top_pairs.pivot_table(values='Packet Size', index='Source', columns='Destination', aggfunc='mean')
plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f', linewidths=.5)
plt.title('Heatmap of Top 20 Source-Destination Pairs based on Probe Request Packet Sizes')
plt.xlabel('Destination MAC Address')
plt.ylabel('Source MAC Address')
plt.show()