import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # /image_raw 토픽의 메시지 타입

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')  # 노드 이름 설정
        # /image_raw 토픽을 구독
        self.subscription = self.create_subscription(
            Image,  # 메시지 타입
            '/image_raw',  # 토픽 이름
            self.listener_callback,  # 콜백 함수
            10  # QoS 설정 (큐 사이즈)
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('good')  # "good" 메시지 출력

def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber()
    try:
        rclpy.spin(node)  # 노드 실행
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()  # 노드 삭제
        rclpy.shutdown()  # rclpy 종료

if __name__ == '__main__':
    main()
