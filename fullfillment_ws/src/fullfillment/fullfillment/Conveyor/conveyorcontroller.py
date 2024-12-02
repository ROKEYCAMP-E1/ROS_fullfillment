#conveyorcontoller.py
import rclpy
from rclpy.node import Node
import serial  # 시리얼 통신을 위한 모듈
from std_msgs.msg import String
from PyQt5.QtCore import QThread, pyqtSignal
from rclpy.executors import SingleThreadedExecutor
from ff_interface.srv import ConveyorRun  # 생성한 서비스 가져오기

class StepPublisher(Node):
    def __init__(self):
        super().__init__('step_publisher')
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200)  # 시리얼 포트 설정
        self.steps=0

        # 서비스 서버 설정
        self.service = self.create_service(ConveyorRun, 'ConveyorRun', self.handle_conveyor_run)

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