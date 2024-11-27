from PyQt5.QtWidgets import QApplication
from ui_logic.user_management import LoginWindow, MyPageWindow
from ui_logic.workspace import WorkspaceWindow, ControlWindow

class MainApp:
    def __init__(self):
        self.app = QApplication([])

        # 화면 초기화
        self.login_window = LoginWindow()
        self.workspace = WorkspaceWindow()
        self.mypage_window = MyPageWindow()
        self.control_window = ControlWindow()

        # 화면 간 연결 설정
        self.login_window.login_success.connect(self.open_workspace)
        self.workspace.mypage_load.connect(self.open_mypage)
        self.workspace.control_load.connect(self.open_control)

        self.login_window.show()
        self.app.exec_()

    def open_workspace(self):
        self.workspace.show()
        self.login_window.close()

    def open_mypage(self):
        self.mypage_window.show()

    def open_control(self):
        self.control_window.show()


if __name__ == "__main__":
    MainApp()
