import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets                     # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                             QLabel, QVBoxLayout)              # +++

from test2_ui import Ui_Form                                   # +++
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 10.0,(640,480))
class video (QtWidgets.QDialog, Ui_Form):

    def __init__(self):
        super().__init__()                  

#        uic.loadUi('test2.ui',self)                           # ---
        self.setupUi(self)                                     # +++

        self.control_bt.clicked.connect(self.start_webcam)
        self.record.clicked.connect(self.start_record)
        self.capture.clicked.connect(self.capture_image)
        #self.capture.clicked.connect(self.startUIWindow)       # - ()

        self.image_label.setScaledContents(True)

        self.cap = None                                        #  -capture <-> +cap

        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0

    @QtCore.pyqtSlot()
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        self.timer.start()



    @QtCore.pyqtSlot()
    def start_record(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self.timer.start()
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            self.displayImage(frame, True)
            # write the flipped frame
            self.displayImage(frame, True)
            out.write(frame)
            #cv2.imshow('frame',frame)
            cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                out.release()
        
    @QtCore.pyqtSlot()
    def save_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        self.timer.start()
        
    @QtCore.pyqtSlot()
    def update_frame(self):
        ret, image = self.cap.read()
        simage     = cv2.flip(image, 1)
        self.displayImage(image, True)

    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame = self.cap.read()
        path = '/home/pi'                         # 
        if flag:
            QtWidgets.QApplication.beep()
            name = "my_image.jpg"
            #cv2.imwrite(os.path.join(path, name), frame)
            cv2.imwrite("NewPicture.jpg",frame)
            self._image_counter += 1

    def displayImage(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(outImage))

    def startUIWindow(self):
        self.Window = UIWindow()                               # - self
        self.setWindowTitle("UIWindow")

#        self.setCentralWidget(self.Window)
#        self.show()
### +++ vvv
        self.Window.ToolsBTN.clicked.connect(self.goWindow1)

        self.hide()
        self.Window.show()

    def goWindow1(self):
        self.show()
        self.Window.hide()
### +++ ^^^


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)

        self.resize(300, 300)
        self.label = QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.ToolsBTN = QPushButton('text')
#        self.ToolsBTN.move(50, 350)

        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.ToolsBTN)
        self.setLayout(self.v_box)


if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = video()
    window.setWindowTitle('main code')
    window.show()
    sys.exit(app.exec_())


