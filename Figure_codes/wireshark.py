import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = '/Users/benjaminnweke/Library/CloudStorage/OneDrive-UniversityofWyoming/wireshark/wireshark.xlsx'
df_raw = pd.read_excel(file_path)

# Extract Fabric and Besu data
fabric = df_raw.iloc[:, [0, 1, 2]].copy()
fabric.columns = ['Packet Count', 'Time (s)', 'Packet Size (Bytes)']
fabric['Blockchain'] = 'Fabric'

besu = df_raw.iloc[:, [3, 4, 5]].copy()
besu.columns = ['Packet Count', 'Time (s)', 'Packet Size (Bytes)']
besu['Blockchain'] = 'Besu'

# Combine and clean
df = pd.concat([fabric, besu], ignore_index=True)
df = df.dropna()
df['Packet Count'] = pd.to_numeric(df['Packet Count'], errors='coerce')
df['Time (s)'] = pd.to_numeric(df['Time (s)'], errors='coerce')
df['Packet Size (Bytes)'] = pd.to_numeric(df['Packet Size (Bytes)'], errors='coerce')
df.dropna(inplace=True)

# Create 10-second time bins
df['Time Bin'] = (df['Time (s)'] // 10) * 10

# Define consistent color map
color_map = {'Fabric': '#0072B2', 'Besu': '#D55E00'}

# Set up figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# (a) Boxplot - Packet Count per Time Bin
sns.boxplot(data=df, x='Time Bin', y='Packet Count', hue='Blockchain',
            palette=color_map, ax=ax1)
ax1.set_title('(a) Packet Count per 10-Second Interval', fontsize=14)
ax1.set_xlabel('Time (s) [10s bins]', fontsize=14)
ax1.set_ylabel('Packet Count', fontsize=14)
ax1.tick_params(axis='both', labelsize=14)
ax1.legend(title='Blockchain', fontsize=14, title_fontsize=14, loc='upper left')
ax1.set_ylim(bottom=0)
ax1.grid(True, linestyle='--', alpha=0.5)

# (b) Bar Chart - Average Packet Size with Standard Deviation
grouped = df.groupby('Blockchain')['Packet Size (Bytes)']
means = grouped.mean()
stds = grouped.std()
labels = means.index.tolist()
values = means.values
errors = stds.values
colors = [color_map[label] for label in labels]

bars = ax2.bar(labels, values, yerr=errors, capsize=10, color=colors)
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, height + 20, f'{height:.1f}',
             ha='center', va='bottom', fontsize=14)

# Add a manual legend for consistency
for label, color in color_map.items():
    ax2.bar(0, 0, color=color, label=label)  # invisible bars just for legend
ax2.legend(title='Blockchain', fontsize=14, title_fontsize=14, loc='upper left')

ax2.set_title('(b) Average Packet Size with Standard Deviation', fontsize=14)
ax2.set_ylabel('Packet Size (Bytes)', fontsize=14)
ax2.tick_params(axis='both', labelsize=14)
ax2.set_ylim(bottom=0)
ax2.grid(True, axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("network_analysis_combined_consistent_legend.png", dpi=300, bbox_inches='tight')
plt.show()
