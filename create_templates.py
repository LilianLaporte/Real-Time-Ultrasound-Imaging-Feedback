import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Global variables
rectangles = []
cropped_images_folder = "cropped_images"

def on_click(event):
    global rectangles
    if event.button == 1:  # Left mouse button
        rectangles.append((event.xdata, event.ydata))
    elif event.button == 3:  # Right mouse button
        if rectangles:
            x1, y1 = rectangles[-1]
            x2, y2 = event.xdata, event.ydata
            rectangles[-1] = ((x1, y1), (x2, y2))
            rect = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='g', facecolor='none')
            ax.add_patch(rect)
            plt.draw()

# Create the cropped images folder
os.makedirs(cropped_images_folder, exist_ok=True)

# Load the image
image = plt.imread("Test videos/11th Setup Piezo 1Mhz Silicium/Side_on_off_20Vpp_2/frame_0090.png")

# Display the image
fig, ax = plt.subplots()
ax.imshow(image)
plt.title("Draw rectangles (Left click to start, Right click to end)")

# Connect the mouse click event to the function
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()

# Crop and save the images
for i, (pt1, pt2) in enumerate(rectangles):
    x1, y1 = int(pt1[0]), int(pt1[1])
    x2, y2 = int(pt2[0]), int(pt2[1])
    cropped_image = image[y1:y2, x1:x2]
    plt.imsave(os.path.join(cropped_images_folder, f"cropped_image_{i}.jpg"), cropped_image)
