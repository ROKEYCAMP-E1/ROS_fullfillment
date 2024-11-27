import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

class CameraHandler:
    def __init__(self, label: QLabel):
        self.camera = cv2.VideoCapture(0)  # 카메라 연결 (0번 기본 카메라)
        self.label = label  # 영상을 표시할 QLabel
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        if not self.camera.isOpened():
            self.camera.open(0)  # 카메라 다시 열기
        self.timer.start(30)  # 30ms마다 프레임 업데이트

    def stop_camera(self):
        self.timer.stop()
        if self.camera.isOpened():
            self.camera.release()  # 카메라 릴리즈

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # OpenCV의 BGR -> RGB 변환
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # NumPy 배열 -> QImage 변환
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # QPixmap으로 QLabel 업데이트
            self.label.setPixmap(QPixmap.fromImage(qimg))

    def close_camera(self):
        """앱 종료 시 카메라 정리"""
        self.stop_camera()
        cv2.destroyAllWindows()
