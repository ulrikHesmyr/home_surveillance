import numpy as np
import cv2 as cv
import imutils
from src.utils.const import MIN_AREA_FOR_CONTOUR

def motion_detected(threshold):
    return np.sum(threshold) > 0

#Applies text to the frame whether motion is detected or not
def motion_frame_add_text(motion, frame):
    if not motion:
        cv.putText(frame, "No motion detected", (10,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    else:
        cv.putText(frame, "Motion detected", (10,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)


#Finds contours in a binary image
def find_contours(binary_frame):
    thresh = cv.dilate(binary_frame, None, iterations=2)
    
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts

#Draws rectangles
def draw_rectangles(cnts, frame):

    for c in cnts:
        if cv.contourArea(c) < MIN_AREA_FOR_CONTOUR:
            continue

        (x,y,w,h) = cv.boundingRect(c)
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)