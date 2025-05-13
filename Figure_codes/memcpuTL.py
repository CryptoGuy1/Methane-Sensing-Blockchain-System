import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Color-blind friendly palette
colors = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7']

# Fabric resource data
fabric_resource = {
    'Transaction Number': [1000]*5 + [5000]*5 + [10000]*5 + [20000]*5 + [30000]*5,
    'Load': [100, 500, 1000, 5000, 10000]*5,
    'Memory (MB)': [49.52, 54.93, 58.89, 60.89, 67.57,
                    84.3, 88.92, 92.47, 99.18, 101.98,
                    78.05, 99.93, 102.05, 105.76, 110.74,
                    125.58, 131.08, 133.58, 142.41, 152.25,
                    127.86, 133.15, 140.3, 155.67, 183.15],
    'CPU (%)': [0.0006, 0.0007, 0.0008, 0.0008, 0.0010,
                0.0144, 0.0265, 0.0302, 0.0308, 0.0311,
                0.0202, 0.0307, 0.0354, 0.0396, 0.0457,
                0.0242, 0.0356, 0.0557, 0.0592, 0.0611,
                0.03, 0.0472, 0.0587, 0.0609, 0.0633]
}

# Besu resource data
besu_resource = {
    'Transaction Number': [1000]*5 + [1500]*5 + [2000]*5 + [2500]*5 + [3000]*5 + [4000]*5,
    'Load': [100, 500, 1000, 5000, 10000]*6,
    'Memory (MB)': [0.79, 0.80, 0.86, 0.90, 0.92,
                    1.89, 2.08, 2.13, 2.22, 2.37,
                    2.90, 2.98, 3.07, 3.15, 3.24,
                    3.61, 3.88, 3.94, 4.17, 4.25,
                    3.76, 4.05, 4.22, 4.35, 4.42,
                    3.87, 4.19, 4.27, 4.38, 4.82],
    'CPU (%)': [4.43, 4.71, 5.06, 5.16, 5.24,
                4.43, 4.99, 5.23, 5.45, 5.55,
                4.42, 5.11, 5.54, 6.25, 7.62,
                4.80, 5.25, 5.72, 6.26, 6.40,
                5.37, 5.55, 6.06, 7.27, 8.71,
                7.39, 8.50, 9.07, 11.24, 13.24]
}

fabric_df = pd.DataFrame(fabric_resource)
besu_df = pd.DataFrame(besu_resource)

# Function to plot grouped bar chart
def plot_resource(ax, df, metric, ylabel, label, xlabel='Transaction Number'):
    loads = sorted(df['Load'].unique())
    txn_nums = sorted(df['Transaction Number'].unique())
    index = np.arange(len(txn_nums))
    bar_width = 0.12

    for i, load in enumerate(loads):
        values = [df[(df['Transaction Number'] == txn) & (df['Load'] == load)][metric].values[0] 
                  if not df[(df['Transaction Number'] == txn) & (df['Load'] == load)].empty else np.nan 
                  for txn in txn_nums]
        ax.bar(index + i * bar_width, values, width=bar_width, label=f'Load {load}', color=colors[i % len(colors)])

    ax.set_xticks(index + bar_width * (len(loads)-1) / 2)
    ax.set_xticklabels(txn_nums, rotation=45)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.text(-0.1, 1.05, label, transform=ax.transAxes, fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), title='Tx Load')

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=300)
labels = ['(a)', '(b)', '(c)', '(d)']

# Plotting each chart
plot_resource(axes[0, 0], fabric_df, 'Memory (MB)', 'Memory Usage (MB)', labels[0])
plot_resource(axes[0, 1], besu_df, 'Memory (MB)', 'Memory Usage (MB)', labels[1])
plot_resource(axes[1, 0], fabric_df, 'CPU (%)', 'CPU Usage (%)', labels[2])
plot_resource(axes[1, 1], besu_df, 'CPU (%)', 'CPU Usage (%)', labels[3])

# Add centered column headers without any box or border
fig.text(0.25, 0.965, 'Fabric', ha='center', va='bottom', fontsize=14, fontweight='bold')
fig.text(0.75, 0.965, 'Besu', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Adjust layout to make room for the headers
plt.tight_layout(rect=[0, 0, 1, 0.93])


plt.tight_layout()
plt.savefig("resource_usage_comparison.png", dpi=300, bbox_inches='tight')
plt.show()

