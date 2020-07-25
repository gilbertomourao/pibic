#!/usr/bin/env python3

from hough import houghOverlay
import cv2
import numpy as np
import math
import time

# Loading the overlay
hw = houghOverlay('hwvhough.bit')

# Extracting lines
img_path = r'/home/xilinx/jupyter_notebooks/temp/data/usar'
canto = img_path + '/canto.png'
janela = img_path + '/janela.png'
porta = img_path + '/porta.png'
tv = img_path + '/tv.png'
chao = img_path + '/chao.png'
quarto = img_path + '/quarto.png'

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
    [lines, segments] = hw.HoughLines(20, 30, 80, 5, 50, canny = edges)
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


if __name__ == "__main__":

    #########################################
    ############## Janela ###################
    #########################################

    hardware_test(janela)

    cv2.imwrite('resultados/janela/edges_janela.png', edges_temp)
    cv2.imwrite('resultados/janela/lines_janela.png', edges)
    cv2.imwrite('resultados/janela/lines_janela_original.png', original)
    cv2.imwrite('resultados/janela/segments_janela.png', edges2)
    cv2.imwrite('resultados/janela/segments_janela_original.png', original2)

    #software time analyzer

    software_test(janela)

    #########################################
    ############## Canto ####################
    #########################################

    hardware_test(canto)

    cv2.imwrite('resultados/canto/edges_canto.png', edges_temp)
    cv2.imwrite('resultados/canto/lines_canto.png', edges)
    cv2.imwrite('resultados/canto/lines_canto_original.png', original)
    cv2.imwrite('resultados/canto/segments_canto.png', edges2)
    cv2.imwrite('resultados/canto/segments_canto_original.png', original2)

    #software time analyzer

    software_test(canto)

    #########################################
    ############## Porta ####################
    #########################################

    hardware_test(porta)

    cv2.imwrite('resultados/porta/edges_porta.png', edges_temp)
    cv2.imwrite('resultados/porta/lines_porta.png', edges)
    cv2.imwrite('resultados/porta/lines_porta_original.png', original)
    cv2.imwrite('resultados/porta/segments_porta.png', edges2)
    cv2.imwrite('resultados/porta/segments_porta_original.png', original2)

    #software time analyzer

    software_test(porta)

    #########################################
    ################# TV ####################
    #########################################

    hardware_test(tv)

    cv2.imwrite('resultados/tv/edges_tv.png', edges_temp)
    cv2.imwrite('resultados/tv/lines_tv.png', edges)
    cv2.imwrite('resultados/tv/lines_tv_original.png', original)
    cv2.imwrite('resultados/tv/segments_tv.png', edges2)
    cv2.imwrite('resultados/tv/segments_tv_original.png', original2)

    #software time analyzer

    software_test(tv)

    #########################################
    ################ Chao ###################
    #########################################

    hardware_test(chao)

    cv2.imwrite('resultados/chao/edges_chao.png', edges_temp)
    cv2.imwrite('resultados/chao/lines_chao.png', edges)
    cv2.imwrite('resultados/chao/lines_chao_original.png', original)
    cv2.imwrite('resultados/chao/segments_chao.png', edges2)
    cv2.imwrite('resultados/chao/segments_chao_original.png', original2)

    #software time analyzer

    software_test(chao)

    #########################################
    ############## Quarto ###################
    #########################################

    hardware_test(quarto)

    cv2.imwrite('resultados/quarto/edges_quarto.png', edges_temp)
    cv2.imwrite('resultados/quarto/lines_quarto.png', edges)
    cv2.imwrite('resultados/quarto/lines_quarto_original.png', original)
    cv2.imwrite('resultados/quarto/segments_quarto.png', edges2)
    cv2.imwrite('resultados/quarto/segments_quarto_original.png', original2)


    #software time analyzer

    software_test(quarto)


