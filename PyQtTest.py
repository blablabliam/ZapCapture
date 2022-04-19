__author__ = "Liam Plybon"
__copyright__ = "Copyright 2022, Liam Plybon"
__credits__ = ["Saulius Lukse", "Drake Anthony (Styropyro)"]
__license__ = "MIT"
__version__ = "2"
__maintainer__ = "Liam Plybon"
__email__ = "lplybon1@gmail.com"
__status__ = "Prototype"
__date__ = "4-17-2022"

import sys
import time
import os
from PIL import Image, ImageTk

# imports for gui interface
from PySide2.QtCore import Qt, QObject, QThread, Signal, Slot
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QProgressBar
)
# imports for Dark Mode theme
from PySide2.QtGui import (
    QPalette,
    QColor,
    QIntValidator
)

import cv2

#global variable
SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3
# input, output, and threshold are manipulated by the directory select buttons
# this allows them to pass into the worker thread without slots and signals.
# as such they are used as global variables
# for clarity, all globals are redefined as global wherever used.
global input_folder
input_folder = 'No Folder Chosen'
global output_folder
output_folder = 'No Folder Chosen'
global threshold
threshold = '5000000'


def count_diff(img1, img2):
    # Finds a difference between a frame and the frame before it.
    small1 = cv2.resize(img1, (0, 0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0, 0), fx=SCALE, fy=SCALE)
    diff = cv2.absdiff(small1, small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    frame_delta1_color = cv2.cvtColor(frame_delta1, cv2.COLOR_GRAY2RGB)
    delta_count1 = cv2.countNonZero(frame_delta1)

    return delta_count1


class Worker(QObject):
    # worker thread for the analysis.
    finished = Signal()
    #progress = Signal(int)
    #input = Signal()
    threadProgress = Signal(int)

    def run(self):
        """Long-running task."""
        print('worker.run')
        # Launches analysis of the videos in the in directory.
        # In future, this needs to have error handling.
        # For now, it is fine without it.
        global input_folder
        global output_folder
        global threshold
        in_folder = input_folder
        out_folder = output_folder
        threshold_integer = int(threshold)
        start = time.time()
        # set framecount, strike counter to zero before looping all frames
        frame_count = 0
        strikes = 0
        self.threadProgress.emit(10)
        #counts number of files in folder for progress bar
        path, dirs, files = next(os.walk(in_folder))
        filecount = len(files)
        for index, filename in enumerate(os.listdir(in_folder)):
            # itterates over files in directory
            # f_in and f_out control input and destination targets
            completion = 10+(90*((index+1)/filecount))
            self.threadProgress.emit(completion)
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

                if diff1 > threshold_integer:
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
        # statistics
        print('[i] Strikes: ', strikes)
        print('[i] elapsed time:', time.time() - start)
        print('analyzed! ')
        #sends finished signal. Essentially terminates the thread.
        self.threadProgress.emit(100)
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        # sets up the gui layout itself
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.inputFileDirectoryButton = QPushButton("Select Input Directory", self)
        self.inputFileDirectoryButton.clicked.connect(self.pick_new_input)
        self.inputFileDirectoryLabel = QLabel(input_folder)
        self.inputFileDirectoryLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.outputFileDirectoryButton = QPushButton("Select Output Directory", self)
        self.outputFileDirectoryButton.clicked.connect(self.pick_new_output)
        self.outputFileDirectoryLabel = QLabel(output_folder)
        self.outputFileDirectoryLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.thresholdLabel = QLabel("Threshold: ", self)
        self.thresholdLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.thresholdEntry = QLineEdit(threshold)
        # restricts the threshold to be numbers only
        self.onlyInt = QIntValidator()
        self.thresholdEntry.setValidator(self.onlyInt)
        self.analysisButton = QPushButton('Perform Analysis', self)
        # self.analysisButton.clicked.connect(self.analysis)
        self.analysisButton.clicked.connect(self.runLongTask)
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #self.progressBar.setGeometry(200, 80, 250, 20)
        self.progressBar.setValue(0)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.inputFileDirectoryButton)
        layout.addWidget(self.inputFileDirectoryLabel)
        layout.addWidget(self.outputFileDirectoryButton)
        layout.addWidget(self.outputFileDirectoryLabel)
        layout.addWidget(self.thresholdLabel)
        layout.addWidget(self.thresholdEntry)
        layout.addWidget(self.analysisButton)
        layout.addWidget(self.progressBar)
        self.centralWidget.setLayout(layout)

    def pick_new_input(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Input Folder")
        global input_folder
        input_folder = str(folder_path)
        self.inputFileDirectoryLabel.setText(str(folder_path))

    def pick_new_output(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Output Folder")
        global output_folder
        output_folder = str(folder_path)
        self.outputFileDirectoryLabel.setText(str(folder_path))

    def runLongTask(self):
        # set the threshold
        global threshold
        threshold = self.thresholdEntry.text()
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # setup progress bar signal
        self.worker.threadProgress.connect(self.onCountChanged)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        print('asdf')

        # Final resets
        self.analysisButton.setEnabled(False)
        print('asdf')
        self.thread.finished.connect(
            lambda: self.analysisButton.setEnabled(True)
        )
        print('asdf')

    def onCountChanged(self, value):
        self.progressBar.setValue(value)

def app_close():
    # function describing app close condition
    return True


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

# finish building window
win = Window()
win.show()
sys.exit(app.exec_())
