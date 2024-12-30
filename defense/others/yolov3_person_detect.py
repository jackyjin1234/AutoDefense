import cv2
import numpy as np


def load_yolo_model(weights_path, config_path):
    net = cv2.dnn.readNet(weights_path, config_path)
    return net


def load_classes(class_file_path):
    with open(class_file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def prepare_image(image_path, net, target_size=(416, 416)):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image {image_path} not found.")
    blob = cv2.dnn.blobFromImage(image,
                                 0.00392,
                                 target_size, (0, 0, 0),
                                 True,
                                 crop=False)
    net.setInput(blob)
    return image, blob


def detect_objects(image, net, outs, classes, threshold=0.5):
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold and class_id == 0:  # 类别0是"person"
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    return boxes, confidences, class_ids, indexes


def draw_detections(image,
                    boxes,
                    class_ids,
                    classes,
                    indexes,
                    person_color=(0, 255, 0),
                    centroid_color=(0, 0, 255)):
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(image, (x, y), (x + w, y + h), person_color, 2)
            cv2.putText(image, label, (x, y - 10), font, 1, person_color, 2)

            # Calculate the centroid of the bounding box
            centroid_x = int(x + w / 2)
            centroid_y = int(y + h / 2)

            # Draw the centroid point
            cv2.circle(image, (centroid_x, centroid_y), 10, centroid_color, -1)


def main(weights_path, config_path, class_file_path, image_path):
    net = load_yolo_model(weights_path, config_path)
    classes = load_classes(class_file_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    image, blob = prepare_image(image_path, net)
    outs = net.forward(output_layers)
    boxes, confidences, class_ids, indexes = detect_objects(
        image, net, outs, classes)

    draw_detections(image, boxes, class_ids, classes, indexes)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main("yolov3.weights", "yolov3.cfg", "coco.names", "test_1.jpg")
