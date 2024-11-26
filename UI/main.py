import sys
from PyQt5.QtWidgets import QApplication
from login_ui import LoginWindow
from login_ui import MyPageWindow
from workspace import MainApp

class TotalApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.workspace = MainApp()
        self.mypage_window = MyPageWindow()

        # 연결 설정
        self.login_window.login_success.connect(self.open_workspace)
        self.workspace.mypage_load.connect(self.open_mypage)
        self.login_window.show()
        sys.exit(self.app.exec_())

    def open_workspace(self):
        self.workspace.show()
        self.login_window.close()

    def open_mypage(self):
        self.mypage_window.show()
    


if __name__ == "__main__":
    TotalApp()