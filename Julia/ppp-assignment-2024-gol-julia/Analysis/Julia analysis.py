import json
import numpy as np
import matplotlib.pyplot as plt

# List of filenames
test = [32000, 64000]

serial_64000 = [80.08023500442505, 69.91987109184265, 65.187509059906, 73.50810384750366]
list_of_filenames = [(1,2,2), (2,2,2), (2,4,2), (4,4,4), (4,8,8), (8,8,8), (8,16,8)]

filenames = []
x_axis_64000 = []
for (a,b,c) in list_of_filenames:
    x_axis_64000.append(a*b)
    for i in range(1, 5):
        filename = f"parallel_gun_64000_64000_{a}_{b}_{c}_10_0_run_{i}.json"
        filenames.append(filename)

value = []
y_axis_64000 = []
count = 0
for filename in filenames:    
    with open(filename, "r") as file:
        data = json.load(file)

    # Access the value you need from the JSON data
    value.append(max(data["wall_time"]))
    count += 1

    # Do something with the value
    if count % 4 == 0:
        y_axis_64000.append((sum(serial_64000)/len(serial_64000))/min(value))
        # print(min(value))
        value = []
# print(y_axis_64000)
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
        y_axis_32000.append((sum(serial_32000)/len(serial_32000))/min(value))
        # print(min(value))
        value = []
print(y_axis_32000)



# Plotting x_axis_64000 and y_axis_64000 with orange line and points
plt.plot(x_axis_64000, y_axis_64000, '-o', color='red')  # '-o' specifies the line style as a solid line with points and color='orange' sets the line color to orange

# Plotting x_axis_32000 and y_axis_32000 with line and points
plt.plot(x_axis_32000, y_axis_32000, '-o', color='green')  # '-o' specifies the line style as a solid line with points

plt.xlabel('Number of Processor')
plt.ylabel('Speedup')
plt.title('Fixed-size Speedup')

# Add legend at the bottom-right
plt.legend(['m=n=64000', 'm=n=32000'], loc='lower right')

plt.show()


