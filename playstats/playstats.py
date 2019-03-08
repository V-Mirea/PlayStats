import gui
import PyQt5.QtWidgets as qt
import cv2

def main():

    cap = cv2.VideoCapture('res/BF3 C4 Jet Kill.mp4')

    app = qt.QApplication([])
    window = gui.AnalysisWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()