import tkinter as tk
from PIL import Image, ImageTk
import cv2


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(SelectionScreen(self))

    def switch_frame(self, frame):
        """Delete visible frame and replace with one of type 'frame_class'."""
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame
        self._frame.pack(fill=tk.BOTH, expand=1)


class SelectionScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self._selection_frame = tk.Frame(self)
        self._path_entry = tk.Entry(self._selection_frame)
        self._browse_button = tk.Button(self._selection_frame, text="...", command=self.browse)

        self._selection_frame.grid(row=0, column=0, sticky="we")
        self._path_entry.grid(row=0, column=0, sticky="we")
        self._browse_button.grid(row=0, column=1)
        self._selection_frame.columnconfigure(0, weight=1)

        self._screen_frame = tk.Frame(self)
        self._screen = tk.Text(self._screen_frame)

        self._screen_frame.grid(row=1, column=0, sticky="nsew")
        self._screen.grid(row=0, column=0, sticky="nsew")
        self._screen_frame.columnconfigure(0, weight=1)
        self._screen_frame.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def browse(self):
        pass


class VideoScreen(tk.Frame):
    def __init__(self, parent, src=None):
        tk.Frame.__init__(self, parent)

        self.image = None
        self.frame = None
        self._canvas = None
        self._src = src

        if src is not None and src.isOpened():
            _, frame = src.read()
            frame_scaled = cv2.pyrDown(frame)
            height, width, channels = frame_scaled.shape

            self._canvas = tk.Canvas(self, width=width, height=height)
            self.display_frame(frame_scaled)
        else:
            self._canvas = tk.Canvas(self, width=960, height=540)

        self._canvas.pack(fill=tk.BOTH, expand=1)

    def display_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.image = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        self._canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.frame = frame

    def play_source(self):
        while self._src.isOpened():
            _, frame = self._src.read()
            self.display_frame(frame)
