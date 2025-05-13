import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Use color-blind friendly palette
colors = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7']

# Data for Fabric
fabric_data = {
    'Transaction Number': [1000]*5 + [5000]*5 + [10000]*5 + [20000]*5 + [30000]*5,
    'TAR': [100, 500, 1000, 5000, 10000]*5,
    'Avg Latency (s)': [0.01, 0.03, 0.04, 0.055, 0.067,
                        0.01, 0.04, 0.05, 0.059, 0.07,
                        0.03, 0.04, 0.06, 0.066, 0.077,
                        0.038, 0.048, 0.071, 0.077, 0.08,
                        0.04, 0.05, 0.075, 0.088, 0.11],
    'Send Rate (TPS)': [141.9, 509.2, 557.1, 563.1, 573.1,
                        150, 515.8, 622.8, 630.9, 633.5,
                        170.1, 520.5, 640.5, 647.5, 655.1,
                        186.5, 532, 647.7, 655.9, 661.2,
                        192.5, 541.1, 648.1, 659.3, 665.5],
    'Throughput (TPS)': [110.3, 250.3, 261.8, 262.7, 468.5,
                         123.5, 426.3, 497.6, 502.6, 504.1,
                         144.4, 456.1, 566.8, 572.4, 578.4,
                         154.3, 477.7, 607.9, 615.1, 619.8,
                         157.7, 484.8, 610.2, 625.4, 628.6]
}

# Data for Besu
besu_data = {
    'Transaction Number': [1000]*5 + [1500]*5 + [2000]*5 + [2500]*5 + [3000]*5 + [4000]*5,
    'TAR': [100, 500, 1000, 5000, 10000]*6,
    'Avg Latency (s)': [3.68, 3.72, 3.73, 3.75, 3.82,
                        3.99, 4.13, 4.14, 4.14, 4.24,
                        4.2, 4.39, 4.41, 4.63, 4.73,
                        4.6, 4.65, 4.73, 4.79, 4.83,
                        5.2, 5.34, 5.37, 5.43, 5.55,
                        6.07, 6.19, 6.26, 6.33, 6.57],
    'Send Rate (TPS)': [1428.6, 1477.1, 1540.8, 1572.3, 1610.3,
                        1632.2, 1639.3, 1657.5, 1842.8, 1893.9,
                        1821.5, 1890.4, 2002, 2026.3, 2047.1,
                        2064.4, 2120.4, 2149.6, 2272.7, 2497.5,
                        2161.4, 2279.6, 2298.9, 2358.5, 2535.9,
                        2542.9, 2575.7, 2597.4, 2638.5, 2708.2],
    'Throughput (TPS)': [244.2, 245.5, 248.8, 262.5, 282.3,
                         317.3, 321.7, 322.4, 325.9, 336.7,
                         388.8, 390.1, 392.7, 394.3, 399.1,
                         393.1, 392.5, 395.5, 398.9, 402.7,
                         394, 396.5, 399.8, 399.7, 405.7,
                         420.1, 422.9, 423.2, 429.9, 433.0]
}

fabric_df = pd.DataFrame(fabric_data)
besu_df = pd.DataFrame(besu_data)

# Function to plot grouped bars
def plot_grouped(ax, df, metric, ylabel, label, xlabel='Transaction Number'):
    loads = sorted(df['TAR'].unique())
    txn_nums = sorted(df['Transaction Number'].unique())
    index = np.arange(len(txn_nums))
    bar_width = 0.12

    for i, load in enumerate(loads):
        values = [df[(df['Transaction Number'] == txn) & (df['TAR'] == load)][metric].values[0] 
                  if not df[(df['Transaction Number'] == txn) & (df['TAR'] == load)].empty else np.nan 
                  for txn in txn_nums]
        ax.bar(index + i * bar_width, values, width=bar_width, label=f'TAR {load}', color=colors[i % len(colors)])

    ax.set_xticks(index + bar_width * (len(loads)-1) / 2)
    ax.set_xticklabels(txn_nums, rotation=45)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.text(-0.1, 1.05, label, transform=ax.transAxes, fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), title='TAR')

# Create figure and axes
fig, axes = plt.subplots(3, 2, figsize=(16, 12), dpi=300)
labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# Fabric column
plot_grouped(axes[0, 0], fabric_df, 'Avg Latency (s)', 'Avg Latency (s)', labels[0])
plot_grouped(axes[1, 0], fabric_df, 'Throughput (TPS)', 'Throughput (TPS)', labels[2])
plot_grouped(axes[2, 0], fabric_df, 'Send Rate (TPS)', 'Send Rate (TPS)', labels[4])

# Besu column
plot_grouped(axes[0, 1], besu_df, 'Avg Latency (s)', 'Avg Latency (s)', labels[1])
plot_grouped(axes[1, 1], besu_df, 'Throughput (TPS)', 'Throughput (TPS)', labels[3])
plot_grouped(axes[2, 1], besu_df, 'Send Rate (TPS)', 'Send Rate (TPS)', labels[5])

# Add centered column headers without any box or border
fig.text(0.25, 0.965, 'Fabric', ha='center', va='bottom', fontsize=14, fontweight='bold')
fig.text(0.75, 0.965, 'Besu', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Adjust layout to make room for the headers
plt.tight_layout(rect=[0, 0, 1, 0.93])


plt.tight_layout()
plt.savefig("tar_scalability_benchmark.png", dpi=300, bbox_inches='tight')
plt.show()

