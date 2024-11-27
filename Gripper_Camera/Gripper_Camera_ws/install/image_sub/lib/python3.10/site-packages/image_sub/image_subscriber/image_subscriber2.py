import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # /image_raw 토픽 메시지 타입
from cv_bridge import CvBridge  # ROS 이미지 메시지를 OpenCV 이미지로 변환
import cv2  # OpenCV 라이브러리

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')  # 노드 이름 설정
        self.subscription = self.create_subscription(
            Image,  # 메시지 타입
            '/image_raw',  # 토픽 이름
            self.listener_callback,  # 콜백 함수
            10  # QoS 설정 (큐 사이즈)
        )
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()  # CvBridge 인스턴스 생성

    def listener_callback(self, msg):
        # ROS Image 메시지를 OpenCV 이미지로 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # OpenCV를 사용하여 이미지 출력
        cv2.imshow("Received Image", cv_image)
        cv2.waitKey(1)  # 짧은 대기 시간을 줘야 이미지가 갱신됨

        # 로그 출력
        self.get_logger().info('Image received and displayed.')

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
        cv2.destroyAllWindows()  # OpenCV 창 닫기

if __name__ == '__main__':
    main()
