import cv2

cap = cv2.VideoCapture("rtsp://admin:xckj2024@192.168.1.64:554/h264/ch1/sub/av_stream")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("video/object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()