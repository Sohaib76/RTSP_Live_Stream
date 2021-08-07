# https://guiguide.readthedocs.io/en/latest/gui/qt.html
#https://pyshine.com/Video-processing-in-Python-with-OpenCV-and-PyQt5-GUI/
#opencv headless, opencv contribute, opencv 3.4
import cv2, imutils , time
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
        QApplication, QGroupBox, QWidget, QLabel, QPushButton, QComboBox, QFrame, QMainWindow, QRadioButton, QCheckBox, QSpinBox , QVBoxLayout)
from PyQt5.QtCore import pyqtSlot, QRect, Qt

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'RTSP Live Feed'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        
        
    

   

        self.widget()



    def widget(self):
        self.setWindowTitle(self.title)
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
        self.frame1.setGeometry(QRect(40, 40, 450, 280))
        self.frame1.move(40, 40)
        
        # selected value will be displayed on label
        self.label1 = QLabel(self.frame1)
        #self.label1.setText("Live Feed")
        self.label1.setGeometry(QRect(30, 30, 500, 280))
        # self.label1.move(40,40)
        self.label1.setPixmap(QtGui.QPixmap("image.png"))
        self.label1.setObjectName("label1")
        
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.label1)
        # self.setLayout(self.layout)

        




        self.frame2 = QGroupBox(self)
        self.frame2.setGeometry(QRect(510, 40, 120, 280))
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

        self.pushButton_2 = QPushButton(self.frame1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Start")
        self.pushButton_2.clicked.connect(self.loadImage)



        # Debugged
     #   self.image = cv2.imread('image2.jpeg')
        # self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        # self.label1.setPixmap(QtGui.QPixmap.fromImage(self.image))

       
        # imag = cv2.imread('image2.jpeg')
        # imag = QtGui.QImage(imag.data, imag.shape[1], imag.shape[0], QtGui.QImage.Format_RGB888)
        # self.label1.setPixmap(QtGui.QPixmap.fromImage(imag))



        #self.show()

    


    def loadImage(self):

        
        cam = True # True for webcam
        if cam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(0)		
        cnt=0
        frames_to_count=20
        st = 0
        fps=0
        
        while(vid.isOpened()):
            img, self.image = vid.read()
            self.image  = imutils.resize(self.image ,height = 480 )
			
			# gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
			# faces = faceCascade.detectMultiScale(
			# gray,
			# scaleFactor=1.15,  
			# minNeighbors=7, 
			# minSize=(80, 80), 
			# flags=cv2.CASCADE_SCALE_IMAGE)
			
			# for (x, y, w, h) in faces:
			# 	cv2.rectangle(self.image, (x, y), (x + w, y + h), (10, 228,220), 5) 
            # 
            if cnt == frames_to_count:
                try: # To avoid divide by 0 we put it in try except
                    print(frames_to_count/(time.time()-st),'FPS') 
                    self.fps = round(frames_to_count/(time.time()-st)) 
                    
                    st = time.time()
                    cnt=0
                    
                except:
                    pass
                
            cnt+=1
            
            self.update()
            #self.setPhoto()
            # key = cv2.waitKey(1)
            # if key == ord("q"):
            #     break

    def setPhoto(self,image):

        imag = cv2.imread('image2.jpeg')
        imag = QtGui.QImage(imag.data, imag.shape[1], imag.shape[0], QtGui.QImage.Format_RGB888)
        self.label1.setPixmap(QtGui.QPixmap.fromImage(imag))
        print(self.label1)
        label = self.findChild(QLabel, "label1")
        print(label)


        print("photo")
        self.tmp = image
        image = imutils.resize(image,width=640)
        # frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        # self.label1.setPixmap(QPixmap.fromImage(image))



        img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label1.setPixmap(QtGui.QPixmap.fromImage(img))
        # self.resize(pixmap.width(),pixmap.height())


       




        # self.filename = 'Snapshot '+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        # cv2.imwrite(self.filename,self.tmp)
        # print('Image saved as:',self.filename)


        # label = QLabel(self)
        # pixmap = QPixmap('image.png')
        # label.setPixmap(pixmap)
        # self.resize(pixmap.width(),pixmap.height())
	
    def update(self):
            img = self.image
            self.setPhoto(img)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())













# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel

# def main():
#     app = QApplication(sys.argv)
#     w = QWidget()

#     # create label
#     b = QLabel(w)
#     b.setText("Hello World") # text value
#     b.move(75, 75) # location of label


#     c = QLabel(w)
#     c.setText("Bye World") # text value
#     c.move(175, 75) # location of label

#     # title for widget
#     w.setWindowTitle("PyQt5")

#     # left margin, top margin, width, height
#     # w.setGeometry(250, 250, 200, 150)
#     # or use below two lines
#     w.resize(720, 680)
#     w.move(250, 250)

#     w.show()


#     x = QWidget()
#     x.move(100, 100)
#     x.resize(200,200)
    
#     x.show()

#     # wait to exit
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()


# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# from PyQt5.QtGui import QIcon, QPixmap

# class App(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 image - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()
    
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
    
#         # Create widget
#         label = QLabel(self)
#         pixmap = QPixmap('image.png')
#         label.setPixmap(pixmap)
#         self.resize(pixmap.width(),pixmap.height())
        
#         self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

