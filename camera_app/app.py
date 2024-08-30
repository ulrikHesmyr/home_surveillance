import src.service.motion_detection as md
import requests

#Change this if you want to use another webcamera than the system default
camera_index = 0


md.start_capture(camera_index)