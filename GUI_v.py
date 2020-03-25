
# PyQt5 Video player
#!/usr/bin/env python

from Canny_v import gradient, non_max_suppression_with_threshold_and_hystersis,sobel_edge_with_gaussian

from PyQt5.QtCore import QDir, Qt, QUrl, QThread,pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProgressBar

import cv2
import sys
import numpy as np

maxframe = 0
fileName=''
exportName =''

class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        global maxframe
        print(fileName)
        print(exportName)
        cap = cv2.VideoCapture(fileName)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        maxframe = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')
        out = cv2.VideoWriter(exportName, fourcc, 20.0, (width , height))
        edge_fil_x = np.asarray([[-1, 0, 1],
                                 [-2, 0, 2],
                                 [-1, 0, 1]])
        edge_fil_y = np.flip(edge_fil_x.T, axis=0)
        currentframe = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                g_x, g_y = sobel_edge_with_gaussian(grayFrame,edge_fil_x,edge_fil_y)
                print("thread here")
                g, d = gradient(g_x, g_y)
                V = non_max_suppression_with_threshold_and_hystersis(g, d)

                V = np.array(V, dtype=np.float32)

                # write the flipped frame
                currentframe +=  1
                self.countChanged.emit(currentframe)
                out.write(cv2.cvtColor(V, cv2.COLOR_GRAY2BGR))
                print(currentframe)
                #cv2.imshow('frame', V)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                 #   break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()




class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Canny Video Player")
        self.calc = External()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.progress = QProgressBar()


        self.show()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.convertButton = QPushButton('Convert')
        self.convertButton.setEnabled(True)
        self.convertButton.clicked.connect(self.convert_canny)


        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('Import.png'), '&Import', self)
        # openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create export action
        exportAction = QAction(QIcon('export.png'), '&Export', self)
        # exportAction.setShortcut('Ctrl+Q')
        exportAction.setStatusTip('Export Movie')
        exportAction.triggered.connect(self.exportfile)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exportAction)





        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        progressbar = QProgressBar()


        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.progress)



        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        global fileName
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)", QDir.homePath())

        if fileName != '':
            print(fileName)
            self.statusBar().showMessage('Now playing()'.format(fileName))
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.play()


        return fileName



    def exportfile(self):
        global exportName
        ###export to folder

        exportName,_ = QFileDialog.getSaveFileName(self, "Export Movie", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)", QDir.homePath())
        print(exportName)
        return exportName

        # sys.exit(app.exec_())


    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def onCountChanged(self, value):
        self.progress.setMaximum(maxframe)
        self.progress.setValue(value)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
    def convert_canny(self):
        print("Converting..")
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()
        self.progress.setMaximum(maxframe)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()

    sys.exit(app.exec_())
