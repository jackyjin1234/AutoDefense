import cv2
import yolov3_person_detect as yolov3
from RTSCapture import RTSCapture

# cap = cv2.VideoCapture(
#     "rtsp://admin:xckj2024@192.168.1.178:554/h264/ch1/sub/av_stream")
# ret, frame = cap.read()
# cv2.namedWindow('192.168.1.178', 0)
# # cv2.resizeWindow('192.168.1.178', 500, 300)
# # 使用，展示
# while ret:
#     ret, frame = cap.read()
#     cv2.imshow('192.168.1.178', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# # 退出时释放窗口和内存
# cv2.destroyAllWindows()
# cap.release()

weights_path = "yolov3.weights"
config_path = "yolov3.cfg"
class_file_path = "coco.names"

net = yolov3.load_yolo_model(weights_path, config_path)
classes = yolov3.load_classes(class_file_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# cap = cv2.VideoCapture(
#     "rtsp://admin:xckj2024@192.168.1.178:554/h264/ch1/sub/av_stream")
# ret, frame = cap.read()
# cv2.namedWindow('Video Stream', 0)

rtscap = RTSCapture.create(
    "rtsp://admin:xckj2024@192.168.1.178:554/h264/ch1/sub/av_stream")
rtscap.start_read()  # 启动子线程并改变 read_latest_frame 的指向

while rtscap.isStarted():
    ret, frame = rtscap.read_latest_frame()
    frame = frame
    if not ret:
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        else:
            continue
    blob = cv2.dnn.blobFromImage(frame,
                                 0.00392, (416, 416), (0, 0, 0),
                                 True,
                                 crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    boxes, confidences, class_ids, indexes = yolov3.detect_objects(
        frame, net, outs, classes)
    yolov3.draw_detections(frame, boxes, class_ids, classes, indexes)

    cv2.imshow('Video Stream', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

rtscap.stop_read()
rtscap.release()
cv2.destroyAllWindows()
