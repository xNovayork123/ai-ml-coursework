#!/usr/bin/env python3

# A quick script to load the training data for the Vacuum World
# Shows the different classes found and plots the shape of the distributions
#

import sys
import numpy as np
import matplotlib.pyplot as plt

USAGE = f"""Usage:
    {sys.argv[0]} <training_data_file>

Examples:
    {sys.argv[0]} training_set1.dat
    cat training_set1.dat | {sys.argv[0]}

Input format:
    CSV file where the final column is the class label.
"""

# Determine input source
if len(sys.argv) > 1:
    data_source = sys.argv[1]
elif not sys.stdin.isatty():
    data_source = sys.stdin
else:
    print(USAGE, file=sys.stderr)
    sys.exit(1)

# Load data
data = np.loadtxt(
    data_source,
    delimiter=",",
    dtype=str,
    skiprows=1
)

X = data[:, :-1].astype(float)
y = data[:, -1]

classes = sorted(set(y))
x_axis = np.arange(1, X.shape[1] + 1)

# Create a 3x3 grid of subplots
fig, axes = plt.subplots(3, 3, figsize=(18, 18))
fig.canvas.manager.set_window_title("Vacuum World Training Data")
fig.suptitle('Dirt Probability Distributions by Class', fontsize=16, y=1.02)

# Flatten the axes array for easy iteration
axes = axes.ravel()

for i, cls in enumerate(classes):
    idx = (y == cls)
    subset = X[idx]

    ax = axes[i]

    # Plot all samples (light scatter)
    for row in subset:
        ax.scatter(x_axis, row, s=10, alpha=0.25)

    # Compute and plot mean (bold line)
    mean_curve = np.mean(subset, axis=0)
    ax.plot(x_axis, mean_curve, linewidth=3, marker="o")

    ax.set_title(f"Class: {cls}", pad=12)
    ax.set_xlabel("Room Index")
    ax.set_ylabel("Dirt Probability")
    ax.set_xticks(x_axis)
    ax.set_ylim(0, np.max(X) * 1.05)

# Hide any unused subplots (if there are fewer than 9 classes)
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

# Adjust vertical spacing
plt.subplots_adjust(hspace=0.4)

plt.show()
