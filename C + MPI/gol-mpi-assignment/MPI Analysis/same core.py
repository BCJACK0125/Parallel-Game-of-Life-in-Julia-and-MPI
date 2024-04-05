import matplotlib.pyplot as plt

# Sample data
names1 = ['(16, 1)', '(8, 2)', '(4, 4)', '(2, 8)', '(1, 16)']
names2 = ['(16, 1)', '(8, 2)', '(4, 4)', '(2, 8)', '(1, 16)']
values1 = [40.0995, 8.933, 8.531333333, 9.00175, 8.765]
values2 = [3.1505, 2.948, 2.69, 2.764, 2.735]

# Plotting the histograms
bar_width = 0.35  # Width of each bar
index = range(len(names1))  # x-axis values

plt.bar(index, values1, width=bar_width, label='m=n=29440, steps=32')
plt.bar([i + bar_width for i in index], values2, width=bar_width, label='m=n=16000, steps=32')

# Labeling the axes
plt.xlabel('Pair of (Cores per node, # Nodes)')
plt.ylabel('Wall Time (s)')

# Adding a legend
plt.legend()

# Adjusting the x-axis ticks and labels
plt.xticks([i + bar_width/2 for i in index], names1)

# Adding index labels on top of the bars
sorted_values1 = sorted(values1)
sorted_values2 = sorted(values2)
for i, v in enumerate(values1):
    index_label = sorted_values1.index(v)
    plt.text(i, v, 'NO.'+str(index_label+1), ha='center', va='bottom')
for i, v in enumerate(values2):
    index_label = sorted_values2.index(v)
    plt.text(i + bar_width, v, 'NO.'+str(index_label+1), ha='center', va='bottom')

# Displaying the plot
plt.show()
