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
y_axis_comm = np.array([0.111,
                        0.989,
                        3.811,
                        3.271,
                        2.451,
                        2.089,
                        2.434
                        ])

x = np.array(range(1, 130, 3))
y = (1/4.5) * np.sqrt(x)  # Communication

# # Create the first plot
# fig, ax1 = plt.subplots()
# ax1.plot(x_axis, y_axis_sync, '-o', color='green')
# ax1.set_xlabel('Number of Processor')
# ax1.set_ylabel('Sync/Comm ratio')
# ax1.tick_params(axis='y')
# ax1.legend(['Sync/Comm ratio on m=n=16000'], loc='lower right')
# plt.title('Sync/Comm ratio vs # Processors')

# Create the second plot
fig, ax2 = plt.subplots()
ax2.plot(x_axis, y_axis_comm, '-o', color='red')
ax2.plot(x, y, '--', color='blue')

ax2.set_xlabel('Number of Processor')
ax2.set_ylabel('Comm/Comp ratio')
ax2.tick_params(axis='y')

ax2.legend(['Comm/Comp ratio on m=n=3200', r'$\frac{\sqrt{P}}{N}$ ($\frac{Communication}{Computation}$)'], loc='upper right')

plt.title('Comm/Comp ratio vs # Processors')
plt.show()
