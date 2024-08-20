import cv2 as cv

def capture(camera_index = 0):
    
    video_capture = cv.VideoCapture(camera_index)

    while True:

        #Trying to read a frame from the video capture device, exiting loop if it failed to read
        ret, frame = video_capture.read()

        if not ret:
            break

        #Displaying the frame
        cv.imshow('frame', frame)

        #Quit if key 'q' s pressed
        key = cv.waitKey(1)
        if key == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()