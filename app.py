import src.service.capture as video_capture

#Change this if you want to use another webcamera than the system default
camera_index = 0


video_capture.capture(camera_index)