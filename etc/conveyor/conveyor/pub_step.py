import rclpy
from rclpy.node import Node
import serial  # 시리얼 통신을 위한 모듈
from std_msgs.msg import String

class StepPublisher(Node):
    def __init__(self):
        super().__init__('step_publisher')
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200)  # 시리얼 포트 설정
        self.timer = self.create_timer(1.0, self.get_step_input)  # 1초마다 사용자 입력 요청

    def get_step_input(self):
        try:
            step_count = input("Enter step count: ")  # 사용자로부터 스텝 수 입력받기
            if step_count.isdigit():  # 숫자인지 확인
                self.serial_port.write(f"{step_count}\n".encode())  # 시리얼로 전송
                self.get_logger().info(f"Sent step count: {step_count} to Arduino")
            else:
                self.get_logger().warn("Invalid input. Please enter a valid step count (integer).")
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.serial_port.close()  # 시리얼 포트 닫기
        self.get_logger().info("Serial port closed.")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = StepPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.cleanup()
    finally:
        node.destroy_node()

if __name__ == '__main__':
    main()
