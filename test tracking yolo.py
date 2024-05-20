import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = r"C:\Users\lilap\OneDrive\Documents\Master ETHZ\ARSL Semester Project\Test videos\2nd Setup cavity_pump\0.4ml_sec.avi"
cap = cv2.VideoCapture(0)

# Define a class mapping dictionary
class_mapping = {
    0: 'Michael Jackson', # The key is the class id, you may need to adjust according to your model
    # Add more mappings as needed
}


# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)
        # Replace class names with custom labels in the results
        for result in results:
            for cls_id, custom_label in class_mapping.items():
                if cls_id in result.names: # check if the class id is in the results
                    result.names[cls_id] = custom_label # replace the class name with the custom label

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()