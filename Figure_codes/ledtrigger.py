import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# LED trigger times for Fabric and Besu
fabric_trigger_times = [
    344, 351, 350, 320, 344, 342, 343, 328, 345, 350,
    328, 342, 348, 320, 351, 355, 326, 326, 349, 355,
    351, 328, 327, 353, 355, 322, 343, 346, 342, 342,
    344, 327, 335, 341, 323, 326, 341, 353, 345, 323,
    352, 347, 349, 346, 340, 335, 353, 346, 340, 330
]

besu_trigger_times = [
    422, 417, 456, 403, 445, 392, 419, 489, 491, 493,
    487, 395, 505, 486, 422, 411, 467, 478, 501, 476,
    443, 432, 475, 398, 507, 481, 412, 406, 504, 501,
    393, 404, 427, 456, 432, 505, 435, 449, 458, 504,
    447, 507, 469, 501, 484, 401, 501, 441, 401, 396
]

# Create a DataFrame for plotting
df = pd.DataFrame({
    'Trigger Time (ms)': fabric_trigger_times + besu_trigger_times,
    'Blockchain': ['Hyperledger Fabric']*50 + ['Hyperledger Besu']*50
})

# Set the figure
plt.figure(figsize=(10, 6), dpi=300)

# Plot the violin plot
sns.violinplot(data=df, x='Blockchain', y='Trigger Time (ms)',
               palette={'Hyperledger Fabric': 'blue', 'Hyperledger Besu': 'red'})

# Improve appearance
plt.ylim(300, 550)
plt.ylabel("Trigger Time (ms)")

# Save the figure
plt.savefig("trigger_time_violin_plot.png", dpi=300, bbox_inches='tight')
plt.show()
