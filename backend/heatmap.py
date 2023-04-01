import numpy as np
import numpy.random
import matplotlib.pyplot as plt

'''
# Generate some test data
x = np.random.randn(8873)
y = np.random.randn(8873)

heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.show()
'''

def generateHeatmap(size):
    # Create a numpy array to store the heatmap
    heatmap = np.zeros((size, size))

    # Choose the coordinates of the hot point
    x = np.random.randint(size/4, size*3/4)
    y = np.random.randint(size/4, size*3/4)

    # Create arrays of x and y coordinates for each point in the heatmap
    x_coords, y_coords = np.meshgrid(range(size), range(size))

    # Calculate the distances between each point and the hot point
    distances = np.sqrt((x_coords - x)**2 + (y_coords - y)**2)

    # Create a smooth heat distribution around the hot point
    sigma = np.sqrt(size)
    heatmap = np.exp(-((distances**2)/(2*sigma**2)))

    # Normalize the heatmap so that the maximum value is 1
    heatmap /= np.max(heatmap)

    # Add some noise to the heatmap
    noise_std = size**0.4 / 100
    noise = np.random.normal(loc=0, scale=noise_std, size=(size, size))
    heatmap += noise

    # Clip the heatmap values to the range [0, 1]
    heatmap = np.clip(heatmap, 0, 1)
    return heatmap

if __name__ == "__main__":
    heatmap = generateHeatmap(50)

    # Display the heatmap using matplotlib
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()