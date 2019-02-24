import gui
import video

import tkinter as tk
import cv2


def main():
    cap = cv2.VideoCapture('res/BF4 HD test.avi')
    stream = video.VideoStream(cap)
    root = gui.MainWindow()
    screen = gui.VideoScreen(root, stream)
    root.start(screen)

if __name__ == "__main__":
    main()