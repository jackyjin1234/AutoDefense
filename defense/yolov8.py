import cv2
import torch
from torchvision import transforms
from ultralytics import YOLO, solutions

model = YOLO("yolov8m.pt")
cap = cv2.VideoCapture("rtsp://admin:xckj2024@192.168.1.64:554")
# cap = cv2.VideoCapture("rtsp://admin:123456@192.168.1.254:554/mpeg4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define region points
region_points = [(700, 10), (800,10), (800, 400), (700, 400)]
classes_to_count = [0]

# Video writer
video_writer = cv2.VideoWriter("video/object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init Object Counter
counter = solutions.ObjectCounter(
    view_img=True,
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=True,
    line_thickness=2,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    # im0 = transforms.Compose([transforms.ToTensor(), transforms.Resize((640, 1280))])(im0)
    tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()