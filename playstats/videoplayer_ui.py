# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videoplayer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class VideoPlayer_ui(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(581, 441)
        self.verticalLayout = QtWidgets.QVBoxLayout(VideoPlayer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBack = QtWidgets.QPushButton(VideoPlayer)
        self.buttonBack.setObjectName("buttonBack")
        self.horizontalLayout.addWidget(self.buttonBack)
        self.buttonPause = QtWidgets.QPushButton(VideoPlayer)
        self.buttonPause.setObjectName("buttonPause")
        self.horizontalLayout.addWidget(self.buttonPause)
        self.checkShowAnalysis = QtWidgets.QCheckBox(VideoPlayer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkShowAnalysis.sizePolicy().hasHeightForWidth())
        self.checkShowAnalysis.setSizePolicy(sizePolicy)
        self.checkShowAnalysis.setChecked(True)
        self.checkShowAnalysis.setObjectName("checkShowAnalysis")
        self.horizontalLayout.addWidget(self.checkShowAnalysis)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(VideoPlayer)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "Video"))
        self.buttonBack.setText(_translate("VideoPlayer", "<<"))
        self.buttonPause.setText(_translate("VideoPlayer", "l> / ||"))
        self.checkShowAnalysis.setText(_translate("VideoPlayer", "Show Analysis"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VideoPlayer = QtWidgets.QWidget()
    ui = Ui_VideoPlayer()
    ui.setupUi(VideoPlayer)
    VideoPlayer.show()
    sys.exit(app.exec_())

