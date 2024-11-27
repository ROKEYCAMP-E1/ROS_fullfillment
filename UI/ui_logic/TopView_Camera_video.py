# TopView_Camera_video.py

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class CameraHandler(QThread):
    frame_ready = pyqtSignal(QImage)

    def __init__(self, device_path):
        super().__init__()
        self.device_path = device_path
        self.camera = cv2.VideoCapture(self.device_path)
        self.running = True


    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(qimg)
         

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        if self.camera.isOpened():
            self.camera.release()