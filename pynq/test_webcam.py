#!/usr/bin/env python3

from __future__ import print_function
from webcam import WebcamVideoStream, FPS
import argparse
import cv2
import numpy as np
from hough import houghOverlay

# loading the overlay
hw = houghOverlay('houghlines.bit')
hw.loadParameters(edges_lthr = 20, edges_hthr = 30, lines_thr = 80, gap_size = 5, min_length = 50)

camera = 0
iterations = 10

print("[INFO] sampling THREADED frames from webcam")
vs = WebcamVideoStream(src=camera).start()

# Hardware
print('Hardware execution...')
fps = FPS().start()

while fps._numFrames < iterations:
    hw.frame[:] = vs.read()
    [lines, segments] = hw.HoughLines()
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Software
print('Software execution...')
# cv function
def sw_houghlines(sw_frame):
    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 30, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    segments = cv2.HoughLinesP(edges,1,np.pi/180,80,50,5)
    return lines

fps = FPS().start()
sw_frame = np.zeros((480,640,3), np.uint8)

while fps._numFrames < iterations:
    sw_frame = vs.read()
    lines = sw_houghlines(sw_frame)
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

#cv2.destroyAllWindows()
vs.stop()
