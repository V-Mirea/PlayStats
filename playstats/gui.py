import tkinter as tk
import PIL.Image, PIL.ImageTk


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None

    def switch_frame(self, frame):
        """Delete visible frame and replace with 'frame'."""
        if self.frame is not None:
            self.frame.destroy()
        self.frame = frame
        self.frame.pack(fill=tk.BOTH, expand=1)

    def start(self, starting_screen=None):
        starting_screen = starting_screen or SelectionScreen(self)
        self.switch_frame(starting_screen)
        self.mainloop()


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
    def __init__(self, parent, stream=None):
        tk.Frame.__init__(self, parent)
        self.stream = stream

        self.canvas = tk.Canvas(self, width=stream.width, height=stream.height)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.delay = 15
        self.update()

    def update(self):
        ret, frame = self.stream.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(self.delay, self.update)


