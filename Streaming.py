import cv2
import time

def resize_frame(frame, target_width, target_height):
    height, width, _ = frame.shape
    aspect_ratio = width / height

    if aspect_ratio > 1:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def stream_and_resize():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    screen_width = int(1920/1.5)  # Set your screen width
    screen_height = int(1080/1.5)  # Set your screen height

    start_time = time.time()
    frame_count = 0
    fps = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("End of video.")
            break

        resized_frame = resize_frame(frame, screen_width, screen_height)
        
        # Calculate the window position for centering
        window_x = int((screen_width - resized_frame.shape[1]) / 2)
        window_y = int((screen_height - resized_frame.shape[0]) / 2)

         # Print fps every 1 second
        elapsed_time = time.time() - start_time
        frame_count += 1
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            start_time = time.time()
            frame_count = 0

        # Put fps information on the frame
        cv2.putText(resized_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Video", resized_frame)
        cv2.moveWindow("Video", window_x, window_y)

        # Break the loop if the 'Esc' key is pressed
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_and_resize()
