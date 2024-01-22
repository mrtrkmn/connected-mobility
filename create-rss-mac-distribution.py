import subprocess
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

# Specify the path to your capture file
cap_file_path = '<pcap-file.pcap>'


# Use tshark to extract MAC addresses and signal strengths
tshark_command = [
    'tshark',
    '-r', cap_file_path,
    '-Y', 'wlan.fc.type_subtype == 0x04',  # Filter for probe requests
    '-T', 'fields', '-e', 'wlan.sa', '-e', 'wlan_radio.signal_dbm'
]

# Run tshark and capture output
result = subprocess.run(tshark_command, capture_output=True, text=True)
output_lines = result.stdout.strip().split('\n')

# Parse tshark output into a DataFrame
data = [line.split() for line in output_lines]
df = pd.DataFrame(data, columns=['MAC Address', 'Signal Strength'])
df['Signal Strength'] = df['Signal Strength'].astype(int)

# Create a bar graph with enhanced visibility
plt.figure(figsize=(15, 8))
sns.barplot(x='MAC Address', y='Signal Strength', data=df, palette='viridis', saturation=0.75, ci=None)
plt.title('Signal Strength Distribution for MAC Addresses')
plt.xlabel('MAC Address')
plt.ylabel('Signal Strength (dBm)')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()  # Adjust layout for better visibility
plt.show()
