import cv2


# Takes a cv.VideoCapture
class VideoStream(cv2.VideoCapture):
    def __init__(self, src=None):
        self.src = src

        if src is not None and src.isOpened():
            self.width = src.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = src.get(cv2.CAP_PROP_FRAME_HEIGHT)
        else:
            self.width = 960
            self.height = 540

    def __del__(self):
        if self.src is not None and self.src.isOpened():
            self.src.release()

    def get_frame(self):
        if self.src.isOpened():
            ret, frame = self.src.read()
            return (True, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) if ret else (False, None)
        else:
            return False, None
