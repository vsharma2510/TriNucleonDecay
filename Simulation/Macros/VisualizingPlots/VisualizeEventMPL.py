import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Create a random 3D array and a corresponding double value array
array_3d = np.random.rand(5, 5, 5)
double_values = np.random.rand(5, 5, 5)

# Get the dimensions of the array
depth, height, width = array_3d.shape

# Define spacing between cubes
cube_spacing = 0.2

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a colormap
cmap = cm.get_cmap('jet')

# Iterate over each element in the array
for z in range(depth):
    for y in range(height):
        for x in range(width):
            # Get the coordinates of the point
            x_point = x
            y_point = y
            z_point = z

            # Get the color based on the double value
            color = cmap(double_values[z, y, x])

            # Plot the point
            ax.scatter(x_point, y_point, z_point, color=color)

            # Calculate the coordinates for the cube
            x_cube = x_point - 0.5 + cube_spacing / 2
            y_cube = y_point - 0.5 + cube_spacing / 2
            z_cube = z_point - 0.5 + cube_spacing / 2

            # Plot the cube
            ax.bar3d(
                x_cube, y_cube, z_cube,
                1 - cube_spacing, 1 - cube_spacing, 1 - cube_spacing,
                color='gray', alpha=0.2
            )

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Array Visualization with Points and Cubes')

# Set the aspect ratio to be equal
ax.set_box_aspect([1, 1, 1])

# Show the plot
plt.show()
