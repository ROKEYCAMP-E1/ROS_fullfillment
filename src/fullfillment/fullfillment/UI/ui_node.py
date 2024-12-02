# ui_node.py

import rclpy
from rclpy.node import Node

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi  # .ui 파일 로드를 위한 모듈
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage  # QPixmap 임포트 추가
from datetime import datetime
from fullfillment.UI.ui_utils.send_email import send_email
from fullfillment.UI.ui_utils.auth import load_user_data
from fullfillment.UI.ui_logic.user_management import LoginWindow, MyPageWindow
import sys
import os
from sensor_msgs.msg import Image # ArUCo 영상 토픽 구독을 위한 임포트
from cv_bridge import CvBridge # ArUCo 영상 토픽 구독을 위한 임포트
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from rclpy.action import ActionClient

from ff_interface.srv import ConveyorRun  # 서비스 임포트
from ff_interface.srv import ConveyorConnection  # 생성한 서비스 가져오기
from ff_interface.action import Job
from ff_interface.srv import RobotControl

# 프로젝트의 루트 디렉토리를 Python의 모듈 검색 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 이제 Fullfillment 패키지에서 import 가능
from fullfillment.Conveyor.conveyorcontroller import ROS2Thread,StepPublisher


class WorkspaceWindow(QMainWindow):
    mypage_load = pyqtSignal() # 마이페이지 화면전환 로직을 위한 시그널 송출
    control_load = pyqtSignal() # 마이페이지 화면전환 로직을 위한 시그널 송출

    def __init__(self):
        super().__init__()
        loadUi("src/fullfillment/fullfillment/UI/ui/workspace.ui", self)
    
        self.control_window = ControlWindow()
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
        self.warnningbox.setText("")
        self.statusbox.setText("")  # 텍스트 초기화
        self.timerbox.setText("경과 시간:  초")

        self.mypage_button.clicked.connect(self.emit_mypage_load) 
        self.control.clicked.connect(self.emit_control_load)

        # Job Action 클라이언트 생성
        self.job_action_client = None
        self.setup_action_client()


    def setup_action_client(self):
        """Job Action 클라이언트를 설정"""
        self.node = rclpy.create_node('job_action_client')
        self.job_action_client = ActionClient(self.node, Job, '/job')

    def update_selected_job(self):
        """현재 ComboBox에서 선택된 작업을 업데이트"""
        current_job = self.jobbox.currentText()
        self.current_job = current_job  # 선택된 작업 저장

    def send_job_action(self, job):
        """Job Action Goal을 서버에 전송"""
        if not self.job_action_client.wait_for_server(timeout_sec=1.0):
            self.warnningbox.append("[ERROR] Action server '/job' is not available!")
            return

        goal_msg = Job.Goal()
        goal_msg.job = job  # 작업 이름 설정

        # 비동기 방식으로 Goal 전송
        self.future = self.job_action_client.send_goal_async(goal_msg, self.handle_feedback)
        self.future.add_done_callback(self.handle_job_response)


    def handle_feedback(self, feedback_msg):
        """Job Action의 피드백 처리"""
        feedback = feedback_msg.feedback
        self.statusbox.append(f"[INFO] Job in progress: {feedback.status}")


    def handle_job_response(self, future):
        """Job Action의 결과 처리"""
        try:
            result = future.result().result
            self.timer_obj.stop()  # 타이머 정지
            if result.job_completed:
                self.statusbox.append(f"[INFO] Job '{result.details}' completed successfully!")
            else:
                self.warnningbox.append(f"[ERROR] Job failed: {result.details}")
        except Exception as e:
            self.warnningbox.append(f"[ERROR] Action call failed: {str(e)}")
        finally:
            # 최종 경과 시간 표시
            self.timerbox.setText(f"총 경과 시간: {self.elapsed_time} 초")

    def emit_mypage_load(self):
        self.mypage_load.emit()

    def emit_control_load(self):
        self.control_load.emit()



    def add_job_to_list(self):
        """선택된 작업을 리스트에 누적"""
        if self.current_job:
            self.selected_list.append(self.current_job)  # 리스트에 추가
            self.statusbox.append(self.current_job)  # 텍스트 브라우저에 추가

            # Action 시작 시간 초기화
            self.elapsed_time = 0
            self.timer_obj.start(1000)  # 1초마다 update_timer 실행

            # Job Action 호출
            self.send_job_action(self.current_job)

    def update_timer(self):
            """타이머를 1초 단위로 업데이트"""
            self.elapsed_time += 1  # 1초 증가
            self.timerbox.setText(f"경과 시간: {self.elapsed_time} 초")  # textBrowser3에 경과 시간 표시

    def update_text_browser(self, text):
        """ControlWindow에서 전달받은 텍스트를 textBrowser에 출력"""
        self.warnningbox.append(text)  # 텍스트 브라우저에 텍스트 추가


