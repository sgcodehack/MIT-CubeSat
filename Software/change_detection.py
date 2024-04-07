import cv2
import numpy as np
import sys
sys.path.append('/usr/lib/aarch64-linux-gnu/')

THRESH = 60 #toggles amount of change
ASSIGN_VALUE = 255
background = None

def identify_change(orig_file = 'car1.jpg', final_file = 'car2.jpg'):
    #get images
    orig = cv2.imread(orig_file)
    final = cv2.imread(final_file)
    orig = cv2.resize(orig, (2206, 1150))
    final = cv2.resize(final, (2206, 1150))
    #convert to grayscale to disregard small changes
    orig_gray = cv2.cvtColor(orig, cv2.COLOR_RGB2GRAY)
    final_gray = cv2.cvtColor(final, cv2.COLOR_RGB2GRAY)
    #subtract the two images
    diff = cv2.absdiff(orig_gray, final_gray)\
    #creates the mask
    threshold_method = cv2.THRESH_BINARY
    _, motion_mask = cv2.threshold(diff, THRESH, ASSIGN_VALUE, threshold_method)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        x, y, w, h, = cv2.boundingRect(contour)
        cv2.rectangle(final, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('result', final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys

    identify_change(*sys.argv[1:])