import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(SelectionScreen)

    def switch_frame(self, frame_class):
        """Delete visible frame and replace with one of type 'frame_class'."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
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
