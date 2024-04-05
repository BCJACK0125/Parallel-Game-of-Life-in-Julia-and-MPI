import numpy as np
import matplotlib.pyplot as plt

# Define the function and its derivative
def sqrt_derivative(x):
    return 1 / (2 * np.sqrt(x))

# Generate x values
x_values = np.array([2, 4, 8, 16, 32, 64, 128])

# Calculate y values
# y_values = sqrt_derivative(x_values)
# y_values2 = np.sqrt(x_values)
N = 10
y_values = N/np.sqrt(x_values)
y_values2 = N*N/x_values

# Plot the derivative
plt.plot(x_values, y_values, '-o', label=r'Communication $\frac{N}{\sqrt{P}}$, N=10')
plt.plot(x_values, y_values2, '-o', label=r'Computation  $\frac{N*N}{P}$, N=10')
plt.xlabel('x')
plt.ylabel('y')
plt.title('# Computation & Communication vs # Processors')
plt.legend()
plt.grid(True)

# Find the point where y_values == y_values2
equal_points = np.where(y_values == y_values2)
for point in equal_points:
    plt.plot(x_values[point], y_values[point], 'ro', label='Equal Point')

plt.show()
