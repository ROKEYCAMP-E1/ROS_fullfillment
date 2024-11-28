#main
from PyQt5.QtWidgets import QApplication
from user_management import LoginWindow, MyPageWindow
from workspace import WorkspaceWindow, ControlWindow
from conveyorcontroller import ROS2Thread
import rclpy

class MainApp:
    def __init__(self):
        self.app = QApplication([])

        self.ros_thread = ROS2Thread()
        # 화면 초기화
        self.login_window = LoginWindow()
        self.workspace = WorkspaceWindow()
        self.mypage_window = MyPageWindow()
        self.control_window = ControlWindow()

        # 화면 간 연결 설정
        self.login_window.login_success.connect(self.open_workspace)
        self.workspace.mypage_load.connect(self.open_mypage)
        self.workspace.control_load.connect(self.open_control)
        
        self.control_window.run_con_signal.connect(self.ros_thread.run_conveyor)
        self.control_window.stop_con_signal.connect(self.ros_thread.stop_conveyor)

        if not rclpy.ok():  # 초기화되지 않은 경우만 실행
            rclpy.init()
        self.ros_thread = ROS2Thread()
        self.ros_thread.start()
        self.login_window.show()
        self.app.aboutToQuit.connect(self.close_application) 
        self.app.exec_()

    def open_workspace(self):
        self.workspace.show()
        self.login_window.close()

    def open_mypage(self):
        self.mypage_window.show()

    def open_control(self):
        self.control_window.show()

    def close_application(self):
        """애플리케이션 종료 처리"""
        self.ros_thread.stop()
        self.app.quit()

def main():
    MainApp()

if __name__ == "__main__":
    main()
