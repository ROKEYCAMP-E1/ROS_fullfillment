# main.py

from PyQt5.QtWidgets import QApplication
from ui_logic.user_management import LoginWindow, MyPageWindow
from ui_logic.workspace import WorkspaceWindow, ControlWindow
from ui_logic.TopView_Camera_video import CameraHandler

class MainApp:
    def __init__(self):
        self.app = QApplication([])

        # 공용 CameraHandler 객체 생성
        self.camera_handler = CameraHandler(device_path="/dev/video3")
        self.camera_handler.start()


        # 화면 초기화
        self.login_window = LoginWindow()
        self.workspace = WorkspaceWindow(self.camera_handler)
        self.mypage_window = MyPageWindow()
        self.control_window = ControlWindow(self.camera_handler)

        # 화면 간 연결 설정
        self.login_window.login_success.connect(self.open_workspace)
        self.workspace.mypage_load.connect(self.open_mypage)
        self.workspace.control_load.connect(self.open_control)
        self.control_window.workspace_load.connect(self.back_to_workspace)

        self.login_window.show()
        self.app.exec_()

    def open_workspace(self):
        self.workspace.show()
        self.login_window.close()

    def open_mypage(self):
        self.mypage_window.show()

    def open_control(self):
        self.control_window.show()
        self.workspace.close()

    def back_to_workspace(self):
        self.workspace.show()
        self.control_window.close()


if __name__ == "__main__":
    MainApp()
