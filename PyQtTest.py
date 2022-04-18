import sys
import time
import os
from PIL import Image, ImageTk

#imports for gui interface
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit
    )
#imports for Dark Mode theme
from PySide2.QtGui import (
    QPalette,
    QColor,
    QIntValidator
    )

import cv2

SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3

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


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        #sets up the gui layout itself
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.inputFileDirectoryButton = QPushButton("Select Input Directory", self)
        self.inputFileDirectoryButton.clicked.connect(self.pick_new_input)
        self.inputFileDirectoryLabel = QLabel('No Input Directory Selected!')
        self.inputFileDirectoryLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.outputFileDirectoryButton = QPushButton("Select Output Directory", self)
        self.outputFileDirectoryButton.clicked.connect(self.pick_new_output)
        self.outputFileDirectoryLabel = QLabel('No Output Directory Selected!')
        self.outputFileDirectoryLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.thresholdLabel = QLabel("Threshold: ", self)
        self.thresholdLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.thresholdEntry = QLineEdit('5000000')
        # restricts the threshold to be numbers only
        self.onlyInt = QIntValidator()
        self.thresholdEntry.setValidator(self.onlyInt)
        self.analysisButton = QPushButton('Perform Analysis', self)
        self.analysisButton.clicked.connect(self.analysis)



        #self.folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.inputFileDirectoryButton)
        layout.addWidget(self.inputFileDirectoryLabel)
        layout.addWidget(self.outputFileDirectoryButton)
        layout.addWidget(self.outputFileDirectoryLabel)
        layout.addWidget(self.thresholdLabel)
        layout.addWidget(self.thresholdEntry)
        layout.addWidget(self.analysisButton)
        self.centralWidget.setLayout(layout)

    # def countClicks(self):
    #     self.clicksCount += 1
    #     self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")
    #
    # def reportProgress(self, n):
    #     self.stepLabel.setText(f"Long-Running Step: {n}")
    #
    # def runLongTask(self):
    #     """Long-running task in 5 steps."""
    #     for i in range(5):
    #         sleep(1)
    #         self.reportProgress(i + 1)

    def pick_new_input(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.inputFileDirectoryLabel.setText(str(folder_path))

    def pick_new_output(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.outputFileDirectoryLabel.setText(str(folder_path))

    def analysis(self):
        # Launches analysis of the videos in the in directory.
        # In future, this needs to have error handling.
        # For now, it is fine without it.
        start = time.time()
        in_folder = self.inputFileDirectoryLabel.text()
        out_folder = self.outputFileDirectoryLabel.text()
        threshold = int(self.thresholdEntry.text())
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

app = QApplication(sys.argv)

# Dark Mode code
# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

#finish building window
win = Window()
win.show()
sys.exit(app.exec_())
