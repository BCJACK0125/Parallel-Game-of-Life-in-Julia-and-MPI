import json
import numpy as np
import matplotlib.pyplot as plt


x_axis= np.array([2, 4, 8, 16, 32, 64, 128])
y_axis_29440 = np.array([1.867472137,3.704705232,6.750930658,12.05369323,18.3075603,30.68995418,31.12574096])
y_axis_16000 = np.array([1.830088392,3.574829347,6.373817438,11.58364312,17.44925101,20.2140772,16.69658406])

x = np.array(range(1, 130, 3))
y = 0.85 - x/159 # Communication

# Plotting x_axis_64000 and y_axis_64000 with orange line and points
plt.plot(x_axis, y_axis_29440, '-o', color='red')  # '-o' specifies the line style as a solid line with points and color='orange' sets the line color to orange

# Plotting x_axis_32000 and y_axis_32000 with line and points
plt.plot(x_axis, y_axis_16000, '-o', color='green')  # '-o' specifies the line style as a solid line with points
plt.xlabel('Number of Processor')
plt.ylabel('Speedup')
plt.title('Fixed-size Speedup')

# Add legend at the bottom-right
plt.legend(['m=n=29440', 'm=n=16000'], loc='lower right')

plt.show()


