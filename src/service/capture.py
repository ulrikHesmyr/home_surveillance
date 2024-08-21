import cv2 as cv
import imutils

"""
The background frame used in the motion detection algorithm to 
detect difference in pixel intensity values between the (ideally) static background frame and foreground frame.
The foreground frame (which is the frame that is being currently captured by the camera) 
may have captured movement, and will thus have different pixel intensity values.
"""
first_frame = None

"""
Threshold for changes in pixel intensity values.
The delta value between the background and foreground frame may have certain changes in 
the pixel values even though there are no movement. Therefore we want to declare what a "significant" change is,
which could indicate actual movement.
"""
LOWER_THRESHOLD = 50

"""
Width of the frame that is sent through the motion detection algorithm. 
If the image is very large, there will be a lot of unecessary operations on the frame matrix, because in reality,
you do not need 1920x1080 pixels to see that there is a person walking in the frame, you may only need 889x500 pixels.
"""
FRAME_WIDTH = 500


def capture(camera_index = 0):
    
    video_capture = cv.VideoCapture(camera_index)

    while True:

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

    video_capture.release()
    cv.destroyAllWindows()

def detection(frame, frame_width = FRAME_WIDTH, lower_threshold = LOWER_THRESHOLD):

    #Resizing because it is not necessary to compute on such large raw images/frames
    frame = imutils.resize(frame, width=frame_width)

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
    threshold = cv.threshold(frame_delta, lower_threshold, 255, cv.THRESH_BINARY)[1]

    return threshold