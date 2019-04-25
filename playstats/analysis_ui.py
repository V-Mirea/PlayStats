# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analysis.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class AnalysisWindow_ui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 582)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtFileName = QtWidgets.QLineEdit(self.centralwidget)
        self.txtFileName.setObjectName("txtFileName")
        self.horizontalLayout_2.addWidget(self.txtFileName)
        self.buttonBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.horizontalLayout_2.addWidget(self.buttonBrowse)
        self.buttonStart = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStart.setObjectName("buttonStart")
        self.horizontalLayout_2.addWidget(self.buttonStart)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboGame = QtWidgets.QComboBox(self.centralwidget)
        self.comboGame.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.comboGame.setObjectName("comboGame")
        self.comboGame.addItem("")
        self.comboGame.addItem("")
        self.comboGame.addItem("")
        self.horizontalLayout_3.addWidget(self.comboGame)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.buttonStats = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStats.setEnabled(False)
        self.buttonStats.setObjectName("buttonStats")
        self.verticalLayout.addWidget(self.buttonStats)
        self.verticalLayout.setStretch(2, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonBrowse.setText(_translate("MainWindow", "..."))
        self.buttonStart.setText(_translate("MainWindow", "Analyze"))
        self.label.setText(_translate("MainWindow", "Game:"))
        self.comboGame.setItemText(0, _translate("MainWindow", "Counter Strike: Global Offensive"))
        self.comboGame.setItemText(1, _translate("MainWindow", "Overwatch"))
        self.comboGame.setItemText(2, _translate("MainWindow", "Fortnite"))
        self.buttonStats.setText(_translate("MainWindow", "See Results"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

