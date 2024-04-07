import cv2
from matplotlib import pyplot as plt
from ultralytics import YOLO

def object_detection():
    model = YOLO("yolov8n.yaml")
    results = model.train(data = "Software/config.yaml", epochs = 3)
    result = model("/home/pi/MIT-CubeSat/Software/basketballs/images/test/basketball_8.jpg")
    print(result)
    
if __name__ == '__main__':
    object_detection()