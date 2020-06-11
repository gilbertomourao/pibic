#!/usr/bin/env python3

from hough import houghOverlay
import cv2
import numpy as np
import math
import time

# Loading the overlay
hw = houghOverlay('houghlines.bit')
hw.loadParameters(edges_lthr = 20, edges_hthr = 30, lines_thr = 80, gap_size = 5, min_length = 50)

# Extracting lines
img_path = r'/home/xilinx/jupyter_notebooks/temp/data/usar'
canto = img_path + '/canto.jpg'
janela = img_path + '/janela.jpg'
porta = img_path + '/porta.jpg'
tv = img_path + '/tv.jpg'
chao = img_path + '/chao.jpg'

# pre-allocation
edges = np.zeros((480,640,3), np.uint8)
original = np.zeros((480,640,3), np.uint8)
edges2 = np.zeros((480,640,3), np.uint8)
original2 = np.zeros((480,640,3), np.uint8)
edges_temp = np.zeros((480,640,3), np.uint8)

def draw_lines_and_segments(lines, segments):
    
    # Lines

    for [rho, theta] in lines:
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(round(x0 + 1500*(-b) + 320))
        y1 = int(round(y0 + 1500*(a) + 240))
        x2 = int(round(x0 - 1500*(-b) + 320))
        y2 = int(round(y0 - 1500*(a) + 240))
        cv2.line(edges, (x1, y1), (x2, y2), (0,0,255), 2)
        cv2.line(original, (x1, y1), (x2, y2), (0,0,255), 2)

    # Segments

    for [x1,y1,x2,y2] in segments:
        cv2.line(edges2, (x1, y1), (x2, y2), (0,0,255), 2)
        cv2.line(original2, (x1, y1), (x2, y2), (0,0,255), 2)

def hardware_test(image):
    hw.frame[:] = cv2.imread(image)
    original[:] = hw.frame[:]
    start = time.time()
    [lines, segments] = hw.HoughLines(canny = edges)
    end = time.time()

    print('Elapsed time (in ms): ',str((end - start)*1e3))

    edges_temp[:] = edges[:]
    edges2[:] = edges[:]
    original2[:] = original[:]

    draw_lines_and_segments(lines, segments)

def software_test(image):
    sw_frame = cv2.imread(image)

    start = time.time()

    gray = cv2.cvtColor(sw_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 20, 30, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    segments = cv2.HoughLinesP(edges,1,np.pi/180,80,50,5)

    end = time.time()

    print('SW elapsed time (in ms): ', str((end - start)*1e3))



#########################################
############## Canto ####################
#########################################

hardware_test(canto)

cv2.imwrite('resultados/canto/edges_canto.jpg', edges_temp)
cv2.imwrite('resultados/canto/lines_canto.jpg', edges)
cv2.imwrite('resultados/canto/lines_canto_original.jpg', original)
cv2.imwrite('resultados/canto/segments_canto.jpg', edges2)
cv2.imwrite('resultados/canto/segments_canto_original.jpg', original2)


#software time analyzer

software_test(canto)

#########################################
############## Janela ###################
#########################################

hardware_test(janela)

cv2.imwrite('resultados/janela/edges_janela.jpg', edges_temp)
cv2.imwrite('resultados/janela/lines_janela.jpg', edges)
cv2.imwrite('resultados/janela/lines_janela_original.jpg', original)
cv2.imwrite('resultados/janela/segments_janela.jpg', edges2)
cv2.imwrite('resultados/janela/segments_janela_original.jpg', original2)

#software time analyzer

software_test(janela)

#########################################
############## Porta ####################
#########################################

hardware_test(porta)

cv2.imwrite('resultados/porta/edges_porta.jpg', edges_temp)
cv2.imwrite('resultados/porta/lines_porta.jpg', edges)
cv2.imwrite('resultados/porta/lines_porta_original.jpg', original)
cv2.imwrite('resultados/porta/segments_porta.jpg', edges2)
cv2.imwrite('resultados/porta/segments_porta_original.jpg', original2)

#software time analyzer

software_test(porta)

#########################################
################# TV ####################
#########################################

hardware_test(tv)

cv2.imwrite('resultados/tv/edges_tv.jpg', edges_temp)
cv2.imwrite('resultados/tv/lines_tv.jpg', edges)
cv2.imwrite('resultados/tv/lines_tv_original.jpg', original)
cv2.imwrite('resultados/tv/segments_tv.jpg', edges2)
cv2.imwrite('resultados/tv/segments_tv_original.jpg', original2)

#software time analyzer

software_test(tv)

#########################################
################ CHAO ###################
#########################################

hardware_test(chao)

cv2.imwrite('resultados/chao/edges_chao.jpg', edges_temp)
cv2.imwrite('resultados/chao/lines_chao.jpg', edges)
cv2.imwrite('resultados/chao/lines_chao_original.jpg', original)
cv2.imwrite('resultados/chao/segments_chao.jpg', edges2)
cv2.imwrite('resultados/chao/segments_chao_original.jpg', original2)

#software time analyzer

software_test(chao)


