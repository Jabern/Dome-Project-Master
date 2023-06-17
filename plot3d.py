import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_combinations(n, L, W, Hz, O, max_r_values, min_r=0):
    combinations = 0
    usable_space_list = []
    for k in range(1, n+1):
        for i in range(len(max_r_values)):
            for j in range(i+1, len(max_r_values)):
                max_r_i = max_r_values[i]
                max_r_j = max_r_values[j]
                min_r_i = min_r
                min_r_j = min_r
                prod_term = np.prod([(max_r_values[m] - min_r) / (max_r_values[m] - O*max_r_values[m]) for m in range(i)] + [(max_r_values[m] - min_r) / (max_r_values[m] - O*max_r_values[m]) for m in range(i+1,j)] + [(max_r_values[m] - min_r) / (max_r_values[m] - O*max_r_values[m]) for m in range(j+1,n)])
                usable_space = (4/3) * np.pi * (max_r_i**3 + max_r_j**3) * (1 - O)
                if (L - max_r_i - max_r_j >= 0) and (W - max_r_i - max_r_j >= 0) and (Hz - max_r_i - max_r_j >= 0) and (usable_space >= 10):
                    combinations += np.math.comb(n, k) * ((L - max(max_r_i, max_r_j)) / (max(max_r_i, max_r_j) - O*max(max_r_i, max_r_j))) * ((W - max(max_r_i, max_r_j)) / (max(max_r_i, max_r_j) - O*max(max_r_i, max_r_j))) * ((Hz - max(max_r_i, max_r_j)) / (max(max_r_i, max_r_j) - O*max(max_r_i, max_r_j))) * prod_term
                    usable_space_list.append([max_r_i, max_r_j, usable_space])
    return np.array(usable_space_list)

# Input parameters
n = 10
L = 15
W = 15
Hz = 10
O = 0.1
max_r_values = np.linspace(2, 10, 100)

# Calculate combinations
usable_space_list = calculate_combinations(n, L, W, Hz, O, max_r_values)

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for usable_space in usable_space_list:
    ax.plot([usable_space[0]], [usable_space[1]], [usable_space[2]], 'ro', alpha=0.8, markersize=2)
ax.set_xlabel('Maximum Radius')
ax.set_ylabel('Maximum Radius')
ax.set_zlabel('Usable Space')
plt.show()
