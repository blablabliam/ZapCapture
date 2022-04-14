#Original code developed for Python 2.7 by Saulius Lukse
#Translated to Python 3 by Liam Plybon (2022)
#Anaconda Environment should include OpenCV and Pillow.
#Venv should include OpenCV and Pillow.
#Current venv is LightningVenv on home directory.

#This is still the same as the original lightning analyzer-
#I am using it for reference while crafting the GUI.

import sys
import cv2
import numpy as np
from PIL import Image
import time

SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3

start = time.time()

def count_diff(img1, img2):
    #Finds a difference between a frame and the frame before it.
    small1 = cv2.resize(img1, (0,0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0,0), fx=SCALE, fy=SCALE)
    #cv2.imshow('frame', small2)
    #cv2.waitKey(1)
    diff = cv2.absdiff(small1, small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    frame_delta1_color = cv2.cvtColor(frame_delta1, cv2.COLOR_GRAY2RGB)
    delta_count1 = cv2.countNonZero(frame_delta1)

    return delta_count1

#Use the argv function if running in command line. Otherwise,
#manually enter in a filename.
#filename = sys.argv[1]
filename = '/home/liam/Videos/Camera/lightning.mp4'
video = cv2.VideoCapture(filename)

nframes = (int)(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = (int)(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = (int)(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps= (int)(video.get(cv2.CAP_PROP_FPS))

frame_count = 0

print("[i] Frame size: ", width, height)
print("[i] Total frames:", nframes)
print("[i] Fps:", fps)

fff = open(filename+".csv", 'w')

flag, frame0 = video.read()
#Use the argv when running from the command line. Otherwise, set it
#as an integer. 10,000 is the suggested one in the webpage.
#The threshold controls how many frames you get. A lower threshold
#will give more lightning strikes; a higher threshold will give less.
#For example, a threshold of 100 will yield thousands of frames, while
#a threshold of 100,000 will yield a thousand ana 1000000 will yield zero.
#Likewise, larger thresholds process faster!
#threshold = int(sys.argv[2])
threshold = 500000
strikes = 0

#Loops through the frames, checking for differences exeeding the threshold.
for f in range(nframes-1):
    flag, frame1 = video.read()
    diff1  = count_diff(frame0, frame1)
    name = filename+"_%06d.jpg" % f

    if diff1 > threshold:
        cv2.imwrite(name, frame1)
        strikes = strikes + 1

        #small = cv2.resize(frame1, (0,0), fx=SCALE, fy=SCALE)
        #cv2.imshow('frame', small)
        #cv2.waitKey(1)

    text = str(f)+', '+str(diff1)
    #print text
    fff.write(text  + '\n')
    fff.flush()
    frame0 = frame1

fff.close()
print('[i] Strikes: ', strikes)
print('[i] elapsed time:', time.time() - start)
