import cv2
import os
import tkinter as tk
from tkinter import ttk
import time


refPt = []
final_boundaries = []
image = []


class ButtonWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Button Window")

        # Initialize the result variable
        self.result = None

        # Create style for buttons
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))

        # Create buttons
        btn1 = ttk.Button(self.root, text="Create ROI", command=lambda: self.on_button_click(1))
        btn1.pack(pady=10)

        btn2 = ttk.Button(self.root, text="Record directly", command=lambda: self.on_button_click(2))
        btn2.pack(pady=10)

        # Center the window on the screen
        self.center_window()

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the centered window
        x = (screen_width - self.root.winfo_reqwidth()) // 2
        y = (screen_height - self.root.winfo_reqheight()) // 2

        # Set the window's geometry
        self.root.geometry(f"+{x}+{y}")

    def on_button_click(self, button_number):
        # Set the result and close the window
        self.result = button_number
        self.root.destroy()
        self.root.quit()

    def show_window(self):
        self.root.mainloop()


def click_and_crop(event, x, y, flags, param):
    global refPt, image, final_boundaries
    
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        final_boundaries.append((refPt[0], refPt[1]))
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("Select Rectangle", image)
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        clone = image.copy()
        cv2.rectangle(clone, refPt[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("Select Rectangle", clone)

def select_ROI(video_source=0):
    global image
    # Open a video capture object
    cap = cv2.VideoCapture(video_source)

    # Check if the video capture object is successfully opened
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    # Read a frame from the video source
    ret, frame = cap.read()
    image = frame.copy()

    #Fit the whole image to the screen
    max_display_height = 800
    if image.shape[0] > max_display_height:
        scale_factor = max_display_height / image.shape[0]
        image = cv2.resize(image, (int(image.shape[1] * scale_factor), max_display_height))
    else:
        scale_factor = 1
    #Create a window for the rectangle selection
    cv2.namedWindow("Select Rectangle")
    cv2.setMouseCallback("Select Rectangle", click_and_crop)
    cv2.imshow("Select Rectangle", image)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

    # Print the coordinates of the selected rectangles
    if final_boundaries:
        print("Selected Rectangles:")
        for i, boundaries in enumerate(final_boundaries):
            print(f"Rectangle {i + 1}:", "Top-left:", boundaries[0], "Bottom-right:", boundaries[1])
        # Get back the coordinates in the right scale
        pt1 = int(boundaries[0][1]/scale_factor), int(boundaries[0][0]/scale_factor)
        pt2 = int(boundaries[1][1]/scale_factor), int(boundaries[1][0]/scale_factor)
    else:
        print("No rectangles selected.")
        pt1, pt2 = None, None
    
    return pt1, pt2
def record_video(output_folder, video_source=0, frame_prefix='frame', frame_extension='png', pt1=None, pt2=None):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open a video capture object
    cap = cv2.VideoCapture(video_source)

    # Check if the video capture object is successfully opened
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    frame_number = 0

    start_time = time.time()

    while True:
        # Read a frame from the video source
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break
        
        if pt1 is not None and pt2 is not None:
            frame = frame[pt1[1]:pt2[1], pt1[0]:pt2[0]]

        # Save the frame as a numbered PNG file
        frame_filename = f"{frame_prefix}_{frame_number:04d}.{frame_extension}"
        frame_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(frame_path, frame)

        frame_number += 1

        # Display the captured frame (optional)
        cv2.imshow('Video Recording', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close any open windows
    cap.release()
    cv2.destroyAllWindows()
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    #Video Setup 
    output_folder = "Test videos/12th Setup Bifurcation/1_5_mL_min_piezo_1MHz_10Vpp"
    video_source = 0

    #Launch the button window
    button_window = ButtonWindow()
    button_window.show_window()
    # Get the result after the window is closed
    result = button_window.result
    if result==1:
        pt1, pt2 = select_ROI(video_source)
        record_video(output_folder, video_source, pt1=pt1, pt2=pt2)
    else:
        record_video(output_folder, video_source)