# use freeze for requirements.txt

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QApplication, QGroupBox, QWidget, QLabel, QPushButton, QComboBox, QFrame, QMainWindow, QRadioButton, QCheckBox, QSpinBox , QVBoxLayout)
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QRect
import numpy as np
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
import random as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas




listx = []
listy = []


class Canvas(FigureCanvas):
    def __init__(self, parent):
        # fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        # super().__init__(fig)
        # self.setParent(parent)
        fig = plt.figure()
        super().__init__(fig)
        self.ax1 = fig.add_subplot(1,1,1)


        """ 
        Matplotlib Script
        """

        style.use('fivethirtyeight')


        # t = np.arange(0.0, 2.0, 0.01)
        # s = 1 + np.sin(2 * np.pi * t)
        
        # self.ax.plot(t, s)

        # self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        #        title='About as simple as it gets, folks')
        # self.ax.grid()

        xs = [0,1,2,3,4,5,6,7,8,9]
        ys=[3,5,2,6,2,6,3,6,9,2]
        count = 11

        def animate(i):
            print("animate")
            xs.append(count + i)
            ys.append(count + i)
            self.ax.clear()
            self.ax.plot(xs, ys)

        ani = animation.FuncAnimation(fig, animate, interval=1000)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0) #rtsp
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        

            listx.append(r.randint(0,10))
            listy.append(r.randint(0,10))
            #print(listx)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()



# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()


class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100, 680,500)

        #self.show()
        self.create_linechart()

    def create_linechart(self):

        # listx = [0,2,3,7,10]
        # listy = [6,4,8,4,5]
        print(len(listx))

        series = QLineSeries(self)
        for x,y in zip(listx,listy):
            series.append(x,y)
        # series.append(0,6)
        # series.append(2, 4)
        # series.append(3, 8)
        # series.append(7, 4)
        # series.append(10, 5)

        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)


        chart =  QChart()

        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Line Chart Example")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)


        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)

        



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
        self.credits.triggered.connect(self.openChart)

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

    def openChart(self):
        print("Clicked")
        # self.char = ChartWindow()
        # self.char.show()
        chart = Canvas(self)
        chart.show()

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
