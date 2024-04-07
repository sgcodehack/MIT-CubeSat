import cv2
from matplotlib import pyplot as plt

def object_detection(image_file = 'test.jpg'):
    img = cv2.imread(image_file)
    