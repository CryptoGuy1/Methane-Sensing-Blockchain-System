import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Fabric Data
fabric_data = {
    'Transaction Number': [1000]*5 + [5000]*5 + [10000]*5 + [20000]*5 + [30000]*5,
    'TAR': [100, 500, 1000, 5000, 10000]*5,
    'Memory': [
        98.93, 107.53, 109.12, 111.34, 121.43,
        105.48, 106.63, 112.12, 115.30, 124.63,
        105.76, 110.74, 111.68, 122.70, 130.86,
        107.83, 115.58, 119.58, 125.58, 139.13,
        107.13, 117.06, 121.13, 134.13, 150.13
    ],
    'CPU': [
        0.00065, 0.00077, 0.00083, 0.00091, 0.00107,
        0.00917, 0.01530, 0.02048, 0.02988, 0.03131,
        0.01607, 0.0181, 0.0295, 0.0305, 0.03211,
        0.0175, 0.0281, 0.0395, 0.04233, 0.05726,
        0.022, 0.02899, 0.043, 0.05, 0.061
    ]
}

# Besu Data
besu_data = {
    'Transaction Number': [1000]*5 + [1500]*5 + [2000]*5 + [2500]*5 + [3000]*5 + [4000]*5,
    'TAR': [100, 500, 1000, 5000, 10000]*6,
    'Memory': [
        0.79, 0.82, 0.89, 0.91, 1.03,
        1.88, 1.94, 2.03, 2.11, 2.53,
        2.46, 2.69, 3.00, 3.09, 3.12,
        3.27, 3.49, 3.76, 3.82, 4.32,
        3.55, 4.05, 4.16, 4.25, 4.42,
        3.85, 4.12, 4.23, 4.33, 5.13
    ],
    'CPU': [
        4.3, 4.61, 4.95, 5.26, 5.37,
        4.23, 4.66, 5.01, 5.31, 5.39,
        4.32, 4.88, 5.14, 5.36, 5.87,
        4.37, 5.38, 5.51, 5.64, 6.4,
        4.53, 5.72, 6.16, 6.7, 8.36,
        7.52, 8.86, 9.29, 11.29, 11.89
    ]
}

fabric_df = pd.DataFrame(fabric_data)
besu_df = pd.DataFrame(besu_data)

# Setup plot
fig, axs = plt.subplots(2, 2, figsize=(16, 10), dpi=300)
labels = ['(a)', '(b)', '(c)', '(d)']
colors = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7']

def plot_grouped_bars(ax, df, metric, ylabel, label):
    tar_values = sorted(df['TAR'].unique())
    txn_numbers = sorted(df['Transaction Number'].unique())
    index = np.arange(len(txn_numbers))
    bar_width = 0.12

    for i, tar in enumerate(tar_values):
        values = [df[(df['Transaction Number'] == txn) & (df['TAR'] == tar)][metric].values[0]
                  if not df[(df['Transaction Number'] == txn) & (df['TAR'] == tar)].empty else np.nan
                  for txn in txn_numbers]
        ax.bar(index + i * bar_width, values, width=bar_width, label=f'TAR {tar}', color=colors[i % len(colors)])

    ax.set_xticks(index + bar_width * (len(tar_values) - 1) / 2)
    ax.set_xticklabels(txn_numbers, rotation=45)
    ax.set_ylabel(ylabel)
    ax.text(-0.1, 1.05, label, transform=ax.transAxes, fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), title='TAR')

# Plot the graphs
plot_grouped_bars(axs[0, 0], fabric_df, 'Memory', 'Memory Usage (MB)', labels[0])
plot_grouped_bars(axs[0, 1], besu_df, 'Memory', 'Memory Usage (MB)', labels[1])
plot_grouped_bars(axs[1, 0], fabric_df, 'CPU', 'CPU Usage (%)', labels[2])
plot_grouped_bars(axs[1, 1], besu_df, 'CPU', 'CPU Usage (%)', labels[3])

# Add centered column headers without any box or border
fig.text(0.25, 0.965, 'Fabric', ha='center', va='bottom', fontsize=14, fontweight='bold')
fig.text(0.75, 0.965, 'Besu', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Adjust layout to make room for the headers
plt.tight_layout(rect=[0, 0, 1, 0.93])


plt.tight_layout()
plt.savefig("resource_usage_by_tar.png", dpi=300, bbox_inches='tight')
plt.show()
