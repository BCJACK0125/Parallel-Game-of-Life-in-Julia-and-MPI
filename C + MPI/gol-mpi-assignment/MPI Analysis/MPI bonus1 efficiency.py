import json
import numpy as np
import matplotlib.pyplot as plt


x_axis= np.array([2, 4, 8, 16, 32, 64, 128])
y_axis_29440 = np.array([0.933736069,0.926176308,0.843866332,0.753355827,0.572111259,0.479530534,0.243169851])
y_axis_hiding = np.array([0.956929596,0.94531615,0.855105469,0.778769041,0.658400079,0.552511065,0.257480477])

x = np.array(range(1, 130, 3))
y = 0.93 - x/180 # Communication

# Plotting x_axis_64000 and y_axis_64000 with orange line and points
plt.plot(x_axis, y_axis_29440, '-o', color='green')  # '-o' specifies the line style as a solid line with points and color='orange' sets the line color to orange

# Plotting x_axis_32000 and y_axis_32000 with line and points
plt.plot(x_axis, y_axis_hiding, '-o', color='red')  # '-o' specifies the line style as a solid line with points

plt.plot(x, y, '--', color='blue')

plt.xlabel('Number of Processor')
plt.ylabel('Efficiency')
plt.title('Latency Hiding Efficiency Analysis (m=n=29440)')

# Add legend at the bottom-right
plt.legend(['Synchronous', 'Latency Hiding', r'Derivative of  $\frac{P}{N}$ ($\frac{Communication}{Computation}$)'], loc='upper right')

plt.show()


