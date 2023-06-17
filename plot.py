import math
import pandas as pd
import matplotlib.pyplot as plt

def n_choose_k(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def generate_dome_combinations(num_domes, L, W, Hz, max_radius, overlap):
    min_radius = 0
    step_size = 0.01
    radius_range = [i * step_size for i in range(int(min_radius/step_size), int(max_radius/step_size) + 1)]
    rows = []
    for k in range(1, num_domes+1):
        combinations = n_choose_k(num_domes, k)
        for radius in radius_range:
            if radius == 0:
                continue
            L_term = (L - radius) / (radius - overlap * radius)
            W_term = (W - radius) / (radius - overlap * radius)
            Hz_term = (Hz - radius) / (radius - overlap * radius)
            product_term = math.prod([(radius - min_radius) / (radius - overlap * radius) for i in range(k)])
            row = {
                'num_domes': num_domes,
                'k': k,
                'radius': radius,
                'combinations': combinations,
                'L_term': L_term,
                'W_term': W_term,
                'Hz_term': Hz_term,
                'product_term': product_term,
                'total': combinations * L_term * W_term * Hz_term * product_term
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    return df

num_domes = 100
L = 15
W = 15
Hz = 10
max_radius = 3.00
overlap = 0.05

df = generate_dome_combinations(num_domes, L, W, Hz, max_radius, overlap)
total_combinations = df['total'].sum()

print(f"Total Combinations: {total_combinations}")

plt.plot(df['radius'], df['total'], 'bo')
plt.xlabel('Radius (m)')
plt.ylabel('Total Combinations')
plt.show()

print(df)
