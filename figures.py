from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
import data

# This is my first example of a simply correlational analysis of wildfires and precipitation in Colorado from 1992-2015
# It includes line charts of yearly totals, a 3-year rolling-average of those numbers, and a scatter plot depicting
# the relationship between precipitation and fire incidence, with a linear regression identifying a negative
# correlation between precipitation and


red = 'tab:red'
blue = 'tab:blue'
# Set variables for plot element colors
fig = plt.figure()
# Establishes the figure object
fig.set_tight_layout(True)
# Provides convenient figure formatting
ax1 = fig.add_subplot(311)
# Creates a chart within the figure
ax1.plot(data.years, data.fires, color = red)
# Instantiates the plot of total fires per year
ax1.set_xlabel('Year')
ax1.set_ylabel('# of Fires')
# Sets labels
ax2 = ax1.twinx()
# Creates another axis object and matches it with the previous plot's x axis
ax2.plot(data.years, data.avgPrecip, color = blue)
ax2.set_ylabel('Precipitation')

ax3 = fig.add_subplot(312)
ax3.scatter(data.rain, data.fires)
fire_fit = np.polyfit(data.rain, data.fires, 1)
# Create line of best fit for rain v fire plot
plt.plot(data.rain, fire_fit[0]*data.rain+fire_fit[1], color = red)
# Instantiates a plot within the scatter including that line of best fit
plt.xlabel('Precipitation')
plt.ylabel('# of Fires')
# Set labels for the scatter plot

ax4 = fig.add_subplot(313)
ax4.plot(data.years, data.rolling_3, color = red)
ax5 = ax4.twinx()
ax5.plot(data.years, data.r_rolling_3, color = blue)

plt.show()
plt.close()

fig = plt.figure(figsize = [7, 7])
ax = fig.add_subplot(111)
table = ax.table(cellText = data.tableData, loc = 'center')
table.set_fontsize(10)
table.scale(1,1.5)
ax.axis('off')
plt.show()