"""
Threshold for changes in pixel intensity values.
The delta value between the background and foreground frame may have certain changes in 
the pixel values even though there are no movement. Therefore we want to declare what a "significant" change is,
which could indicate actual movement.
"""
LOWER_THRESHOLD = 70

"""
Width of the frame that is sent through the motion detection algorithm. 
If the image is very large, there will be a lot of unecessary operations on the frame matrix, because in reality,
you do not need 1920x1080 pixels to see that there is a person walking in the frame, you may only need 889x500 pixels.
"""
FRAME_WIDTH = 500

"""
Minimum area (in pixels) that a contour must have to be considered as a an object for drawing a rectangle around it
"""
MIN_AREA_FOR_CONTOUR = 750


"""
Length of the stream duration in seconds 
"""
NOTIFICATION_DELAY = 60