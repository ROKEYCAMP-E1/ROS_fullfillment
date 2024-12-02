#conveyorcontoller.py
import rclpy
from rclpy.node import Node
import serial  # 시리얼 통신을 위한 모듈
from std_msgs.msg import String
from PyQt5.QtCore import QThread, pyqtSignal
from rclpy.executors import SingleThreadedExecutor
from ff_interface.srv import ConveyorRun  # 생성한 서비스 가져오기
from ff_interface.srv import ConveyorConnection  # 생성한 서비스 가져오기

class StepPublisher(Node):
    def __init__(self):
        super().__init__('step_publisher')

        self.serial_port = None
        self.steps = 0

        # 경고 메시지가 전송되었는지 추적하는 변수
        self.warn_message_sent = False

        # 서비스 서버 설정
        self.service = self.create_service(ConveyorRun, 'ConveyorRun', self.handle_conveyor_run)

        # conveyor 연결 상태를 주기적으로 체크하는 타이머 설정
        self.timer = self.create_timer(1.0, self.check_usb_connection)  # 1초마다 연결 체크

        # conveyor 연결 상태 서비스 클라이언트
        self.conveyor_connection_service_client = self.create_client(ConveyorConnection, 'conveyor_connection')

    def check_usb_connection(self):
        """USB 연결 상태를 주기적으로 체크"""
        try:
            if self.serial_port is None or not self.serial_port.is_open:
                if not self.warn_message_sent:  # 한 번만 경고 메시지 전송
                    self.get_logger().warn("USB disconnected.")
                    self.send_warn("[warn] Conveyor disconnected.")
                    self.warn_message_sent = True  # 경고 메시지를 처리했음을 표시

                # USB 연결을 시도
                self.serial_port = self.try_open_serial_port()
                if self.serial_port:
                    self.get_logger().info("USB reconnected successfully.")
                    self.send_warn("Conveyor reconnected successfully.")
                    self.warn_message_sent = False  # USB 연결이 복구되었으므로 경고 메시지 플래그 리셋
            else:
                # 시리얼 포트가 열려 있다면 연결 상태를 유지
                self.get_logger().info("USB connected.")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to communicate with USB: {e}")
            self.send_warn("[warn] Conveyor disconnected.")
            self.warn_message_sent = True  # 예외가 발생했을 때 경고 메시지 처리



    def try_open_serial_port(self):
        """시리얼 포트를 열기 시도"""
        try:
            return serial.Serial('/dev/ttyACM0', 115200)  # 시리얼 포트 설정
        except serial.SerialException:
            # 여기에서 로그를 출력하지 않고 상위 함수에서 처리하도록 None 반환
            return None

    def send_warn(self, message):
        """USB 상태를 서비스로 전송"""
        if not self.conveyor_connection_service_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error("usb_status_service is not available.")
            return

        request = ConveyorConnection.Request()
        request.message = message
        future = self.conveyor_connection_service_client.call_async(request)
        future.add_done_callback(self.handle_service_response)

    def handle_conveyor_run(self, request, response):
        """ConveyorRun 서비스 요청 처리"""
        if request.steps == 0:  # 정지 요청
            self.stop_conveyor()
            response.success = True
            response.message = "Conveyor stopped successfully."
        else:  # 요청된 steps만큼 구동
            self.run_conveyor(request.steps)
            response.success = True
            response.message = f"Conveyor running with {request.steps} steps."

        return response
    
    def handle_service_response(self, future):
        """서비스 요청 응답 처리"""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Conveyor connection status updated successfully.")
            else:
                self.get_logger().error("Failed to update conveyor connection status.")
        except Exception as e:
            self.get_logger().error(f"Error in service response: {e}")


    def run_conveyor(self, steps):
        """Conveyor를 실행"""
        self.steps = steps
        self.send_steps()

    def stop_conveyor(self):
        """Conveyor를 정지"""
        self.steps = 0
        self.send_steps()
    
    def send_steps(self):
        # try:
        #     if self.steps.isdigit():  # 숫자인지 확인
        self.serial_port.write(f"{self.steps}\n".encode())  # 시리얼로 전송
        self.get_logger().info(f"Sent step count: {self.steps} to Arduino")
        #     else:
        #         self.get_logger().warn("Invalid input. Please enter a valid step count (integer).")
        # except KeyboardInterrupt:
        #     self.cleanup()

    def cleanup(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()  # 시리얼 포트 닫기
            self.get_logger().info("Serial port closed.")
        rclpy.shutdown()


class ROS2Thread(QThread):
    ros_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        if not rclpy.ok():  # rclpy가 초기화되지 않았다면 초기화
            rclpy.init()
        self.node = StepPublisher()
        self.executor = SingleThreadedExecutor()  # SingleThreadedExecutor 사용
        self.executor.add_node(self.node)
        self._running = True

    def run(self):
        while self._running:
            self.executor.spin_once(timeout_sec=0.1)

    def run_conveyor(self, steps):
        """Conveyor 실행 요청"""
        self.node.run_conveyor(steps)

    def stop_conveyor(self):
        """Conveyor 정지 요청"""
        self.node.stop_conveyor()

    def stop(self):
        self._running = False
        self.executor.shutdown()
        self.node.cleanup()
        self.quit()

def main(args=None):
    rclpy.init(args=args)
    node = StepPublisher()

    try:
        rclpy.spin(node)  # ROS2 이벤트 루프
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped by user.")
    finally:
        node.cleanup()
        rclpy.shutdown()


if __name__ == '__main__':
    main()