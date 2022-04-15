# Original code developed for Python 2.7 by Saulius Lukse
# Translated to Python 3 by Liam Plybon (2022)
# Venv should include OpenCV, Pyinstaller, and Pillow.
# Current venv is LightningVenv on home directory.
__author__ = "Liam Plybon"
__copyright__ = "Copyright 2022, Liam Plybon"
__credits__ = ["Saulius Lukse", "Drake Anthony (Styropyro)"]
__license__ = "MIT"
__version__ = "1"
__maintainer__ = "Liam Plybon"
__email__ = "lplybon1@gmail.com"
__status__ = "Production"
__date__ = "4-14-2022"

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import sys
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

# hardcoded values for  computer vision
SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3


def browse_button_in():
    # Allow user to select a directory and store it in global var
    # called folder_path_in
    # This function is called by the input directory button.
    global folder_path_in
    filename = filedialog.askdirectory()
    folder_path_in.set(filename)
    print(filename)


def browse_button_out():
    # Allow user to select a directory and store it in global var
    # called folder_path_out
    # This function is called by the output directory button.
    global folder_path_out
    filename = filedialog.askdirectory()
    folder_path_out.set(filename)
    print(filename)


def count_diff(img1, img2):
    # Finds a difference between a frame and the frame before it.
    small1 = cv2.resize(img1, (0, 0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0, 0), fx=SCALE, fy=SCALE)
    #cv2.imshow('frame', small2)
    # cv2.waitKey(1)
    diff = cv2.absdiff(small1, small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    frame_delta1_color = cv2.cvtColor(frame_delta1, cv2.COLOR_GRAY2RGB)
    delta_count1 = cv2.countNonZero(frame_delta1)

    return delta_count1


def execute_analysis():
    # Launches analysis of the videos in the in directory.
    # In future, this needs to have error handling.
    # For now, it is fine without it.
    start = time.time()
    in_folder = folder_path_in.get()
    out_folder = folder_path_out.get()
    threshold = int(thresholdsetpoint.get())
    print(threshold)
    # print(in_folder, out_folder)
    # set framecount, strike counter to zero before looping all frames
    frame_count = 0
    strikes = 0
    for filename in os.listdir(in_folder):
        # itterates over files in directory
        # f_in and f_out control input and destination targets
        f_in = os.path.join(in_folder, filename)
        f_out = os.path.join(out_folder, filename)
        video = cv2.VideoCapture(f_in)
        # gets statistics on current video
        nframes = (int)(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = (int)(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = (int)(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = (int)(video.get(cv2.CAP_PROP_FPS))
        # video diagnostics printout for user ease.
        # Might incorporate into visible log at later date
        print(str(f_in))
        print("[i] Frame size: ", width, height)
        print("[i] Total frames:", nframes)
        print("[i] Fps:", fps)
        # opens csv for statistics- might want to disable for production.
        fff = open(f_out+".csv", 'w')
        # reads the video out to give a frame and flag
        flag, frame0 = video.read()
        for i in range(nframes-1):
            # loops through all of the frames, looking for strikes.
            flag, frame1 = video.read()
            diff1 = count_diff(frame0, frame1)
            name = f_out+"_%06d.jpg" % i

            if diff1 > threshold:
                # pass condition
                cv2.imwrite(name, frame1)
                strikes = strikes + 1

            text = str(f_out)+', '+str(diff1)
            # print text to csv
            fff.write(text + '\n')
            fff.flush()
            # pass frame forward
            frame0 = frame1
    fff.close()
    #statistics
    print('[i] Strikes: ', strikes)
    print('[i] elapsed time:', time.time() - start)
    print('analyzed! ')


# Build window root frame
root = Tk()

# beautify tkinter a bit
root.title("Lightning Bolt Analyzer")
root.geometry('700x300+1000+300')
root.resizable(width=False, height=False)

# add background lightning - kinda ugly but works for now
bg = PhotoImage(file="assets/background.gif")
background_image = bg
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# establish grid in root called mainframe
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Get the input folder directory.
# This directory will hold all of the video files to be analyzed.
folder_path_in = StringVar()
inputlabel = Label(master=mainframe, textvariable=folder_path_in, font=('Open Sans', 12))
inputlabel.grid(row=0, column=1)
inputbuttonimg = PhotoImage(file="assets/button_input-folder.png")
inputbutton = Button(master=mainframe, text="Input Folder", command=browse_button_in)
inputbutton.config(image=inputbuttonimg)
inputbutton.grid(row=0, column=0)

# Get the output folder directory.
# This directory will hold all of the image frames after analysis.
folder_path_out = StringVar()
outputlabel = Label(master=mainframe, textvariable=folder_path_out, font=('Open Sans', 12))
outputlabel.grid(row=1, column=1)
outputbuttonimg = PhotoImage(file="assets/button_output-folder.png")
outputbutton = Button(master=mainframe, text="Output Folder", command=browse_button_out)
outputbutton.config(image=outputbuttonimg)
outputbutton.grid(row=1, column=0)

# input for the Threshold.
# Input can range from 10,000 all the way to 500,000 while giving good results.
# default threshold will give sparse values, and should be lowered during use.
thresholdsetpoint = StringVar()
thresholdsetpoint.set(500000)
thresholdlabel = Label(master=mainframe, text="Threshold Select", font=('Open Sans', 12))
thresholdlabel.grid(row=2, column=0)
threshold = Entry(master=mainframe, textvariable=thresholdsetpoint, font=('Open Sans', 12))
threshold.grid(row=2, column=1)

# Analyze button
# This should start the analysis, and give some kind of feedback.
analysislabel = Label(master=mainframe, text='Perform Analysis?', font=('Open Sans', 12))
analysislabel.grid(row=3, column=0)
analysisbuttonimg = PhotoImage(file="assets/button_analyze.png")
analysisbutton = Button(master=mainframe,
                        text='Analyze!',
                        command=execute_analysis)
analysisbutton.config(image=analysisbuttonimg)
analysisbutton.grid(row=3, column=1)

# Progress Bar
# A progress bar can be installed here, although since that requires multithreading
# I am not super exited to get into it until the whole system is working.
# For now, a placeholder bar gets to occupy the slot.
analysisprogress = ttk.Progressbar(master=root,
                                   orient=HORIZONTAL,
                                   length=600,
                                   mode='determinate')
analysisprogress.grid(row=1, column=0)

# Instructions Text Box
# This sits below the mainframe, and gives instructions on running the software.
instructions = '''Select an input folder with lightning videos, then select a
folder to output the image results. The default threshold of 500,000 is
agressive; if you don't get many images after processing, reduce the threshold
by factors of 10 until you do. Clicking 'Analyze!' will start the process. You
can watch the files in real time in your output folder to verify that the
script is running.
https://blablabliam.github.io'''
instructionbox = Label(master=root, text=instructions, font=('Open Sans', 10))
instructionbox.grid(row=2, column=0)

# establish mainframe padding between children
# for child in mainframe.winfo_children():
#     child.grid_configure(padx=5, pady=5)

inputlabel.focus()

# executes the main window.
root.mainloop()