class ControlWindow(QMainWindow):
    send_text = pyqtSignal(str)
    workspace_load = pyqtSignal()
    _instance = None # Singleton 인스턴스 저장
    _initialized = False  # 초기화 상태 플래그
    # ROS2Thread와 연결할 신호 정의
    run_con_signal = pyqtSignal(int)
    stop_con_signal = pyqtSignal()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ControlWindow, cls).__new__(cls, *args, **kwargs)
    
        return cls._instance


    def __init__(self, parent=None):
        if not self._initialized:
            super().__init__(parent)
            loadUi("src/fullfillment/fullfillment/UI/ui/control_window.ui", self)

            # 버튼 연결
            self.play.clicked.connect(self.play_robot)
            self.pause.clicked.connect(self.pause_robot)
            self.stop.clicked.connect(self.stop_robot)
            self.resume.clicked.connect(self.resume_robot)
            self.run_con.clicked.connect(self.run_conveyor) 
            self.stop_con.clicked.connect(self.stop_conveyor) 
            self.gohome.clicked.connect(self.emit_workspace_load)

            self._initialized = True  # 초기화 완료 플래그 설정
        
    def emit_workspace_load(self):
        self.workspace_load.emit()

    def play_robot(self):
        text_to_send = "[Control] Robot play"
        self.send_text.emit(text_to_send)  # 기존 동작 유지
        self._send_robot_command("forward", text_to_send)

    def pause_robot(self):
        text_to_send = "[Control] Robot pause"
        self.send_text.emit(text_to_send)  # 기존 동작 유지
        self._send_robot_command("stop", text_to_send)

    def stop_robot(self):
        text_to_send = "[Control] Robot stop"
        self.send_text.emit(text_to_send)  # 기존 동작 유지
        self._send_robot_command("stop", text_to_send)

    def resume_robot(self):
        text_to_send = "[Control] Robot resume"
        self.send_text.emit(text_to_send)  # 기존 동작 유지
        self._send_robot_command("forward", text_to_send)


    def _send_robot_command(self, command, log_message):
        """
        Send a command to the /RobotControl service.
        """
        if not self.robot_control_client.wait_for_service(timeout_sec=1.0):
            self.send_text.emit("[Error] /RobotControl service is not available.")
            return

        # 서비스 요청 생성 및 전송
        request = RobotControl.Request()
        request.command = command

        future = self.robot_control_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)

        # 서비스 응답 확인
        response = future.result()
        if response.success:
            self.send_text.emit(log_message)
        else:
            self.send_text.emit(f"[Error] {response.message}")

    def run_conveyor(self):
        self.run_con_signal.emit(1000000)
        text_to_send = "[Control] conveyor run"
        self.send_text.emit(text_to_send) 
        
    def stop_conveyor(self):
        self.stop_con_signal.emit()
        text_to_send = "[Control] conveyor stop"
        self.send_text.emit(text_to_send) 


