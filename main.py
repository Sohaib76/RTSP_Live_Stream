
from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
# from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui



class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''
    def __init__(self):
        super().__init__()
        # 1. Window settings
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Matplotlib live plot in PyQt - example 2")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QVBoxLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        self.lyt.addWidget(self.myFig)

        # 3. Show
        self.show()
        return


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0) #rtsp
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        

            # listx.append(r.randint(0,10))
            # listy.append(r.randint(0,10))
            #print(listx)
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RTSP Live Feed")
        self.disply_width = 450
        self.display_height = 300 #280
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.move(40,40)
        self.image_label.resize(self.disply_width, self.display_height)
        self.textLabel = QtWidgets.QLabel('Webcam')



        #######################Customization

        self.left = 10
        self.top = 10
        self.width = 700
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
        self.analytics = self.viewMenu.addAction("&Analytics")
        self.analytics.triggered.connect(self.openChart)


        # create frame for a set of checkbox
        self.frame1 = QtWidgets.QGroupBox(self)
        self.frame1.setGeometry(QtCore.QRect(40, 40, 450, 300))
        self.frame1.move(40, 40)




        #Right Frame
        self.frame2 = QtWidgets.QGroupBox(self)
        self.frame2.setGeometry(QtCore.QRect(510, 40, 170, 300))
        self.frame1.move(40, 40)


        # self.radioBtn1 = QtWidgets.QRadioButton("Yes", self.frame2)
        # self.radioBtn1.setChecked(True)  # select by default
        # self.radioBtn1.move(10, 10)

        

        # self.spinbox1 = QtWidgets.QSpinBox(self.frame2)
        # self.spinbox1.setValue(3) # default value
        # self.spinbox1.setMinimum(0) # minimum value
        # self.spinbox1.setMaximum(6) # maximum value
        # self.spinbox1.move(10, 100)

        self.label = QtWidgets.QLabel('Select Model', self.frame2)
        self.label.move(10,20)

        comboBox = QtWidgets.QComboBox(self.frame2)
        comboBox.addItem("Yolov5")
        comboBox.addItem("Yolact")
        comboBox.addItem("UNet")
        comboBox.addItem("Other")
        # comboBox.move(50, 50)
        comboBox.setGeometry(10,50, 150, 30)
        comboBox.activated[str].connect(self.model_choice)


        self.label = QtWidgets.QLabel('Select Features', self.frame2)
        self.label.move(10,120)
        self.checkbox1 = QtWidgets.QCheckBox("People Count", self.frame2)
        self.checkbox1.setChecked(False)  # select by default
        self.checkbox1.move(10, 140)
        self.checkbox2 = QtWidgets.QCheckBox("Gender Identification", self.frame2)
        self.checkbox2.setChecked(False)  # select by default
        self.checkbox2.move(10, 170)
        self.checkbox3 = QtWidgets.QCheckBox("Face Recognition", self.frame2)
        self.checkbox3.setChecked(False)  # select by default
        self.checkbox3.move(10, 200)
        x = self.checkbox3.isChecked()
        print("Face Recognition checked", x)
    




        ####################################

        # create a vertical box layout and add the two labels
        vbox = QtWidgets.QVBoxLayout()
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

    def model_choice(self,text):
        print("model selected", text)

    def openChart(self):
        print("Clicked")
        # self.char = ChartWindow()
        # self.char.show()
        # chart = Canvas(self)
        chart = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        chart.show()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @QtCore.pyqtSlot(np.ndarray)
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







class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,

# Data source
# ------------
n = np.linspace(0, 499, 500)
d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
i = 0
def get_next_datapoint():
    global i
    i += 1
    if i > 499:
        i = 0
    return d[i]

# if __name__ == "__main__":
#     qapp = QtWidgets.QApplication(sys.argv)
#     app = ApplicationWindow()
#     qapp.exec_()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
