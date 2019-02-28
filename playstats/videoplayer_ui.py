# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playstats/videoplayer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class VideoPlayer_ui(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(581, 441)
        self.gridLayout = QtWidgets.QGridLayout(VideoPlayer)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonForward = QtWidgets.QPushButton(VideoPlayer)
        self.buttonForward.setObjectName("buttonForward")
        self.gridLayout.addWidget(self.buttonForward, 1, 2, 1, 1)
        self.buttonPause = QtWidgets.QPushButton(VideoPlayer)
        self.buttonPause.setObjectName("buttonPause")
        self.gridLayout.addWidget(self.buttonPause, 1, 1, 1, 1)
        self.buttonBack = QtWidgets.QPushButton(VideoPlayer)
        self.buttonBack.setObjectName("buttonBack")
        self.gridLayout.addWidget(self.buttonBack, 1, 0, 1, 1)
        self.videoFrame = QtWidgets.QFrame(VideoPlayer)
        self.videoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoFrame.setObjectName("videoFrame")
        self.gridLayout.addWidget(self.videoFrame, 0, 0, 1, 3)

        self.retranslateUi(VideoPlayer)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "Video"))
        self.buttonForward.setText(_translate("VideoPlayer", ">>"))
        self.buttonPause.setText(_translate("VideoPlayer", "l> / ||"))
        self.buttonBack.setText(_translate("VideoPlayer", "<<"))