class UINode(Node):
    def __init__(self):
        super().__init__('ui_node')

        self.app = QApplication([])

        # USB 상태 서비스 서버 생성
        self.usb_error_service_server = self.create_service(ConveyorConnection, 'conveyor_connection', self.handle_conveyor_connnection)


        # ROS2 서비스 클라이언트 생성
        self.conveyor_service_client = self.create_client(ConveyorRun, 'conveyor_control')

        # 화면 초기화
        self.login_window = LoginWindow()
        self.workspace = WorkspaceWindow()
        self.mypage_window = MyPageWindow()
        self.control_window = ControlWindow()

        # 화면 간 연결 설정
        self.login_window.login_success.connect(self.start_conveyor_and_open_workspace)
        self.workspace.mypage_load.connect(self.open_mypage)
        self.workspace.control_load.connect(self.open_control)
        self.control_window.workspace_load.connect(self.back_to_workspace)

        # ArUCo 영상 토픽 구독
        self.bridge = CvBridge()
        qos_profile = QoSProfile(depth=10)
        self.create_subscription(
            Image, 
            'aruco_image', 
            self.image_callback, 
            qos_profile
        )

        # QApplication 종료 이벤트 연결
        self.app.aboutToQuit.connect(self.stop_conveyor_on_exit)

        self.login_window.show()



    def handle_conveyor_connnection(self, request, response):
        """USB 상태 서비스 요청 처리"""
        message = request.message

        if '[warn]' in message.lower():  # 경고 메시지가 포함된 경우
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"{timestamp}: {message}"
            self.workspace.warnningbox.append(full_message)  # 워닝 박스에 추가
            self.send_warnning_email(full_message)  # 이메일 전송

        response.success = True
        response.response = "Conveyor Connection processed successfully."
        return response

    def send_warnning_email(self, message):
        user_data = load_user_data()
        receiver_email = user_data["email"]
        subject = "Workspace Report"

        if message:
            send_email(receiver_email, subject, message)
        else:
            print("메시지가 비어 있습니다.")

    def call_conveyor_service(self, steps):
        """ConveyorRun 서비스 호출"""
        from ff_interface.srv import ConveyorRun  # 서비스 메시지 임포트
        client = self.create_client(ConveyorRun, 'ConveyorRun')

        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for ConveyorRun service...")

        request = ConveyorRun.Request()
        request.steps = steps

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f"ConveyorRun service response: {future.result().message}")
        else:
            self.get_logger().error("ConveyorRun service call failed.")


    def start_conveyor_and_open_workspace(self):
        """컨베이어 시작 및 워크스페이스 창 열기"""
        self.call_conveyor_service(steps=100000)  # 예: 100,000 스텝
        self.workspace.show()
        self.login_window.close()

    def stop_conveyor_on_exit(self):
        """애플리케이션 종료 시 컨베이어 정지"""
        self.call_conveyor_service(steps=0)  # 정지

    def open_mypage(self):
        self.mypage_window.show()

    def open_control(self):
        self.control_window.show()
        self.workspace.close()

    def back_to_workspace(self):
        self.workspace.show()
        self.control_window.close()

    def run(self):
        # QTimer로 ROS2 콜백을 주기적으로 호출
        timer = QTimer()
        timer.timeout.connect(lambda: rclpy.spin_once(self, timeout_sec=0.01))
        timer.start(10)  # 10ms 간격으로 ROS2 이벤트 처리

        self.app.exec_()
        self.ros2_thread.stop()

    def image_callback(self, msg): # ArUCo image 토픽 콜백
        try:
            # sensor_msgs/Image -> OpenCV 이미지로 변환
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # OpenCV 이미지를 QPixmap으로 변환
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            qt_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qt_image)

            # WorkspaceWindow의 worldcamera에 이미지 표시
            self.workspace.worldcamera.setPixmap(pixmap)
            self.control_window.worldcamera.setPixmap(pixmap)

        except Exception as e:
            self.get_logger().error(f"Failed to process image: {e}")


def main(args=None):
    rclpy.init(args=args)
    ui_node = UINode()

    try:
        ui_node.run()
    except KeyboardInterrupt:
        ui_node.get_logger().info("Shutting down UI Node...")
    finally:
        rclpy.shutdown()



if __name__ == "__main__":
    main()