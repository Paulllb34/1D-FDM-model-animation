# Paul Blackhurst, 2024
#
# This script reads in the data from an FDM model in Excel
# and creates an animation to help visualize the results.
# It uses a function (update) to update the frame for each
# row in the data, and then uses the matplotlib.animation
# module to create the animation.

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Path to excel file
path = "/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/2D_data_anim_func/1D_FDM_rfssw.xlsx"

# Read in excel file with FDM model
data = pd.read_excel(path, header=None, usecols=range(2, 503), skiprows=8, sheet_name='500_nodes_cond_fix')

# Generate x-axis values using list comprehension syntax
length = 501
middle_index = length // 2
increment = 0.01
x = np.array([(i - middle_index) * increment for i in range(length)])

# Plot, axis limits based on data
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(x.min(), x.max())
ax.set_ylim(data.min().min(), data.max().max())

# Plot labels, grid, title
plt.xlabel('Location (m)')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.title('RFSSW - 9mm toolset')

# Initialize the text annotation for the time stamp
time_stamp = ax.text(0.95, 0.95, '', transform=ax.transAxes, ha='right', va='top')

# Animation update function
def update(frame):
    # Get the data for the current frame (row)
    current_data = data.iloc[frame, :724]

    # Update the line plot with the new data
    line.set_data(x, current_data)  # Use x-axis values defined earlier

    # Update the time stamp
    time = frame * 0.25  # Each row is 0.25 seconds apart
    time_stamp.set_text('Time Stamp: {:.1f} s'.format(time))

    return line, time_stamp

# Create the animation
anim = animation.FuncAnimation(fig, update, frames=len(data), interval=50, blit=True)

# Save the animation as a GIF file
anim.save('/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/2D_data_anim_func/gif2.gif', writer='pillow')

# Display the animation
plt.show()