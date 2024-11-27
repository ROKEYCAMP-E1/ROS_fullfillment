import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # /image_raw 토픽 메시지 타입
from cv_bridge import CvBridge  # ROS 이미지 메시지를 OpenCV 이미지로 변환
import cv2  # OpenCV 라이브러리
from ultralytics import YOLO  # YOLOv8 라이브러리

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
        self.model = YOLO('yolov8n.pt')  # YOLOv8 모델 로드 (사전 훈련된 모델 사용)

    def listener_callback(self, msg):
        # ROS Image 메시지를 OpenCV 이미지로 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # YOLOv8 모델로 객체 탐지 수행
        results = self.model(cv_image)

        # 탐지된 이미지가 있을 경우
        if len(results[0].boxes) > 0:
            # 바운딩 박스를 그린 이미지를 얻음
            frame_with_boxes = results[0].plot()

            # 탐지된 이미지를 파일로 덮어쓰기
            filename = "detected_image.jpg"
            cv2.imwrite(filename, frame_with_boxes)
            self.get_logger().info(f"Detected image saved as {filename}")

        # 로그 출력
        self.get_logger().info('Image received and processed.')

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
