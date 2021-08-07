from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QApplication, QGroupBox, QWidget, QLabel, QPushButton, QComboBox, QFrame, QMainWindow, QRadioButton, QCheckBox, QSpinBox , QVBoxLayout)
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QRect
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()



# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 450
        self.display_height = 300 #280
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.move(40,40)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')



        #######################Customization

        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        


        self.menubar= self.menuBar() # add menu bar
        self.fileMenu = self.menubar.addMenu("&File")
        self.editMenu = self.menubar.addMenu("&Edit")
        self.viewMenu = self.menubar.addMenu("&View")
        self.helpMenu = self.menubar.addMenu("&Help")  # Add Help in menu bar
        self.about = self.helpMenu.addAction("&About")  # Add option in Help
        self.about.setShortcut("F11") # display F11 as shortcut
        self.credits = self.helpMenu.addAction("&Credits") # Add another option in Help

        # create frame for a set of checkbox
        self.frame1 = QGroupBox(self)
        self.frame1.setGeometry(QRect(40, 40, 450, 300))
        self.frame1.move(40, 40)




        #Right Frame
        self.frame2 = QGroupBox(self)
        self.frame2.setGeometry(QRect(510, 40, 120, 300))
        self.frame1.move(40, 40)


        self.radioBtn1 = QRadioButton("Yes", self.frame2)
        self.radioBtn1.setChecked(True)  # select by default
        self.radioBtn1.move(10, 10)

        self.checkbox1 = QCheckBox("C++", self.frame2)
        self.checkbox1.setChecked(True)  # select by default
        self.checkbox1.move(10, 50)

        self.spinbox1 = QSpinBox(self.frame2)
        self.spinbox1.setValue(3) # default value
        self.spinbox1.setMinimum(0) # minimum value
        self.spinbox1.setMaximum(6) # maximum value
        self.spinbox1.move(10, 100)




        ####################################

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, ) #Qt.KeepAspectRatio
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
