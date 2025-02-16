# Paul Blackhurst, OSU, Feb 2025
#
# This script reads in the data from an FDM model in Excel
# and creates an animation to help visualize the results.
# It creates a plot for every row in the data and saves each
# plot to a folder. It then uses imageio to compile all of
# the plots into a GIF animation.

# Import Libraries
import os
import matplotlib.pyplot as plt
import pandas as pd
import imageio as io
import numpy as np

# Specify the time and space increment used in FDM model.
dt = 0.5
dx = 0.009
# GIF frames per second
fpsec = 20

# Specify the width of the model in the excel sheet (how long is each row?).
model_width = 501

title = '1D FDM Heat Conduction' # Title displayed on animation

# Path to where the excel file is stored.
data_path = '/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/2D_data_anim_manual/1D_FDM_rfssw.xlsx'

# Path to folder where you want to save the plots.
plots_save_path = '/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/2D_data_anim_manual/plots'

# Read in the data from the excel file, specifying how many rows and columns to skip to get to the data.
data = pd.read_excel(data_path, header=None, usecols=range(2, 503), skiprows=8, sheet_name='500_nodes_cond_fix')

# Generate x-axis values using list comprehension syntax. Uses dx defined above. Assumes 0 is in the middle.
middle_index = model_width // 2
x = []
for i in range(model_width):
       x.append((i - middle_index) * dx)
x = np.array(x)

# j is an iterator for printing the save progress to the terminal.
j=0

# This for-loop generates a plot for each row of data in the excel file. Other plot details specified as well.
for i in range(len(data.iloc[0])):
    fig, ax = plt.subplots() # Create figure and plotting area.
    row = data.iloc[i] # Grabs the current row of data.

    # References max and min values in the data to create axis limits.
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(data.min().min(), data.max().max())

    ax.set_title(title) # Create title.

    # Plot the data, specify axis labels.
    ax.plot(x, row, label='heat distribution', color='tab:blue',
            marker='o', linestyle='solid', linewidth=0.5, markersize=1)
    ax.set_xlabel('Distance (m)', color = 'black')
    ax.set_ylabel('Temperature (C)', color='black')
    
    # Create time stamp for current dt.
    time_stamp = ax.text(0.95, 0.95, f"t = {dt*j} s", transform=ax.transAxes, ha='right', va='top')

    # Save the plot in folder specified above.
    save_path = os.path.join(plots_save_path, f"plot_{i:03d}.png")
    fig.savefig(save_path, dpi=300)

    # Print plot saving progress to terminal.
    print(f"Saved Plot {i:03d}")
    j += 1

# Create a list of image files
image_files = []
for f in os.listdir(plots_save_path):
        if f.endswith('.png'):
              image_files.append(f)
image_files.sort()

# Specify where to save GIF
output_gif = f'/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/2D_data_anim_manual/gif_{fpsec}fps.gif'

# j is an iterator for printing the save progress to the terminal.
i = 0

# Create an imageio GIF object, iterate through and append every png plot
# mode = "I" for gifs, mode = "V" for video files (needs ffmpeg arg)
with io.get_writer(output_gif, mode='I', fps = fpsec) as writer:
        for file in image_files:
                image_path = os.path.join(plots_save_path, file)
                image = io.imread(image_path)
                writer.append_data(image)
                i += 1
                print(f"Appended Image {i:03d}")

print(f"GIF saved to {output_gif}")