import gui

import tkinter as tk
import cv2


def main():
    root = gui.MainWindow()

    cap = cv2.VideoCapture('res/csgo clutch.avi')
    stream = gui.VideoScreen(root, cap)

    root.switch_frame(stream)
    stream.play_source()

    root.mainloop()


if __name__ == "__main__":
    main()