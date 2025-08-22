__author__ = "Liam Plybon (blablabliam.github.io)"
__copyright__ = "Copyright 2022, Liam Plybon"
__credits__ = ["Saulius Lukse", "Drake Anthony (Styropyro)", "Stephen C Hummel"]
__license__ = "MIT"
__version__ = "2"
__maintainer__ = "Liam Plybon"
__email__ = "lplybon1@gmail.com"
__status__ = "Prototype"
__date__ = "6-16-2022"

import os
import sys
import cv2
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import (
    QPalette,
    QColor,
    QIntValidator
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QProgressBar,
    QMessageBox
)

# global constantssfs
SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3
END_STRIKE_PERCENTAGE = .9
GIF_FRAMES_LIMIT = 100
# input, output, and threshold are manipulated by the directory select buttons
# this allows them to pass into the worker thread without slots and signals.
# as such they are used as global variables
# for clarity, all globals are redefined as global wherever used.
input_folder = 'No Folder Chosen'
output_folder = 'No Folder Chosen'
threshold = '5000000'
buttonState = True


def count_diff(img1, img2):
    # Finds a difference between a frame and the frame before it.
    small1 = cv2.resize(img1, (0, 0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0, 0), fx=SCALE, fy=SCALE)
    diff = cv2.absdiff(small1, small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    delta_count1 = cv2.countNonZero(frame_delta1)

    return delta_count1


def error_popup(message):
    """Might cause a crash, but since it is for errors I am less inclined to worry."""
    print(message)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText("Error")
    msg.setInformativeText(str(message))
    msg.setWindowTitle("Lightning Analysis Error")
    # prevents crash after closing message box
    msg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    msg.exec()


# Popup for info after analysis. Caused crashes when started from
# the analysis thread rather than the main thread.
# Might reintroduce one day, since it provides nice information.

# def info_popup(message):
#     msg = QMessageBox()
#     msg.setIcon(QMessageBox.Information)
#     msg.setText("Analysis Complete!")
#     msg.setInformativeText(str(message))
#     msg.setWindowTitle("Lightning Analysis Complete")
#     # prevents crash after closing message box
#     msg.setAttribute(Qt.WA_DeleteOnClose)
#     msg.exec_()

class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class Worker(QObject):
    # worker thread for the analysis.
    finished = Signal()
    threadProgress = Signal(int)

    def run(self):
        """Analyzes lightning. """
        # Launches analysis of the videos in the in directory.
        print('Started Analysis!')
        global input_folder
        global output_folder
        global threshold
        global buttonState
        in_folder = input_folder
        out_folder = output_folder
        threshold_integer = int(threshold)
        strikes = 0
        # set progress bar to 10 so people know it is working
        self.threadProgress.emit(10)
        try:
            # error if the folder is invalid. Check folder for verification.
            _, dirs, files = next(os.walk(in_folder))
        except (OSError, StopIteration):
            error_popup('Input folder not valid. Select a valid folder.')
            self.threadProgress.emit(0)
            self.finished.emit()
            return
        try:
            # determine if the output folder is valid
            _, dirs, files = next(os.walk(out_folder))
        except (OSError, StopIteration):
            error_popup('Output folder not valid. Select a valid folder.')
            self.threadProgress.emit(0)
            self.finished.emit()
            return
        # create frame and gif directories after checking for existence
        impath = os.path.join(out_folder, 'frames/')
        gif_path = os.path.join(out_folder, 'gifs/')
        if not os.path.isdir(impath):
            os.mkdir(impath)
        if not os.path.isdir(gif_path):
            os.mkdir(gif_path)
        # get the current directory files count. If the out folder is the same
        # as the in folder, this might have changed after creating the output
        # folders above.
        path, dirs, files = next(os.walk(in_folder))
        filecount = len(files) + len(dirs)
        # set per file progress bar quantity
        per_file = 90 / filecount
        for index, filename in enumerate(os.listdir(in_folder)):
            # iterates over files in directory
            # f_in and f_out control input and destination targets
            print('Processing ' + filename)
            try:
                file_base = 10 + index * per_file
                completion = file_base
            except (ZeroDivisionError, TypeError, ValueError):
                self.threadProgress.emit(0)
                self.finished.emit()
                return
            self.threadProgress.emit(completion)
            f_in = os.path.join(in_folder, filename)
            f_out = os.path.join(out_folder, filename)
            try:
                video = cv2.VideoCapture(f_in)
            except Exception as e:
                print(f'video lib error: {e}')
                return
            # gets statistics on current video
            n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            if fps == 0 or n_frames == 1:
                print('zero fps or image!')
                video.release()  # Clean up video capture
                continue

            fff = open(f_out + ".csv", 'w')
            try:
                # reads the video out to give a frame and flag
                flag, frame0 = video.read()
                # Set video codec.
                print("setting codec mp4v")
                fourcc = cv2.VideoWriter.fourcc(*'mp4v')
                print("codec successful!")
                # savestate for using the dead_zone.
                dead_zone = 0
                # creates list for gif frames
                gif_frames = []
                # strike counter independent for file. Helps with writing gifs.
                file_strikes = 0
                # remove filename period, so that the output files don't confuse anything.
                filename = filename.replace('.', '_')
                for i in range(n_frames - 1):
                    # loops through all the frames, looking for strikes.
                    # iterate progress bar
                    file_cap = (i / (n_frames + 1)) * per_file
                    file_completion = file_base + file_cap
                    self.threadProgress.emit(file_completion)
                    # process the video
                    flag, frame1 = video.read()
                    diff1 = count_diff(frame0, frame1)
                    # checks for file output name system
                    # names files and gifs respectively.
                    if not buttonState and isinstance(fps, int):
                        timestamp = str(round(int(i) / int(fps), 2)).replace('.', '-')
                        im_name = impath + '/' + str(filename) + str(timestamp) + '.png'
                        gif_name = gif_path + '/' + str(filename) + str(timestamp) + '.mp4'
                    else:
                        im_name = impath + str(filename) + "_%06d.png" % i
                        gif_name = gif_path + str(filename) + "_%06d.mp4" % i
                    if len(gif_frames) == GIF_FRAMES_LIMIT:
                        # end a gif if the clip gets large to prevent computer issues.
                        # massive gifs can cause lag and other problems.
                        dead_zone = 0
                    if diff1 > threshold_integer:
                        # pass condition to save a frame and start a save state
                        strikes = strikes + 1
                        file_strikes = file_strikes + 1
                        gif_name = gif_name
                        # write previous gif list to a gif if not the second frame
                        # and the dead zone is already zero (ie lightning has already
                        # struck and the gif buffer contains frames).
                        if dead_zone == 0 and file_strikes > 1:
                            gif_frames.pop(0)
                            print('setting writer')
                            out = cv2.VideoWriter(gif_name, fourcc, 4.0, (width, height))
                            for idx, frame in enumerate(gif_frames):
                                print('writing frame')
                                out.write(frame)
                                print('wrote frame')
                            out.release()
                            gif_frames = []
                        # dead_zone must be an int > 0 to save an image.
                        dead_zone = 3
                        gif_name = gif_name

                    if diff1 < threshold_integer * END_STRIKE_PERCENTAGE:
                        # iterates dead zone to zero, leaving dead zone condition.
                        # if the diff is less than the end strike percentage, the
                        # dead zone is reduced by 1. Dead zone of 0 will result
                        # in not saving the frame.
                        # end strike percentage set in the initial constants.
                        # still need to find the sweet spot between 1% and 30%.
                        if dead_zone > 0:
                            dead_zone = dead_zone - 1

                    if dead_zone > 0:
                        # save frame for passing the dead_zone condition.
                        cv2.imwrite(im_name, frame1)
                        # save frame to list for writing to gif
                        gif_frames.append(frame1)

                    text = str(f_out) + ', ' + str(diff1)
                    # write threshold data to csv
                    fff.write(text + '\n')
                    fff.flush()
                    # pass frame forward
                    frame0 = frame1
                    if i == n_frames - 1 and gif_frames and len(gif_frames) > 0:
                        # saves a gif at the end of a file
                        gif_frames.pop(0)
                        print('setting writer')
                        out = cv2.VideoWriter(gif_name, fourcc, 4.0, (width, height))
                        for idx, frame in enumerate(gif_frames):
                            print('writing frame')
                            out.write(frame)
                            print('wrote frame')
                        out.release()
                        gif_frames = []
                        dead_zone = 0
            finally:
                # Always close the CSV file when done with this video
                fff.close()
                video.release()  # Also clean up video capture

        self.threadProgress.emit(100)
        print('analysis complete!')
        # statistics for nerds!
        # video_strikes = 'Strikes: ' + str(strikes) + '\n'
        # elapsed_time = 'Process Time: ' + str(int(time.time() - start)) + ' s\n'
        # print(video_strikes)
        # print(elapsed_time)
        # info = video_strikes+elapsed_time
        # looks like calling popups from this thread can cause crashes.
        # For stability, I am removing the info popup. Error popups will be left
        # for now, but need to be fixed.

        # info_popup(info)
        # sends finished signal. Essentially terminates the thread.
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.starvationButton = None
        self.progressBar = None
        self.analysisButton = None
        self.onlyInt = None
        self.thresholdEntry = None
        self.thresholdLabel = None
        self.outputTimestampButton = None
        self.outputFrameNumButton = None
        self.outputFilenameLabel = None
        self.outputFileDirectoryLabel = None
        self.outputFileDirectoryButton = None
        self.inputFileDirectoryLabel = None
        self.inputFileDirectoryButton = None
        self.centralWidget = None
        self.setupUi()

    def setupUi(self):
        # sets up the gui layout itself
        self.setWindowTitle("ZapCapture")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        # directory widgets
        self.inputFileDirectoryButton = QPushButton("Select Input Directory", self)
        self.inputFileDirectoryButton.clicked.connect(self.pick_new_input)
        self.inputFileDirectoryLabel = QLabel(input_folder)
        self.inputFileDirectoryLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.outputFileDirectoryButton = QPushButton("Select Output Directory", self)
        self.outputFileDirectoryButton.clicked.connect(self.pick_new_output)
        self.outputFileDirectoryLabel = QLabel(output_folder)
        self.outputFileDirectoryLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        # file name widgets
        self.outputFilenameLabel = QLabel('Output File Name (❓)')
        self.outputFilenameLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.outputFilenameLabel.setToolTip(
            'Output File Name determines the standard used to give a file name. Frame number will output files as an '
            'integer, while timestamp will output files as a timestamp.')
        self.outputFrameNumButton = QRadioButton("Frame Number")
        self.outputFrameNumButton.setChecked(True)
        self.outputFrameNumButton.toggled.connect(lambda: self.btn_state(self.outputFrameNumButton))
        self.outputTimestampButton = QRadioButton("Timestamp")
        self.outputTimestampButton.setChecked(False)
        self.outputTimestampButton.toggled.connect(
            lambda: self.btn_state(self.outputTimestampButton))
        # threshold widget
        self.thresholdLabel = QLabel("Threshold (❓)", self)
        self.thresholdLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.thresholdLabel.setToolTip(
            'Threshold determines the sensitivity of the computer vision algorithm. High thresholds will execute quickly with few output images, while low thresholds will potentially detect every frame of the video as a lightning event. Each video in your folder may need an individually tuned threshold; in this case, make subfolders for videos from the same camera and event. For example, separate your dash-cam footage and stationary camera footage. Nighttime footage can require thresholds around 10 million, while daytime footage can be as low as 10 thousand.')
        self.thresholdEntry = QLineEdit(threshold)
        # restricts the threshold to be numbers only
        self.onlyInt = QIntValidator()
        self.thresholdEntry.setValidator(self.onlyInt)
        self.analysisButton = QPushButton('Perform Analysis', self)
        # self.analysisButton.clicked.connect(self.analysis)
        self.analysisButton.clicked.connect(self.runLongTask)
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.progressBar.setValue(0)
        # monetization to prevent starvation
        link_template = '<a href={0}>{1}</a>'
        self.starvationButton = HyperlinkLabel(self)
        starvation_message = '''Like ZapCapture? Consider buying me a coffee!'''
        self.starvationButton.setText(
            link_template.format('https://www.buymeacoffee.com/Blablabliam', starvation_message))

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.inputFileDirectoryButton)
        layout.addWidget(self.inputFileDirectoryLabel)
        layout.addWidget(self.outputFileDirectoryButton)
        layout.addWidget(self.outputFileDirectoryLabel)
        layout.addWidget(self.outputFilenameLabel)
        layout.addWidget(self.outputFrameNumButton)
        layout.addWidget(self.outputTimestampButton)
        layout.addWidget(self.thresholdLabel)
        layout.addWidget(self.thresholdEntry)
        layout.addWidget(self.analysisButton)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.starvationButton)
        self.centralWidget.setLayout(layout)

    def pick_new_input(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Input Folder")
        global input_folder
        input_folder = str(folder_path)
        self.inputFileDirectoryLabel.setText(str(folder_path))
        # reset the progress bar to 0
        self.progressBar.setValue(0)
        self.analysisButton.setEnabled(True)

    def pick_new_output(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Output Folder")
        global output_folder
        output_folder = str(folder_path)
        self.outputFileDirectoryLabel.setText(str(folder_path))
        # reset the progress bar to 0
        self.progressBar.setValue(0)
        self.analysisButton.setEnabled(True)

    def btn_state(self, b):
        global buttonState
        if b.text() == "Frame Number":
            if b.isChecked():
                buttonState = True
                print(b.text() + " is selected")
            else:
                buttonState = False
                print(b.text() + " is deselected")

    def clear_output_folder(self):
        """Clear all files and subdirectories from the output folder before starting analysis."""
        global output_folder

        # Check if output folder is set and exists
        if output_folder and output_folder != 'No Folder Chosen' and os.path.exists(output_folder):
            try:
                import shutil
                files_removed = 0
                dirs_removed = 0

                # Get list of all items in the output folder
                for filename in os.listdir(output_folder):
                    file_path = os.path.join(output_folder, filename)

                    if os.path.isfile(file_path):
                        # Remove files
                        os.remove(file_path)
                        files_removed += 1
                    elif os.path.isdir(file_path):
                        # Remove directories and all their contents
                        shutil.rmtree(file_path)
                        dirs_removed += 1

                print(f"Cleared output folder: {files_removed} files and {dirs_removed} directories removed")
            except Exception as e:
                print(f"Error clearing output folder: {e}")
                # Show error message to user
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Warning")
                msg.setText(f"Could not clear output folder: {e}")
                msg.exec()

    def runLongTask(self):
        # Validate input and output folders before starting analysis
        global input_folder, output_folder, threshold

        # Check if input folder is selected and valid
        if not input_folder or input_folder == 'No Folder Chosen':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Required")
            msg.setText("Please select an input folder before starting analysis.")
            msg.exec()
            return

        if not os.path.exists(input_folder):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Input Folder")
            msg.setText("The selected input folder does not exist. Please select a valid input folder.")
            msg.exec()
            return

        # Check if output folder is selected and valid
        if not output_folder or output_folder == 'No Folder Chosen':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Output Required")
            msg.setText("Please select an output folder before starting analysis.")
            msg.exec()
            return

        if not os.path.exists(output_folder):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Output Folder")
            msg.setText("The selected output folder does not exist. Please select a valid output folder.")
            msg.exec()
            return

        # Clear the output folder before starting analysis
        self.clear_output_folder()

        # set the threshold
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

        # Final resets
        self.analysisButton.setEnabled(False)
        self.thread.finished.connect(self.enableAnalysisButton)
        # self.thread.finished.connect(
        #     lambda: self.analysisButton.setEnabled(True)
        # )

    def onCountChanged(self, value):
        self.progressBar.setValue(value)

    def enableAnalysisButton(self):
        self.analysisButton.setEnabled(True)


app = QApplication(sys.argv)

# Dark Mode code
# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
app.setPalette(palette)

# finish building window
win = Window()
win.show()
sys.exit(app.exec())
