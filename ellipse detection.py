import matplotlib.pyplot as plt
import cv2

from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

# Load picture, convert to grayscale and detect edges
# image_gray = cv2.imread('Test videos\\4th Setup phantom_transducer\\2_transducer_1_5V_2\\frame_0000.png', cv2.IMREAD_GRAYSCALE)
image_gray = cv2.imread('ellipse_test.png', cv2.IMREAD_GRAYSCALE)

edges = canny(image_gray, sigma=2.0,
              low_threshold=0.55, high_threshold=0.8)

plt.imshow(edges)
plt.show()
# Perform a Hough Transform
# The accuracy corresponds to the bin size of a major axis.
# The value is chosen in order to get a single high accumulator.
# The threshold eliminates low accumulators
result = hough_ellipse(edges, accuracy=20, threshold=250,
                       min_size=100, max_size=120)
print('viebibviev')
result.sort(order='accumulator')
print(result)
# Estimated parameters for the ellipse
best = list(result[-1])
yc, xc, a, b = (int(round(x)) for x in best[1:5])
orientation = best[5]

# Draw the ellipse on the original image
cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
image_gray[cy, cx] = (0, 0, 255)
# Draw the edge (white) and the resulting ellipse (red)
edges = color.gray2rgb(img_as_ubyte(edges))
edges[cy, cx] = (250, 0, 0)

fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True)

ax1.set_title('Original picture')
ax1.imshow(image_gray)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)

plt.show()