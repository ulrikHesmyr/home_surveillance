import src.service.capturer as capturer
import requests

#Change this if you want to use another webcamera than the system default
camera_index = 0


capturer.start_capture(camera_index)