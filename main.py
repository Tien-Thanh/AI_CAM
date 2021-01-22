# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStyle
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2
import datetime
from datetime import date
from datetime import datetime
import os
import os.path
from os import path
from pathlib import Path
import re
import time
import numpy as np
import smtplib
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from PIL import Image
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

from ui import *
from check import *
from detect import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form2()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.openwindow)
    def openwindow(self):
        self.mon = self.ui.checkBox.isChecked()
        self.car = self.ui.checkBox_2.isChecked()
        self.ill = self.ui.checkBox_3.isChecked()
        self.person = self.ui.checkBox_4.isChecked()

        self.window = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        mainWindow.hide()
        self.window.show()
        self.points_CAM1 = []
        self.points_CAM2 = []
        self.points_CAM3 = []
        self.points_CAM4 = []
        self.ui.Mon_1.setVisible(self.mon)
        self.ui.Car_1.setVisible(self.car)
        self.ui.Ill_1.setVisible(self.ill)
        self.ui.Per_1.setVisible(self.person)

        self.ui.Mon_2.setVisible(self.mon)
        self.ui.Car_2.setVisible(self.car)
        self.ui.Ill_2.setVisible(self.ill)
        self.ui.Per_2.setVisible(self.person)

        self.ui.Mon_3.setVisible(self.mon)
        self.ui.Car_3.setVisible(self.car)
        self.ui.Ill_3.setVisible(self.ill)
        self.ui.Per_3.setVisible(self.person)

        self.ui.Mon_4.setVisible(self.mon)
        self.ui.Car_4.setVisible(self.car)
        self.ui.Ill_4.setVisible(self.ill)
        self.ui.Per_4.setVisible(self.person)

        # create timers
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.timer4 = QTimer()

        # set timer timeout callback function
        self.timer1.timeout.connect(self.viewCam1)
        self.timer2.timeout.connect(self.viewCam2)
        self.timer3.timeout.connect(self.viewCam3)
        self.timer4.timeout.connect(self.viewCam4)

        self.timer1.timeout.connect(self.show_detect)
        self.ui.Start_1.clicked.connect(self.controlTimer11)
        self.ui.Stop_1.clicked.connect(self.controlTimer12)
        self.timer2.timeout.connect(self.show_detect2)
        self.ui.Start_2.clicked.connect(self.controlTimer21)
        self.ui.Stop_2.clicked.connect(self.controlTimer22)
        self.timer3.timeout.connect(self.show_detect3)
        self.ui.Start_3.clicked.connect(self.controlTimer31)
        self.ui.Stop_3.clicked.connect(self.controlTimer32)
        self.timer4.timeout.connect(self.show_detect4)
        self.ui.Start_4.clicked.connect(self.controlTimer41)
        self.ui.Stop_4.clicked.connect(self.controlTimer42)

        self.ui.Cam_Draw_1.mousePressEvent = self.mouseEventCAM1
        self.ui.Draw_1.clicked.connect(self.startDrawAreaCAM1)
        self.ui.Clear_1.clicked.connect(self.removeAreaCAM1)
        self.ui.Mon_1.clicked.connect(self.detect_object)

        self.ui.Cam_Draw_2.mousePressEvent = self.mouseEventCAM2
        self.ui.Draw_2.clicked.connect(self.startDrawAreaCAM2)
        self.ui.Clear_2.clicked.connect(self.removeAreaCAM2)
        self.ui.Mon_2.clicked.connect(self.detect_object2)

        self.ui.Cam_Draw_3.mousePressEvent = self.mouseEventCAM3
        self.ui.Draw_3.clicked.connect(self.startDrawAreaCAM3)
        self.ui.Clear_3.clicked.connect(self.removeAreaCAM3)
        self.ui.Mon_3.clicked.connect(self.detect_object3)

        self.ui.Cam_Draw_4.mousePressEvent = self.mouseEventCAM4
        self.ui.Draw_4.clicked.connect(self.startDrawAreaCAM4)
        self.ui.Clear_4.clicked.connect(self.removeAreaCAM4)
        self.ui.Mon_4.clicked.connect(self.detect_object4)
        
        self.ui.openBtn.clicked.connect(self.open_file)
        self.ui.playBtn.clicked.connect(self.play_video)
        self.ui.volumeBtn.clicked.connect(self.mute_video)
        self.ui.slider.sliderMoved.connect(self.set_position)
        self.ui.volume_slider.sliderMoved.connect(self.set_volume)
        #self.ui.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.ui.mediaPlayer.positionChanged.connect(self.position_changed)
        self.ui.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.ui.fullscreenBtn.clicked.connect(self.full_screen)
        self.ui.fastBtn.clicked.connect(self.fast)
        self.ui.slowBtn.clicked.connect(self.slow)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.ui.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.ui.playBtn.setEnabled(True)
            self.ui.fastBtn.setEnabled(True)
            self.ui.slowBtn.setEnabled(True)
        
    def mute_video(self):
        if not self.ui.mediaPlayer.isMuted():
            self.ui.mediaPlayer.setMuted(True)
            self.ui.volumeBtn.setIcon(
                self.ui.tab_2.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.ui.mediaPlayer.setMuted(False)
            self.ui.volumeBtn.setIcon(
                self.ui.tab_2.style().standardIcon(QStyle.SP_MediaVolume))

    def play_video(self):
        if self.ui.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.mediaPlayer.pause()

        else:
            self.ui.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.ui.tab_2.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.tab_2.playBtn.setIcon(
                self.ui.tab_2.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.ui.tab_2.playBtn.setIcon(
                self.ui.tab_2.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def set_volume(self, volume):
        self.ui.mediaPlayer.setVolume(volume)

    def position_changed(self, position):
        self.ui.slider.setValue(position)

    def duration_changed(self, duration):
        self.ui.slider.setRange(0, duration)

    def set_position(self, position):
        self.ui.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.ui.tab_2.playBtn.setEnabled(False)
        self.ui.tab_2.label.setText("Error: " + self.ui.tab_2.mediaPlayer.errorString())

    def full_screen(self):
        if self.window.isFullScreen() == False:
            self.window.showFullScreen()
            self.ui.fullscreenBtn.setText("Exit")
        else:
            self.window.showNormal()
            self.ui.fullscreenBtn.setText("Full Screen")

    def fast(self):
        self.ui.mediaPlayer.setPosition(self.ui.mediaPlayer.position() + 10*60)

    def slow(self):
        self.ui.mediaPlayer.setPosition(self.ui.mediaPlayer.position() - 10*60)

    def image_to_QImage(self, image, label):
        image = cv2.resize(image, (label.width()-2, label.height()-20))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        step = channel * width
        return QImage(image.data, width, height, step, QImage.Format_RGB888)

    def createDir(self, IP_CAM: str):
        today = date.today()
        month = today.strftime("%m")
        year = today.strftime("%Y")

        os.chdir('/home/hades/')
        if os.path.exists("project") == False:
            os.mkdir('project')
        os.chdir('/home/hades/project')
        if os.path.exists("IVA") == False:
            os.mkdir('IVA')
        os.chdir('/home/hades/project/IVA')
        if os.path.exists(IP_CAM) == False:
            os.mkdir(IP_CAM)
        os.chdir('/home/hades/project/IVA/' + IP_CAM)
        if os.path.exists("Nam " + year) == False:
            os.mkdir("Nam " + str(year))
        os.chdir('/home/hades/project/IVA/'+ IP_CAM + '/' + "Nam " + year)
        if os.path.exists("Thang " + month) == False:
            os.mkdir("Thang " + str(month))
        os.chdir('/home/hades/project/IVA/' + IP_CAM + '/' + "Nam " + year + '/' + "Thang " + month)


    # view camera 1
    def viewCam1(self):
        ret, image = self.cap1.read()
        self.out1.write(image)
        image1 = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image,(464,293))
        # get image infos
        height, width, channel = image_resized.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image_resized.data, width, height, step, QImage.Format_RGB888)
        self.ui.Cam_Draw_1.setPixmap(QPixmap.fromImage(
           self.image_to_QImage(self.drawArea(image1, self.points_CAM1, self.ui.Cam_Draw_1), self.ui.Cam_Draw_1)))
        if self.flag == 0:
           self.ui.Cam_1.setPixmap(QPixmap.fromImage(qImg))
    time_start1 = 0
    time_stop1 = 0
    Flag_CAM1 = 0
    def controlTimer11(self):
        # if timer is stopped
        if not self.timer1.isActive():
            # create video capture
            self.cap1 = cv2.VideoCapture('/home/hades/DA3/Video1.avi')
            self.createDir('IP_CAM_1')
            self.Flag_CAM1 = self.cap1.isOpened()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(self.cap1.get(3))
            frame_height = int(self.cap1.get(4))
            self.out1 = cv2.VideoWriter('output.avi', fourcc, 30, (frame_width, frame_height))
            now = datetime.now()
            self.date11 = now.strftime("%d-%m")
            self.time_start1 = now.strftime(" %H:%M:%S-")
            # start timer
            self.timer1.start(20)
        # if timer is started
    def controlTimer12(self):
        # stop timer
        self.timer1.stop()
        self.cap1.release()
        self.out1.release()
        now = datetime.now()
        self.time_stop1 = now.strftime(" %H:%M:%S")
        self.date12 = now.strftime("%d-%m")
        fileName = str(self.date11) + str(self.time_start1) +"->" + str(self.date12) + str(self.time_stop1) + '.avi'
        self.createDir('IP_CAM_1')
        os.rename('output.avi', fileName)


    def mouseEventCAM1(self, event):
        if self.Flag_CAM1 == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.points_CAM1.append([x, y])
            print("Position clicked is ({}, {})".format(x, y))
    def startDrawAreaCAM1(self):
        self.Flag_CAM1 = 1

    def removeAreaCAM1(self):
        while len(self.points_CAM1):
            self.points_CAM1.pop()

    def drawArea(self, image, points: list, qlabel: QtWidgets.QLabel):
        image_draw = image.copy()
        image_draw = cv2.resize(image_draw, (qlabel.width() , qlabel.height()))
        # print(len(points))
        if len(points) > 1:
            image_draw = cv2.polylines(image_draw, np.array([points]),1,  (0, 255, 255), 1)
            self.contour = np.array([points]).reshape((-1,1,2)).astype(np.int32)
            #print(self.contour.shape)
            self.flag1 = 1
            b, g, r = cv2.split(image_draw)
            cv2.fillPoly(b, np.array([points]), (0, 255, 0))
            cv2.fillPoly(r, np.array([points]), (0, 255, 0))
            image_draw = cv2.merge([b, g, r])
        return image_draw
    flag1 = 0
    flag = 0
    class_ids = []
    confidences = []
    boxes = []
    flag2 = 0

    def detect_object(self):
        if self.timer1.isActive():
            self.flag = 1
    def show_detect(self):
        #while (cap.isOpened()):
        ret, frame = self.cap1.read()
        frame = cv2.resize(frame, (464, 293))
        boxes, confidences, class_ids = Detect_person(frame = frame, boxes = self.boxes, confidences = self.confidences, class_ids = self.class_ids)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)
            if self.flag1 == 1:
                dist1 = cv2.pointPolygonTest(self.contour, (x, y ), False)
                dist2 = cv2.pointPolygonTest(self.contour, (x, y + h), False)
                dist3 = cv2.pointPolygonTest(self.contour, (x + w, y), False)
                dist4 = cv2.pointPolygonTest(self.contour, (x + w, y + h), False)
            #print(dist1,dist2,dist3,dist4)
                if ((dist1==1) or (dist2==1) or (dist3==1) or (dist4==1)) and self.flag2 == 0:
                    print("Canh bao co xam nhap 1")
                    content = 'Canh bao co xam nhap'
                    #mail = smtplib.SMTP('smtp.gmail.com', 587)
                    #mail.ehlo()
                    #mail.starttls()
                    #mail.login('whitelion1080@gmail.com', 'password')
                    #mail.sendmail('whitelion1080@gmail.com', 'thanh.daotien26@gmail.com', content)
                    #mail.close()
                    self.flag2 = 1

        remove_list(self.boxes)
        remove_list(self.confidences)
        remove_list(self.class_ids)
        frame1 = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(464,293))
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)

        #print(self.bkg_list1)
        if self.flag == 1:
            self.ui.Cam_Draw_1.setPixmap(
                QPixmap.fromImage(self.image_to_QImage(self.drawArea(frame1, self.points_CAM1, self.ui.Cam_Draw_1),
                                                       self.ui.Cam_Draw_1)))
            self.ui.Cam_1.setPixmap(QPixmap.fromImage(qImg))

    #view camera 2

    def viewCam2(self):
        ret, image = self.cap2.read()
        self.out2.write(image)
        image1 = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image,(464,293))
        # get image infos
        height, width, channel = image_resized.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image_resized.data, width, height, step, QImage.Format_RGB888)
        self.ui.Cam_Draw_2.setPixmap(QPixmap.fromImage(
           self.image_to_QImage(self.drawArea2(image1, self.points_CAM2, self.ui.Cam_Draw_2), self.ui.Cam_Draw_2)))
        #if self.flag == 0:
        self.ui.Cam_2.setPixmap(QPixmap.fromImage(qImg))
    time_start2 = 0
    time_stop2 = 0
    Flag_CAM2 = 0
    def controlTimer21(self):
        # if timer is stopped
        if not self.timer2.isActive():
            # create video capture
            self.cap2 = cv2.VideoCapture(0)
            self.createDir('IP_CAM_2')
            self.Flag_CAM2 = self.cap2.isOpened()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(self.cap2.get(3))
            frame_height = int(self.cap2.get(4))
            self.out2 = cv2.VideoWriter('output.avi', fourcc, 30, (frame_width, frame_height))
            now = datetime.now()
            self.date21 = now.strftime("%d-%m")
            self.time_start2 = now.strftime(" %H:%M:%S-")
            # start timer
            self.timer2.start(20)
        # if timer is started
    def controlTimer22(self):
        # stop timer
        self.timer2.stop()
        self.cap2.release()
        self.out2.release()
        now = datetime.now()
        self.time_stop2 = now.strftime(" %H:%M:%S")
        self.date22 = now.strftime("%d-%m")
        fileName = str(self.date21) + str(self.time_start2) +"->" + str(self.date22) + str(self.time_stop2) + '.avi'
        self.createDir('IP_CAM_2')
        os.rename('output.avi', fileName)


    def mouseEventCAM2(self, event):
        if self.Flag_CAM2 == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.points_CAM2.append([x, y])
            print("Position clicked is ({}, {})".format(x, y))
    def startDrawAreaCAM2(self):
        self.Flag_CAM2 = 1

    def removeAreaCAM2(self):
        while len(self.points_CAM2):
            self.points_CAM2.pop()

    def drawArea2(self, image, points: list, qlabel: QtWidgets.QLabel):
        image_draw = image.copy()
        image_draw = cv2.resize(image_draw, (qlabel.width() , qlabel.height()))
        # print(len(points))
        if len(points) > 1:
            image_draw = cv2.polylines(image_draw, np.array([points]),1,  (0, 255, 255), 1)
            self.contour2 = np.array([points]).reshape((-1,1,2)).astype(np.int32)
            self.flag21 = 1
            b, g, r = cv2.split(image_draw)
            cv2.fillPoly(b, np.array([points]), (0, 255, 0))
            cv2.fillPoly(r, np.array([points]), (0, 255, 0))
            image_draw = cv2.merge([b, g, r])
        return image_draw
    flag21 = 0
    flag20 = 0
    class_ids2 = []
    confidences2 = []
    boxes2 = []
    flag22 = 0

    def detect_object2(self):
       if self.timer2.isActive():
            self.flag20 = 1
    def show_detect2(self):
        #while (cap.isOpened()):
        ret, frame = self.cap2.read()
        frame = cv2.resize(frame, (464, 293))
        boxes, confidences, class_ids = Detect_person(frame = frame, boxes = self.boxes2, confidences = self.confidences2, class_ids = self.class_ids2)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)
            if self.flag21 == 1:
                dist1 = cv2.pointPolygonTest(self.contour2, (x, y ), False)
                dist2 = cv2.pointPolygonTest(self.contour2, (x, y + h), False)
                dist3 = cv2.pointPolygonTest(self.contour2, (x + w, y), False)
                dist4 = cv2.pointPolygonTest(self.contour2, (x + w, y + h), False)
            #print(dist1,dist2,dist3,dist4)
                if ((dist1==1) or (dist2==1) or (dist3==1) or (dist4==1)) and self.flag22 == 0:
                    print("Canh bao co xam nhap 2")
                    content = 'Canh bao co xam nhap'
                    #mail = smtplib.SMTP('smtp.gmail.com', 587)
                    #mail.ehlo()
                    #mail.starttls()
                    #mail.login('whitelion1080@gmail.com', 'password')
                    #mail.sendmail('whitelion1080@gmail.com', 'thanh.daotien26@gmail.com', content)
                    #mail.close()
                    self.flag22 = 1

        remove_list(self.boxes2)
        remove_list(self.confidences2)
        remove_list(self.class_ids2)
        frame1 = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(464,293))
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        #print(self.bkg_list1)
        if self.flag20 == 1:
            self.ui.Cam_Draw_2.setPixmap(
                QPixmap.fromImage(self.image_to_QImage(self.drawArea2(frame1, self.points_CAM2, self.ui.Cam_Draw_2),
                                                       self.ui.Cam_Draw_2)))
            self.ui.Cam_2.setPixmap(QPixmap.fromImage(qImg))

    def viewCam3(self):
        ret, image = self.cap3.read()
        self.out3.write(image)
        image1 = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image,(464,293))
        # get image infos
        height, width, channel = image_resized.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image_resized.data, width, height, step, QImage.Format_RGB888)
        self.ui.Cam_Draw_3.setPixmap(QPixmap.fromImage(
           self.image_to_QImage(self.drawArea3(image1, self.points_CAM3, self.ui.Cam_Draw_3), self.ui.Cam_Draw_3)))
        #if self.flag == 0:
        self.ui.Cam_3.setPixmap(QPixmap.fromImage(qImg))
    time_start3 = 0
    time_stop3 = 0
    Flag_CAM3 = 0
    def controlTimer31(self):
        # if timer is stopped
        if not self.timer3.isActive():
            # create video capture
            self.cap3 = cv2.VideoCapture('/home/hades/Documents/video_task_7.mp4')
            self.createDir('IP_CAM_3')
            self.Flag_CAM3 = self.cap3.isOpened()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(self.cap3.get(3))
            frame_height = int(self.cap3.get(4))
            self.out3 = cv2.VideoWriter('output.avi', fourcc, 30, (frame_width, frame_height))
            now = datetime.now()
            self.date31 = now.strftime("%d-%m")
            self.time_start3 = now.strftime(" %H:%M:%S-")
            # start timer
            self.timer3.start(20)
        # if timer is started
    def controlTimer32(self):
        # stop timer
        self.timer3.stop()
        self.cap3.release()
        self.out3.release()
        now1 = datetime.now()
        self.time_stop3 = now1.strftime(" %H:%M:%S")
        self.date32 = now1.strftime("%d-%m")
        fileName = str(self.date31) + str(self.time_start3) +"->" + str(self.date32) + str(self.time_stop3) + '.avi'
        self.createDir('IP_CAM_3')
        os.rename('output.avi', fileName)


    def mouseEventCAM3(self, event):
        if self.Flag_CAM3 == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.points_CAM3.append([x, y])
            print("Position clicked is ({}, {})".format(x, y))
    def startDrawAreaCAM3(self):
        self.Flag_CAM3 = 1

    def removeAreaCAM3(self):
        while len(self.points_CAM3):
            self.points_CAM3.pop()

    def drawArea3(self, image, points: list, qlabel: QtWidgets.QLabel):
        image_draw = image.copy()
        image_draw = cv2.resize(image_draw, (qlabel.width() , qlabel.height()))
        # print(len(points))
        if len(points) > 1:
            image_draw = cv2.polylines(image_draw, np.array([points]),1,  (0, 255, 255), 1)
            self.contour3 = np.array([points]).reshape((-1,1,2)).astype(np.int32)
            self.flag31 = 1
            b, g, r = cv2.split(image_draw)
            cv2.fillPoly(b, np.array([points]), (0, 255, 0))
            cv2.fillPoly(r, np.array([points]), (0, 255, 0))
            image_draw = cv2.merge([b, g, r])
        return image_draw
    flag31 = 0
    flag30 = 0
    class_ids3 = []
    confidences3 = []
    boxes3 = []
    flag32 = 0

    def detect_object3(self):
        if self.timer3.isActive():
            self.flag30 = 1
    def show_detect3(self):
        #while (cap.isOpened()):
        ret, frame = self.cap3.read()
        frame = cv2.resize(frame, (464, 293))
        boxes, confidences, class_ids = Detect_person(frame = frame, boxes = self.boxes3, confidences = self.confidences3, class_ids = self.class_ids3)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)
            if self.flag31 == 1:
                dist1 = cv2.pointPolygonTest(self.contour3, (x, y ), False)
                dist2 = cv2.pointPolygonTest(self.contour3, (x, y + h), False)
                dist3 = cv2.pointPolygonTest(self.contour3, (x + w, y), False)
                dist4 = cv2.pointPolygonTest(self.contour3, (x + w, y + h), False)
            #print(dist1,dist2,dist3,dist4)
                if ((dist1==1) or (dist2==1) or (dist3==1) or (dist4==1)) and self.flag32 == 0:
                    print("Canh bao co xam nhap 3")
                    content = 'Canh bao co xam nhap'
                    #mail = smtplib.SMTP('smtp.gmail.com', 587)
                    #mail.ehlo()
                    #mail.starttls()
                    #mail.login('whitelion1080@gmail.com', 'password')
                    #mail.sendmail('whitelion1080@gmail.com', 'thanh.daotien26@gmail.com', content)
                    #mail.close()
                    self.flag32 = 1

        remove_list(self.boxes3)
        remove_list(self.confidences3)
        remove_list(self.class_ids3)
        frame1 = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(464,293))
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        #print(self.bkg_list1)
        if self.flag30 == 1:
            self.ui.Cam_Draw_3.setPixmap(
                QPixmap.fromImage(self.image_to_QImage(self.drawArea3(frame1, self.points_CAM3, self.ui.Cam_Draw_3),
                                                       self.ui.Cam_Draw_3)))
            self.ui.Cam_3.setPixmap(QPixmap.fromImage(qImg))


    def viewCam4(self):
        ret, image = self.cap4.read()
        self.out4.write(image)
        image1 = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image,(464,293))
        # get image infos
        height, width, channel = image_resized.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image_resized.data, width, height, step, QImage.Format_RGB888)
        self.ui.Cam_Draw_4.setPixmap(QPixmap.fromImage(
           self.image_to_QImage(self.drawArea4(image1, self.points_CAM4, self.ui.Cam_Draw_4), self.ui.Cam_Draw_4)))
        #if self.flag == 0:
        self.ui.Cam_4.setPixmap(QPixmap.fromImage(qImg))
    time_start4 = 0
    time_stop4 = 0
    Flag_CAM4 = 0
    def controlTimer41(self):
        # if timer is stopped
        if not self.timer4.isActive():
            # create video capture
            self.cap4 = cv2.VideoCapture('/home/hades/Documents/DA3/1.avi')
            self.createDir('IP_CAM_4')
            self.Flag_CAM4 = self.cap4.isOpened()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(self.cap4.get(3))
            frame_height = int(self.cap4.get(4))
            self.out4 = cv2.VideoWriter('output.avi', fourcc, 30, (frame_width, frame_height))
            now = datetime.now()
            self.date41 = now.strftime("%d-%m")
            self.time_start4 = now.strftime(" %H:%M:%S-")
            # start timer
            self.timer4.start(20)
        # if timer is started
    def controlTimer42(self):
        # stop timer
        self.timer4.stop()
        self.cap4.release()
        self.out4.release()
        now1 = datetime.now()
        self.time_stop4 = now1.strftime(" %H:%M:%S")
        self.date42 = now1.strftime("%d-%m")
        fileName = str(self.date41) + str(self.time_start4) +"->" + str(self.date42) + str(self.time_stop4) + '.avi'
        self.createDir('IP_CAM_4')
        os.rename('output.avi', fileName)


    def mouseEventCAM4(self, event):
        if self.Flag_CAM4 == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.points_CAM4.append([x, y])
            print("Position clicked is ({}, {})".format(x, y))
    def startDrawAreaCAM4(self):
        self.Flag_CAM4 = 1

    def removeAreaCAM4(self):
        while len(self.points_CAM4):
            self.points_CAM4.pop()

    def drawArea4(self, image, points: list, qlabel: QtWidgets.QLabel):
        image_draw = image.copy()
        image_draw = cv2.resize(image_draw, (qlabel.width() , qlabel.height()))
        # print(len(points))
        if len(points) > 1:
            image_draw = cv2.polylines(image_draw, np.array([points]),1,  (0, 255, 255), 1)
            self.contour4 = np.array([points]).reshape((-1,1,2)).astype(np.int32)
            self.flag41 = 1
            b, g, r = cv2.split(image_draw)
            cv2.fillPoly(b, np.array([points]), (0, 255, 0))
            cv2.fillPoly(r, np.array([points]), (0, 255, 0))
            image_draw = cv2.merge([b, g, r])
        return image_draw
    flag41 = 0
    flag40 = 0
    class_ids4 = []
    confidences4 = []
    boxes4 = []
    flag42 = 0

    def detect_object4(self):
        if self.timer4.isActive():
            self.flag40 = 1
    def show_detect4(self):
        #while (cap.isOpened()):
        ret, frame = self.cap4.read()
        frame = cv2.resize(frame, (464, 293))
        boxes, confidences, class_ids = Detect_person(frame = frame, boxes = self.boxes4, confidences = self.confidences4, class_ids = self.class_ids4)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)
            if self.flag41 == 1:
                dist1 = cv2.pointPolygonTest(self.contour4, (x, y ), False)
                dist2 = cv2.pointPolygonTest(self.contour4, (x, y + h), False)
                dist3 = cv2.pointPolygonTest(self.contour4, (x + w, y), False)
                dist4 = cv2.pointPolygonTest(self.contour4, (x + w, y + h), False)
            #print(dist1,dist2,dist3,dist4)
                if ((dist1==1) or (dist2==1) or (dist3==1) or (dist4==1)) and self.flag42 == 0:
                    print("Canh bao co xam nhap 4")
                    content = 'Canh bao co xam nhap'
                    #mail = smtplib.SMTP('smtp.gmail.com', 587)
                    #mail.ehlo()
                    #mail.starttls()
                    #mail.login('whitelion1080@gmail.com', 'password')
                    #mail.sendmail('whitelion1080@gmail.com', 'thanh.daotien26@gmail.com', content)
                    #mail.close()
                    self.flag42 = 1

        remove_list(self.boxes4)
        remove_list(self.confidences4)
        remove_list(self.class_ids4)        
        frame1 = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(464,293))
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        #print(self.bkg_list1)
        if self.flag40 == 1:
            self.ui.Cam_Draw_4.setPixmap(
                QPixmap.fromImage(self.image_to_QImage(self.drawArea4(frame1, self.points_CAM4, self.ui.Cam_Draw_4),
                                                       self.ui.Cam_Draw_4)))
            self.ui.Cam_4.setPixmap(QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # create and show mainWindow
    mainWindow.show()
    sys.exit(app.exec_())


