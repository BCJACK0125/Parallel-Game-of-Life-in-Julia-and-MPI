import numpy as np
import matplotlib.pyplot as plt

x_axis = np.array([2, 4, 8, 16, 32, 64, 128])
y_axis_sync = np.array([0.003014286,
                        0.281106604,
                        0.253363895,
                        0.336218182,
                        1.14523,
                        2.093702871,
                        0.951556684
                        ])
y_axis_comm = np.array([0.004144464,
                        0.012368728,
                        0.098661485,
                        0.110044018,
                        0.110957004,
                        0.21132457,
                        0.462299135
                        ])

x = np.array(range(1, 130, 3))
y = (1/275) * x -0.008  # Communication

# Create the first plot
fig, ax1 = plt.subplots()
ax1.plot(x_axis, y_axis_sync, '-o', color='green')
ax1.set_xlabel('Number of Processor')
ax1.set_ylabel('Sync/Comm ratio')
ax1.tick_params(axis='y')
ax1.legend(['Sync/Comm ratio on m=n=16000'], loc='lower right')
plt.title('Sync/Comm ratio vs # Processors')

# Create the second plot
fig, ax2 = plt.subplots()
ax2.plot(x_axis, y_axis_comm, '-o', color='red')
ax2.plot(x, y, '--', color='blue')

ax2.set_xlabel('Number of Processor')
ax2.set_ylabel('Comm/Comp ratio')
ax2.tick_params(axis='y')

ax2.legend(['Comm/Comp ratio on m=n=16000', r'$\frac{P}{N}$ ($\frac{Communication}{Computation}$)'], loc='lower right')

plt.title('Comm/Comp ratio vs # Processors')
plt.show()
