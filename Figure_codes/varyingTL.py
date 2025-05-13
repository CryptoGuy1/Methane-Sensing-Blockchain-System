import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Color-blind–friendly palette
colors = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7']

# Fabric benchmark data
fabric_data = {
    'Transaction Number': [1000]*5 + [5000]*5 + [10000]*5 + [20000]*5 + [30000]*5,
    'Transaction Load': [100, 500, 1000, 5000, 10000]*5,
    'Avg Latency (s)': [0.02, 0.04, 0.05, 0.06, 0.09,
                        0.04, 0.05, 0.07, 0.097, 0.107,
                        0.04, 0.08, 0.088, 0.104, 0.11,
                        0.05, 0.077, 0.11, 0.18, 0.187,
                        0.07, 0.09, 0.17, 0.23, 0.5],
    'Send Rate (TPS)': [176.4, 561.5, 566.3, 573.1, 579.7,
                        203.2, 641.6, 646.8, 650.3, 656.2,
                        207, 643, 649.3, 667.1, 677.2,
                        213.1, 643.7, 655.3, 660, 665,
                        223.1, 647.1, 661.4, 677.7, 684.3],
    'Throughput (TPS)': [130, 516.8, 531.6, 554.3, 566.1,
                         187.8, 519.4, 542.6, 559.1, 614.5,
                         194.1, 553.3, 573.9, 588, 620.5,
                         208.7, 586.7, 596.9, 601.1, 624.3,
                         218.7, 595.6, 605.8, 608.3, 626.7]
}
fabric_df = pd.DataFrame(fabric_data)

# Besu benchmark data
besu_data = {
    'Transaction Number': [1000]*5 + [1500]*5 + [2000]*5 + [2500]*5 + [3000]*5 + [4000]*5,
    'Transaction Load': [100, 500, 1000, 5000, 10000]*6,
    'Avg Latency (s)': [3.48, 3.64, 3.68, 3.77, 3.78,
                        4.1, 4.18, 4.22, 4.42, 4.53,
                        4.41, 4.61, 4.71, 4.85, 4.88,
                        4.52, 4.65, 4.69, 4.86, 4.89,
                        5.21, 5.26, 5.38, 5.43, 5.53,
                        5.91, 6.19, 6.32, 6.41, 6.56],
    'Send Rate (TPS)': [1432.7, 1567.4, 1610.3, 1721.2, 1890.4,
                        1674.1, 1787.8, 1824.8, 1870.3, 1984.1,
                        1872.7, 1885, 1901.1, 2053.4, 2145.9,
                        1973.2, 2000, 2085.1, 2147.8, 2198.8,
                        2228.8, 2364.1, 2377.2, 2431.1, 2487.6,
                        2433.1, 2489.1, 2551, 2737.9, 2801.1],
    'Throughput (TPS)': [241.4, 246.7, 257.3, 287.5, 303.4,
                         320.8, 322.2, 326, 345.4, 352.2,
                         355.9, 379.9, 386.4, 391.9, 393.9,
                         362.3, 390.7, 392.5, 396.8, 399.4,
                         359.6, 391.7, 394.1, 399.5, 413.5,
                         413.2, 419.1, 428.7, 430.5, 452.7]
}
besu_df = pd.DataFrame(besu_data)

# Plotting function
def plot_grouped_bar(ax, df, metric, ylabel, label):
    loads = sorted(df['Transaction Load'].unique())
    txn_numbers = sorted(df['Transaction Number'].unique())
    bar_width = 0.12
    index = np.arange(len(txn_numbers))

    for i, load in enumerate(loads):
        values = []
        for txn in txn_numbers:
            row = df[(df['Transaction Number'] == txn) & (df['Transaction Load'] == load)]
            values.append(row[metric].values[0] if not row.empty else np.nan)
        ax.bar(index + i * bar_width, values, width=bar_width, label=f'Load {load}', color=colors[i % len(colors)])
    
    ax.set_xticks(index + bar_width * (len(loads)-1) / 2)
    ax.set_xticklabels(txn_numbers, rotation=45)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Transaction Number')
    ax.text(-0.1, 1.05, label, transform=ax.transAxes, fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), title='Tx Load')

# Create subplots
fig, axes = plt.subplots(3, 2, figsize=(16, 12), dpi=300)
labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# Fabric Plots
plot_grouped_bar(axes[0, 0], fabric_df, 'Avg Latency (s)', 'Avg Latency (s)', labels[0])
plot_grouped_bar(axes[1, 0], fabric_df, 'Throughput (TPS)', 'Throughput (TPS)', labels[2])
plot_grouped_bar(axes[2, 0], fabric_df, 'Send Rate (TPS)', 'Send Rate (TPS)', labels[4])

# Besu Plots
plot_grouped_bar(axes[0, 1], besu_df, 'Avg Latency (s)', 'Avg Latency (s)', labels[1])
plot_grouped_bar(axes[1, 1], besu_df, 'Throughput (TPS)', 'Throughput (TPS)', labels[3])
plot_grouped_bar(axes[2, 1], besu_df, 'Send Rate (TPS)', 'Send Rate (TPS)', labels[5])

# Add centered column headers without any box or border
fig.text(0.25, 0.965, 'Fabric', ha='center', va='bottom', fontsize=14, fontweight='bold')
fig.text(0.75, 0.965, 'Besu', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Adjust layout to make room for the headers
plt.tight_layout(rect=[0, 0, 1, 0.93])

plt.tight_layout()
plt.savefig("fabric_besu_plot_labeled_clean.png", dpi=300, bbox_inches='tight')
plt.show()
