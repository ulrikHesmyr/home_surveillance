import cv2 as cv
import imutils
import time
import numpy as np
import threading
from src.utils.notifications import send_notification
from src.utils.motion_detection import motion_detected, motion_frame_add_text, draw_rectangles, find_contours
from src.utils.const import NOTIFICATION_DELAY, FRAME_WIDTH, LOWER_THRESHOLD


"""
The background frame used in the motion detection algorithm to 
detect difference in pixel intensity values between the (ideally) static background frame and foreground frame.
The foreground frame (which is the frame that is being currently captured by the camera) 
may have captured movement, and will thus have different pixel intensity values.
"""
first_frame = None

#Move this to a separate file, working as a local database
authenticated_users = ["ulrik123"]

#True if a notification has been sent recently (within the NOTIFICATION_DELAY previous seconds), false if not
sent_notification = False

#true if there is a current livestream, false if not
stream_online = False

#True if the capturer is active, false if is deactivated
capture = False

def start_capture(camera_index = 0):
    
    video_capture = cv.VideoCapture(camera_index)

    global capture
    capture = True

    while capture:

        #Trying to read a frame from the video capture device, exiting loop if it failed to read
        ret, frame = video_capture.read()

        if not ret:
            break

        frame = detection(frame)
        if frame is None:
            continue
        
        #Displaying the frame
        cv.imshow('frame', frame)

        #Quit if key 'q' s pressed
        key = cv.waitKey(1)
        if key == ord('q'):
            break

    #Cancel timer somehow? Not critical, but may take some time to get CLI back from the timer thread
    video_capture.release()
    cv.destroyAllWindows()



#Returns a binary image where the pixel values are either 0 or 255, 0 if no motion detected, 255 if motion detected
def detection(frame):

    #Resizing because it is not necessary to compute on such large raw images/frames
    frame = imutils.resize(frame, width=FRAME_WIDTH)

    #Applying grayscale and blur because no subsequent images are 100% equal due to the camera sensors
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (21,21), 0)

    #Initializing the background image of our foreground and background segmentation
    global first_frame

    if first_frame is None:
        first_frame = blurred
        return None

    #Simple subtraction between background and foreground frames to see if there are any differences
    frame_delta = cv.absdiff(first_frame, blurred)

    #Applying a threshold in how much a pixel must be different to determine if there is actual movement
    threshold = cv.threshold(frame_delta, LOWER_THRESHOLD, 255, cv.THRESH_BINARY)[1]

    contours = find_contours(threshold)

    draw_rectangles(contours, frame)

    motion = motion_detected(threshold)

    if(motion):
        global sent_notification

        if not sent_notification and not stream_online:
            sent_notification = True
            send_notification()
            threading.Timer(NOTIFICATION_DELAY, reactivate_notification).start()
    
    motion_frame_add_text(motion, frame)
        
    
    cv.imshow('threshold', threshold)

    return frame



def reactivate_notification():
    global sent_notification

    sent_notification = False