import pandas as pd
import matplotlib.pyplot as plt

# Load Excel data
file_path = '/Users/benjaminnweke/Library/CloudStorage/OneDrive-UniversityofWyoming/wireshark/energy_fabric&besu.xlsx'
df = pd.read_excel(file_path, header=1)

# Rename columns for clarity
df.columns = [
    'Fabric_ActivePower', 'Fabric_ApparentPower', 'Fabric_PF',
    'Besu_ActivePower', 'Besu_ApparentPower', 'Besu_PF'
]

# Create a time axis assuming 30-minute intervals
time_axis = [i * 0.5 for i in range(len(df))]  # in hours

# Set font size globally
plt.rcParams.update({'font.size': 14})

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, dpi=300)

# Plot (a) Active Power
ax1.plot(time_axis, df['Fabric_ActivePower'], label='Fabric', color='#0072B2', linewidth=2)
ax1.plot(time_axis, df['Besu_ActivePower'], label='Besu', color='#D55E00', linewidth=2)
ax1.set_ylabel('Active Power (W)')
ax1.set_title('(a) Active Power over Time')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# Plot (b) Apparent Power
ax2.plot(time_axis, df['Fabric_ApparentPower'], label='Fabric', color='#0072B2', linewidth=2)
ax2.plot(time_axis, df['Besu_ApparentPower'], label='Besu', color='#D55E00', linewidth=2)
ax2.set_ylabel('Apparent Power (VA)')
ax2.set_xlabel('Time (hours)')
ax2.set_title('(b) Apparent Power over Time')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

# Final layout
plt.tight_layout()
plt.savefig("energy_time_series_plot_fixed.png", dpi=300, bbox_inches='tight')
plt.show()

