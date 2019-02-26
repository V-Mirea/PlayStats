import gui
import video
import PyQt5.QtWidgets as qt
import cv2

def main():

    cap = cv2.VideoCapture('res/BF3 C4 Jet Kill.mp4')

    app = qt.QApplication([])
    window = gui.AnalysisWindow()
    screen = gui.VideoScreen(None, cap)
    #screen.show()

    layout = qt.QGridLayout(window.ui.widget)
    layout.addWidget(screen)
    window.ui.widget.setLayout(layout)

    window.show()
    screen._timer.start()
    app.exec_()

if __name__ == "__main__":
    main()