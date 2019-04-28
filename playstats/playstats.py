import gui
import PyQt5.QtWidgets as qt
import cv2

def main():
    app = qt.QApplication([])
    window = gui.AnalysisWindow()
    window.showMaximized()
    app.exec_()

if __name__ == "__main__":
    main()