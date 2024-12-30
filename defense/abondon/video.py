import cv2
from yolov3 import detect
import time

# ip摄像机地址url
# url = r"rtsp://admin:xxxxxx@192.168.1.75:554/11"
# cap = cv2.VideoCapture(url)

# 访问摄像机需要的信息
# ip = '192.168.1.75'
# user = 'admin'
# password = 'xxxxxx' # 访问摄像机需要密码
# 抓取视频流
i = [26,34,175,170,151,52,44,41]
for i in range(10):
    try:
        cap = cv2.VideoCapture("rtsp://admin:xckj2024@192.168.1.178:554/h264/ch1/sub/av_stream")  # 端口port通常是固定的554
    except:
        print('1')
ret, frame = cap.read()
cv2.namedWindow('192.168.1.178', 0)
# cv2.resizeWindow('192.168.1.178', 500, 300)

# 加载 YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

prev = 0

# 使用，展示
while ret:
    ret, frame = cap.read()
    time_elapsed = time.time() - prev

    if time_elapsed > 1./10:
        prev = time.time()
        frame = detect(frame, net, output_layers, classes)
    cv2.imshow('192.168.1.178', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 退出时释放窗口和内存
cv2.destroyAllWindows()
cap.release()