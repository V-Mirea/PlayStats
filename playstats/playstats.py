import gui
import video
from PyQt5 import QtWidgets

def main():

    app = QtWidgets.QApplication([])
    screen = gui.VideoScreen()
    screen.show()
    app.exec_()

if __name__ == "__main__":
    main()