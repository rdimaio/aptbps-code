import subprocess
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import itertools
import os
from scipy import stats
import csv

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, 'data')
ACCS_PATH = os.path.join(DATA_PATH, 'accs')

# Each .csv file has 1200 rows representing the accuracy at each epoch.
# There are 20 columns, each one representing the number of partitions
# used to encode the input dataset.

triangle_fftkde_name = 'triangle-fftkde_mlp.csv'

with open(os.path.join(ACCS_PATH, triangle_fftkde_name)) as fd:
    reader = csv.reader(fd)
    # 1191 -> 1201 because of the header
    last10 = [row for idx, row in enumerate(reader) if idx in np.arange(1191,1201)]
    last10 = np.asarray(last10, dtype=np.float64)

    triangle_fftkde_accs = np.zeros([last10.shape[1]])
    triangle_fftkde_sems = np.zeros([last10.shape[1]])

    for i in range(0, last10.shape[1]): # Iterate over columns (n. of partitions)

        # Get the accuracies of last 10 epochs for that column (n. of partitions)
        last10_curr_col = last10[0:, i]

        triangle_fftkde_accs[i] = np.mean(last10_curr_col)
        triangle_fftkde_sems[i] = stats.sem(last10_curr_col)

comp_fftkde_name = 'comp-fftkde_mlp.csv'

with open(os.path.join(ACCS_PATH, comp_fftkde_name)) as fd:
    reader = csv.reader(fd)
    # 1191 -> 1201 because of the header
    last10 = [row for idx, row in enumerate(reader) if idx in np.arange(1191,1201)]
    last10 = np.asarray(last10, dtype=np.float64)

    comp_fftkde_accs = np.zeros([last10.shape[1]])
    comp_fftkde_sems = np.zeros([last10.shape[1]])

    for i in range(0, last10.shape[1]): # Iterate over columns (n. of partitions)

        # Get the accuracies of last 10 epochs for that column (n. of partitions)
        last10_curr_col = last10[0:, i]

        comp_fftkde_accs[i] = np.mean(last10_curr_col)
        comp_fftkde_sems[i] = stats.sem(last10_curr_col)
    
comp_gkde_name = 'comp-gkde_mlp.csv'

with open(os.path.join(ACCS_PATH, comp_gkde_name)) as fd:
    reader = csv.reader(fd)
    # 1191 -> 1201 because of the header
    last10 = [row for idx, row in enumerate(reader) if idx in np.arange(1191,1201)]
    last10 = np.asarray(last10, dtype=np.float64)

    comp_gkde_accs = np.zeros([last10.shape[1]])
    comp_gkde_sems = np.zeros([last10.shape[1]])

    for i in range(0, last10.shape[1]): # Iterate over columns (n. of partitions)

        # Get the accuracies of last 10 epochs for that column (n. of partitions)
        last10_curr_col = last10[0:, i]

        comp_gkde_accs[i] = np.mean(last10_curr_col)
        comp_gkde_sems[i] = stats.sem(last10_curr_col)

triangle_gkde_name = 'triangle-gkde_mlp.csv'

with open(os.path.join(ACCS_PATH, triangle_gkde_name)) as fd:
    reader = csv.reader(fd)
    # 1191 -> 1201 because of the header
    last10 = [row for idx, row in enumerate(reader) if idx in np.arange(1191,1201)]
    last10 = np.asarray(last10, dtype=np.float64)

    triangle_gkde_accs = np.zeros([last10.shape[1]])
    triangle_gkde_sems = np.zeros([last10.shape[1]])

    for i in range(0, last10.shape[1]): # Iterate over columns (n. of partitions)

        # Get the accuracies of last 10 epochs for that column (n. of partitions)
        last10_curr_col = last10[0:, i]

        triangle_gkde_accs[i] = np.mean(last10_curr_col)
        triangle_gkde_sems[i] = stats.sem(last10_curr_col)

bps_name = 'bps_mlp.csv'

with open(os.path.join(ACCS_PATH, bps_name)) as fd:
    reader = csv.reader(fd)
    # 1191 -> 1201 because of the header
    last10 = [row for idx, row in enumerate(reader) if idx in np.arange(1191,1201)]
    last10 = np.asarray(last10, dtype=np.float64)

    bps_acc = np.mean(last10)
    bps_sem = stats.sem(last10)

fig, ax = plt.subplots()
ax.set_title("Accuracy by number of partitions", weight='bold')

ax.yaxis.grid(True, color='#EEEEEE')
fig.tight_layout()
ax.set_ylabel("Accuracy (%)")
ax.set_xlabel("Number of partitions")

marker = itertools.cycle((',', '^', 's', 'D', 'o')) 
linestyle = itertools.cycle(("-","--","-.",(0, (3, 1, 1, 1))))

x = np.arange(0, 19)

# BPS data
plt.axhline(y=bps_acc, color='b', linestyle='dotted', label="bps MLP", marker=next(marker))
plt.errorbar(0, bps_acc, yerr=bps_sem,capsize=5)

# APTBPS data
plt.errorbar(x, triangle_gkde_accs, linestyle=next(linestyle), yerr=triangle_gkde_sems, marker='o', markersize=4, capsize=5, label="triangle-gkde MLP")
plt.errorbar(x, comp_gkde_accs, linestyle=next(linestyle), marker='o', yerr=comp_gkde_sems, markersize=4, capsize=5, label="comp-gkde MLP")
plt.errorbar(x, triangle_fftkde_accs,yerr=triangle_fftkde_sems, linestyle=next(linestyle), marker='o', markersize=4, capsize=5, label="triangle-fftkde MLP")
plt.errorbar(x, comp_fftkde_accs, yerr=comp_fftkde_sems, linestyle=next(linestyle), marker='o', markersize=4, capsize=5, label="comp-fftkde MLP")

plt.xticks(np.arange(len(triangle_fftkde_accs)), np.arange(2, len(triangle_fftkde_accs)+2))
plt.grid(linestyle='--')
plt.legend(loc="upper right")
plt.show()

print("values: ")

print("bps mean acc:")
print(bps_acc)
print("bps sem:")
print(bps_sem)

print("triangle gkde mean accs:")
print(triangle_gkde_accs)
print("triangle gkde sems:")
print(triangle_gkde_sems)

print("comp gkde mean accs:")
print(comp_gkde_accs)
print("comp gkde sems:")
print(comp_gkde_sems)

print("triangle fftkde mean accs:")
print(triangle_fftkde_accs)
print("triangle fftkde sems:")
print(triangle_fftkde_sems)

print("comp fftkde mean accs:")
print(comp_fftkde_accs)
print("comp fftkde sems:")
print(comp_fftkde_sems)