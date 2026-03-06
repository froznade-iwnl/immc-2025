from SALib.analyze import sobol
from SALib.sample import saltelli
import numpy as np

# 1. Define the problem
problem = {
    'num_vars': 2,
    'names': ['x', 'y'],
    'bounds': [
        [0.25, 393.55],   # x range
        [98, 19596]    # y range
    ]
}

# 2. Generate samples
N = 1024
param_values = saltelli.sample(problem, N)

# 3. Evaluate the model
def model(x, y):
    return x**2 + 10*y

z = np.array([model(x, y) for x, y in param_values])

# 4. Compute Sobol indices
Si = sobol.analyze(problem, z)

# 5. Print results
print("First-order Sobol indices:")
print(f"S_x = {Si['S1'][0]:.4f}")
print(f"S_y = {Si['S1'][1]:.4f}")
