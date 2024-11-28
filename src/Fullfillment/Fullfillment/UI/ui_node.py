# ui_main.py

import rclpy
from rclpy.node import Node

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi  # .ui 파일 로드를 위한 모듈
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap  # QPixmap 임포트 추가
from datetime import datetime
from utils.send_email import send_email
from utils.auth import load_user_data
from ui_logic.TopView_Camera_video import CameraHandler
from ui_logic.user_management import LoginWindow, MyPageWindow
import sys
import os

# 프로젝트의 루트 디렉토리를 Python의 모듈 검색 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 이제 Fullfillment 패키지에서 import 가능
from Fullfillment.Conveyor.conveyorcontroller import ROS2Thread,StepPublisher


class WorkspaceWindow(QMainWindow):
    mypage_load = pyqtSignal() # 마이페이지 화면전환 로직을 위한 시그널 송출
    control_load = pyqtSignal() # 마이페이지 화면전환 로직을 위한 시그널 송출

    def __init__(self, camera_handler):
        super().__init__()
        loadUi("src/Fullfillment/Fullfillment/UI/ui/workspace.ui", self)
    
        self.control_window = ControlWindow(camera_handler)
        self.control_window.send_text.connect(self.update_text_browser)

        self.ros_thread = ROS2Thread()
        self.ros_thread.start()

        self.control_window.run_con_signal.connect(self.ros_thread.run_conveyor)
        self.control_window.stop_con_signal.connect(self.ros_thread.stop_conveyor)


        self.jobbox.activated.connect(self.update_selected_job)  
        self.selectjob.clicked.connect(self.add_job_to_list)

        self.timer_obj = QTimer(self)
        self.timer_obj.timeout.connect(self.update_timer)  # 매초 호출할 함수 연결
        self.elapsed_time = 0  

        self.selected_list = []  # 선택된 작업 저장
        self.textBrowser.setText("")
        self.textBrowser_2.setText("")  # 텍스트 초기화
        self.textBrowser_3.setText("경과 시간:  초")

        self.mypage_button.clicked.connect(self.emit_mypage_load) 
        self.control.clicked.connect(self.emit_control_load)

        # TopView Camera 연결
        self.camera_handler = camera_handler
        self.camera_handler.frame_ready.connect(self.update_frame)  # 프레임 연결

        self.current_job = None

    def update_frame(self, frame):
        self.worldcamera.setPixmap(QPixmap.fromImage(frame))


    def emit_mypage_load(self):
        self.mypage_load.emit()

    def emit_control_load(self):
        self.control_load.emit()

    def update_selected_job(self):
        """현재 ComboBox에서 선택된 작업을 업데이트"""
        current_job = self.jobbox.currentText()
        self.current_job = current_job  # 선택된 작업 저장


    def add_job_to_list(self):
        """선택된 작업을 리스트에 누적"""
        if self.current_job:
            self.selected_list.append(self.current_job)  # 리스트에 추가
            self.textBrowser_2.append(self.current_job)  # 텍스트 브라우저에 추가

            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 작업 시작 시간 저장

            # 타이머 초기화 및 시작
            self.elapsed_time = 0
            self.timer_obj.start(1000)  # 1초마다 update_timer 실행

    def update_timer(self):
            """타이머를 1초 단위로 업데이트"""
            self.elapsed_time += 1  # 1초 증가
            self.textBrowser_3.setText(f"경과 시간: {self.elapsed_time} 초")  # textBrowser3에 경과 시간 표시

    def update_text_browser(self, text):
        """ControlWindow에서 전달받은 텍스트를 textBrowser에 출력"""
        self.textBrowser.append(text)  # 텍스트 브라우저에 텍스트 추가


class ControlWindow(QMainWindow):
    send_text = pyqtSignal(str)
    workspace_load = pyqtSignal()
    _instance = None # Singleton 인스턴스 저장
    _initialized = False  # 초기화 상태 플래그
    # ROS2Thread와 연결할 신호 정의
    run_con_signal = pyqtSignal(int)
    stop_con_signal = pyqtSignal()

    def __new__(cls, camera_handler=None, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ControlWindow, cls).__new__(cls, *args, **kwargs)
    
        return cls._instance


    def __init__(self, camera_handler ,parent=None):
        if not self._initialized:
            super().__init__(parent)
            loadUi("src/Fullfillment/Fullfillment/UI/ui/control_window.ui", self)

            # 버튼 연결
            self.play.clicked.connect(self.play_robot)
            self.pause.clicked.connect(self.pause_robot)
            self.stop.clicked.connect(self.stop_robot)
            self.resume.clicked.connect(self.resume_robot)
            self.run_con.clicked.connect(self.run_conveyor)
            self.stop_con.clicked.connect(self.stop_conveyor)
            self.gohome.clicked.connect(self.emit_workspace_load)

            # 카메라 연결
            self.camera_handler = camera_handler
            self.camera_handler.frame_ready.connect(self.update_frame)  # 프레임 연결

            self._initialized = True  # 초기화 완료 플래그 설정

    def update_frame(self, frame):
        self.worldcamera.setPixmap(QPixmap.fromImage(frame))
        
    def emit_workspace_load(self):
        self.workspace_load.emit()

    def play_robot(self):
        text_to_send = "Robot play"
        self.send_text.emit(text_to_send) 
    def pause_robot(self):
        text_to_send = "Robot pause"
        self.send_text.emit(text_to_send) 
    def stop_robot(self):
        text_to_send = "Robot stop"
        self.send_text.emit(text_to_send) 
    def resume_robot(self):
        text_to_send = "Robot resume"
        self.send_text.emit(text_to_send) 

    def run_conveyor(self):
        self.run_con_signal.emit(100000)
        text_to_send = "conveyor run"
        self.send_text.emit(text_to_send) 
        
    def stop_conveyor(self):
        self.stop_con_signal.emit()
        text_to_send = "conveyor stop"
        self.send_text.emit(text_to_send) 


    def send_workspace_email(self, message):
        user_data = load_user_data()
        receiver_email = user_data["email"]
        subject = "Workspace Report"

        if message:
            send_email(receiver_email, subject, message)
        else:
            print("메시지가 비어 있습니다.")

class UINode(Node):
    def __init__(self):
        super().__init__('ui_node')

        self.app = QApplication([])

        # 공용 CameraHandler 객체 생성
        self.camera_handler = CameraHandler(device_path="/dev/video2")
        self.camera_handler.start()

        # ROS2Thread 초기화
        self.ros2_thread = ROS2Thread()
        self.ros2_thread.start()

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

    def run(self):
        self.app.exec_()
        self.ros2_thread.stop()


def main(args=None):
    rclpy.init(args=args)
    ui_node = UINode()

    try:
        ui_node.run()
    except KeyboardInterrupt:
        ui_node.get_logger().info("Shutting down UI Node...")
    finally:
        ui_node.camera_handler.stop()
        rclpy.shutdown()



if __name__ == "__main__":
    main()