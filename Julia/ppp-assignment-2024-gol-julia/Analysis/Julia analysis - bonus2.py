import json
import numpy as np
import matplotlib.pyplot as plt

# List of filenames
test = [32000, 64000]

serial_16000 = [80.08023500442505, 69.91987109184265, 65.187509059906, 73.50810384750366]
list_of_filenames = [(1,2,2), (2,2,2), (2,4,2), (4,4,4), (4,8,8), (8,8,8), (16, 8,8)]

filenames = []
x_axis_16000 = []
for (a,b,c) in list_of_filenames:
    x_axis_16000.append(a*b)
    for i in range(1, 5):
        filename = f"parallel_gun_16000_16000_{a}_{b}_{c}_10_0_run_{i}.json"
        filenames.append(filename)

value = []
y_axis_16000 = []
y_axis_16000_2 = [17.0265,
8.7165,
4.88875,
2.69,
1.78575,
1.5415,
1.86625,
]


count = 0
for filename in filenames:    
    with open(filename, "r") as file:
        data = json.load(file)

    # Access the value you need from the JSON data
    value.append(max(data["wall_time"]))
    count += 1

    # Do something with the value
    if count % 4 == 0:
        y_axis_16000.append(min(value))
        # print(min(value))
        value = []
print(y_axis_16000)
# print(sum(serial_64000)/len(serial_64000))

serial_32000 = [12.213973999023438, 12.200830936431885, 12.21374797821045, 12.207705020904541]
list_of_filenames = [(1,2,2), (2,2,2), (2,4,2), (4,4,4), (4,8,8), (8,8,8), (8,16,8)]

filenames = []
x_axis_32000 = []
for (a,b,c) in list_of_filenames:
    x_axis_32000.append(a*b)
    for i in range(1, 5):
        filename = f"parallel_gun_32000_32000_{a}_{b}_{c}_10_0_run_{i}.json"
        filenames.append(filename)

value = []
y_axis_32000 = []
count = 0
for filename in filenames:    
    with open(filename, "r") as file:
        data = json.load(file)

    # Access the value you need from the JSON data
    value.append(max(data["wall_time"]))
    count += 1

    # Do something with the value
    if count % 4 == 0:
        y_axis_32000.append(min(value))
        # print(min(value))
        value = []
# print(y_axis_32000)
y_axis_32000_2 = [22,
12.1705,
6.9345,
4.2865,
3.1935,
1.859,
197.176
]



# Plotting x_axis_64000 and y_axis_64000 with orange line and points
# plt.plot(x_axis_64000, y_axis_64000, '-o', color='red')  # '-o' specifies the line style as a solid line with points and color='orange' sets the line color to orange

# Plotting x_axis_32000 and y_axis_32000 with line and points
plt.plot(x_axis_32000, y_axis_32000, '-o', color='green')  # '-o' specifies the line style as a solid line with points
plt.plot(x_axis_32000, y_axis_32000_2, '-o', color='red')  # '-o' specifies the line style as a solid line with points and color='orange' sets the line color to orange

plt.xlabel('Number of Processor')
plt.ylabel('Time (s)')
plt.title('Comparison of execution time (m=n=32000, step=10)')

# Add legend at the bottom-right
plt.legend(['Julia', 'C + MPI'], loc='upper left')

plt.show()


