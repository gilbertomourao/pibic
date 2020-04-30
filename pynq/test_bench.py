#!/usr/bin/env python3

from hough import houghOverlay
import cv2
import numpy as np
import math
import time

# Loading the overlay
hw = houghOverlay('xfhough100.bit')
hw.loadParameters(edges_lthr = 20, edges_hthr = 50, lines_thr = 80)

# Extracting lines
img_path = r'/home/xilinx/jupyter_notebooks/temp/data/usar'
canto = img_path + '/canto.jpg'
janela = img_path + '/janela.jpg'
porta = img_path + '/porta.jpg'
tv = img_path + '/tv.jpg'

# pre-allocation
edges = np.zeros((480,640,3), np.uint8)
original = np.zeros((480,640,3), np.uint8)

#########################################
############## Canto ####################
#########################################

hw.frame[:] = cv2.imread(canto)
original[:] = hw.frame[:]
start = time.time()
[rho, theta] = hw.HoughLines(canny = edges)
end = time.time()

print('Elapsed time (in ms): ',str((end - start)*1e3))

start = time.time()
cv2.imwrite('resultados/edges_canto.jpg', edges)
end = time.time()

print('imwrite elapsed time (in ms): ',str((end-start)*1e3))

start = time.time()
# Drawing lines
for i in range(100):
    a = math.cos(theta[i])
    b = math.sin(theta[i])
    x0 = a*rho[i]
    y0 = b*rho[i]
    x1 = int(round(x0 + 1500*(-b) + 320))
    y1 = int(round(y0 + 1500*(a) + 240))
    x2 = int(round(x0 - 1500*(-b) + 320))
    y2 = int(round(y0 - 1500*(a) + 240))
    cv2.line(edges, (x1, y1), (x2, y2), (255,0,0), 1)
    cv2.line(original, (x1, y1), (x2, y2), (255,0,0),1)
end = time.time()

print('line drawing elapsed time (in ms): ',str((end-start)*1e3))

cv2.imwrite('resultados/lines_canto.jpg', edges)
cv2.imwrite('resultados/lines_canto_original.jpg', original)

#software time analyzer

sw_frame = cv2.imread(canto)

def sw_houghlines(sw_frame):
    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 50, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    return lines

start = time.time()
lines = sw_houghlines(sw_frame)
end = time.time()

print('SW elapsed time (in ms): ', str((end - start)*1e3))

#########################################
############## Janela ###################
#########################################

hw.frame[:] = cv2.imread(janela)
original[:] = hw.frame[:]
start = time.time()
[rho, theta] = hw.HoughLines(canny = edges)
end = time.time()

print('Elapsed time (in ms): ',str((end - start)*1e3))

start = time.time()
cv2.imwrite('resultados/edges_janela.jpg', edges)
end = time.time()

print('imwrite elapsed time (in ms): ',str((end-start)*1e3))

start = time.time()
# Drawing lines
for i in range(100):
    a = math.cos(theta[i])
    b = math.sin(theta[i])
    x0 = a*rho[i]
    y0 = b*rho[i]
    x1 = int(round(x0 + 1500*(-b) + 320))
    y1 = int(round(y0 + 1500*(a) + 240))
    x2 = int(round(x0 - 1500*(-b) + 320))
    y2 = int(round(y0 - 1500*(a) + 240))
    cv2.line(edges, (x1, y1), (x2, y2), (255,0,0), 1)
    cv2.line(original, (x1, y1), (x2, y2), (255,0,0), 1)
end = time.time()

print('line drawing elapsed time (in ms): ',str((end-start)*1e3))

cv2.imwrite('resultados/lines_janela.jpg', edges)
cv2.imwrite('resultados/lines_janela_original.jpg', original)

#software time analyzer

sw_frame = cv2.imread(janela)

def sw_houghlines(sw_frame):
    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 50, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    return lines

start = time.time()
lines = sw_houghlines(sw_frame)
end = time.time()

print('SW elapsed time (in ms): ', str((end - start)*1e3))

#########################################
############## Porta ####################
#########################################

hw.frame[:] = cv2.imread(porta)
original[:] = hw.frame[:]
start = time.time()
[rho, theta] = hw.HoughLines(canny = edges)
end = time.time()

print('Elapsed time (in ms): ',str((end - start)*1e3))

start = time.time()
cv2.imwrite('resultados/edges_porta.jpg', edges)
end = time.time()

print('imwrite elapsed time (in ms): ',str((end-start)*1e3))

start = time.time()
# Drawing lines
for i in range(100):
    a = math.cos(theta[i])
    b = math.sin(theta[i])
    x0 = a*rho[i]
    y0 = b*rho[i]
    x1 = int(round(x0 + 1500*(-b) + 320))
    y1 = int(round(y0 + 1500*(a) + 240))
    x2 = int(round(x0 - 1500*(-b) + 320))
    y2 = int(round(y0 - 1500*(a) + 240))
    cv2.line(edges, (x1, y1), (x2, y2), (255,0,0), 1)
    cv2.line(original, (x1, y1), (x2, y2), (255,0,0), 1)
end = time.time()

print('line drawing elapsed time (in ms): ',str((end-start)*1e3))

cv2.imwrite('resultados/lines_porta.jpg', edges)
cv2.imwrite('resultados/lines_porta_original.jpg', original)

#software time analyzer

sw_frame = cv2.imread(porta)

def sw_houghlines(sw_frame):
    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 50, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    return lines

start = time.time()
lines = sw_houghlines(sw_frame)
end = time.time()

print('SW elapsed time (in ms): ', str((end - start)*1e3))

#########################################
################# TV ####################
#########################################

hw.frame[:] = cv2.imread(tv)
original[:] = hw.frame[:]
start = time.time()
[rho, theta] = hw.HoughLines(canny = edges)
end = time.time()

print('Elapsed time (in ms): ',str((end - start)*1e3))

start = time.time()
cv2.imwrite('resultados/edges_tv.jpg', edges)
end = time.time()

print('imwrite elapsed time (in ms): ',str((end-start)*1e3))

start = time.time()
# Drawing lines
for i in range(100):
    a = math.cos(theta[i])
    b = math.sin(theta[i])
    x0 = a*rho[i]
    y0 = b*rho[i]
    x1 = int(round(x0 + 1500*(-b) + 320))
    y1 = int(round(y0 + 1500*(a) + 240))
    x2 = int(round(x0 - 1500*(-b) + 320))
    y2 = int(round(y0 - 1500*(a) + 240))
    cv2.line(edges, (x1, y1), (x2, y2), (255,0,0), 1)
    cv2.line(original, (x1, y1), (x2, y2), (255,0,0), 1)
end = time.time()

print('line drawing elapsed time (in ms): ',str((end-start)*1e3))

cv2.imwrite('resultados/lines_tv.jpg', edges)
cv2.imwrite('resultados/lines_tv_original.jpg', original)

#software time analyzer

sw_frame = cv2.imread(tv)

def sw_houghlines(sw_frame):
    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 50, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    return lines

start = time.time()
lines = sw_houghlines(sw_frame)
end = time.time()

print('SW elapsed time (in ms): ', str((end - start)*1e3))


