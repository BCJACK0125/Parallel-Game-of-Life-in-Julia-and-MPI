import json
import numpy as np
import matplotlib.pyplot as plt

# List of filenames
names1 = ['(16, 1)', '(8, 2)', '(4, 4)', '(2, 8)', '(1, 16)']
names2 = ['(16, 1)', '(8, 2)', '(4, 4)', '(2, 8)', '(1, 16)']

list_of_filenames = [1,2,4,8,16]

filenames = []
for k in list_of_filenames:
    for i in range(1, 5):
        filename = f"parallel_gun_24000_24000_4_4_{k}_10_0_run_{i}.json"
        filenames.append(filename)

value = []
y_axis_24000 = []
count = 0
for filename in filenames:    
    with open(filename, "r") as file:
        data = json.load(file)

    # Access the value you need from the JSON data
    value.append(max(data["wall_time"]))
    count += 1

    # Do something with the value
    if count % 4 == 0:
        y_axis_24000.append(min(value))
        # print(min(value))
        value = []
print(y_axis_24000)
# print(sum(serial_64000)/len(serial_64000))

filenames = []
for k in list_of_filenames:
    for i in range(1, 5):
        filename = f"parallel_gun_50000_50000_4_4_{k}_10_0_run_{i}.json"
        filenames.append(filename)

value = []
y_axis_50000 = []
count = 0
for filename in filenames:    
    with open(filename, "r") as file:
        data = json.load(file)

    # Access the value you need from the JSON data
    value.append(max(data["wall_time"]))
    count += 1

    # Do something with the value
    if count % 4 == 0:
        y_axis_50000.append(min(value))
        # print(min(value))
        value = []
# print(y_axis_50000)



# Plotting the histograms
bar_width = 0.35  # Width of each bar
index = range(len(names1))  # x-axis values

plt.bar(index, y_axis_24000, width=bar_width, label='m=n=24000')
plt.bar([i + bar_width for i in index], y_axis_50000, width=bar_width, label='m=n=50000')

# Labeling the axes
plt.xlabel('Pair of (Cores per node, # Nodes)')
plt.ylabel('Wall Time (s)')

# Adding a legend
plt.legend()

# Adjusting the x-axis ticks and labels
plt.xticks([i + bar_width/2 for i in index], names1)

# Adding index labels on top of the bars
sorted_values1 = sorted(y_axis_24000)
sorted_values2 = sorted(y_axis_50000)
for i, v in enumerate(y_axis_24000):
    index_label = sorted_values1.index(v)
    plt.text(i, v, 'NO.'+str(index_label+1), ha='center', va='bottom')
for i, v in enumerate(y_axis_50000):
    index_label = sorted_values2.index(v)
    plt.text(i + bar_width, v, 'NO.'+str(index_label+1), ha='center', va='bottom')

# Displaying the plot
plt.show()


