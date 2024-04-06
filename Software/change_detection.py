import cv2
import numpy as np

THRESH = 60 #toggles amount of change
ASSIGN_VALUE = 255

def identify_change(orig_file, final_file):
    #get images
    orig = cv2.imread(orig_file)
    final = cv2.imread(final_file)
    #convert to grayscale to disregard small changes
    orig_gray = cv2.cvtColor(orig, cv2.COLOR_RGB2GRAY)
    final_gray = cv2.cvtColor(final, cv2.COLOR_RGB2GRAY)
    #subtract the two images
    diff = cv2.absdiff(orig_gray, final_gray)
    #creates the mask
    threshold_method = cv2.THRESH_BINARY
    ret, motion_mask = cv2.threshold(diff, THRESH, ASSIGN_VALUE, threshold_method)
    cv2.imshow('Motion Mask', motion_mask)
    cv2.imshow()

if __name__ == '__main__':
    import sys
    
    identify_change(*sys.argv[1:])