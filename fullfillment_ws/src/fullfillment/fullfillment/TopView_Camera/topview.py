import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray
from ff_interface.msg import ArucoDetections
from sensor_msgs.msg import Image
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge
import json
import numpy as np


class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        self.image_publisher = self.create_publisher(Image, 'aruco_image', 10)
        self.detections_publisher = self.create_publisher(ArucoDetections, 'aruco_detections', 10)
        self.bridge = CvBridge()

        # 비디오 캡처 초기화
        self.cap = cv2.VideoCapture('/dev/video2')

        # MJPG 포맷으로 설정
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        # 해상도 설정: 1280x720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # 카메라 연결 확인 로깅
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open video capture device.")
            raise RuntimeError("Could not open video capture device.")

        # ArUCo 설정
        self.marker_length = 0.108  # 마커 크기 (미터 단위)
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        self.parameters = aruco.DetectorParameters_create()

        # 기준 마커 ID
        self.origin_id = 54
        self.c_id = 53

        # JSON 파일에서 캘리브레이션 데이터 읽기
        calibration_file = 'src/fullfillment/fullfillment/TopView_Camera/calibration.json'
        try:
            with open(calibration_file, 'r') as file:
                calibration_data = json.load(file)
                self.mtx = np.array(calibration_data['mtx'])
                self.dist = np.array(calibration_data.get('dist', [0, 0, 0, 0, 0]))
        except Exception as e:
            self.get_logger().error(f"Failed to load calibration data: {e}")
            raise

        # Timer로 detect_markers 주기 호출
        self.timer = self.create_timer(0.1, self.detect_markers)

    def calculate_angle_between_vectors(self, vec1, vec2):
        """두 벡터 간 각도 계산"""
        unit_vec1 = vec1 / np.linalg.norm(vec1)
        unit_vec2 = vec2 / np.linalg.norm(vec2)
        dot_product = np.dot(unit_vec1, unit_vec2)
        angle = np.arccos(np.clip(dot_product, -1.0, 1.0))  # -1 ~ 1 사이로 클리핑
        return np.degrees(angle)

    def extract_x_axis_vector(self, rvec):
        """회전 벡터로부터 X축 방향 벡터 추출"""
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        return rotation_matrix[:, 0]  # X축 벡터 (회전 행렬의 첫 번째 열)

    def display_angle(self, frame, angle):
        """화면 우측 하단에 각도 표시"""
        height, width = frame.shape[:2]
        text = f"Angle Between X-Axes: {angle:.2f} deg"
        cv2.putText(frame, text, (width - 400, height - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2, cv2.LINE_AA)

    def detect_markers(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Failed to capture frame.")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ArUCo 마커 탐지
        corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        if ids is not None:
            # 자세 추정
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.marker_length, self.mtx, self.dist)

            x_axis_54 = None
            x_axis_53 = None
            marker_ids = []
            poses = PoseArray()

            for i in range(len(ids)):
                marker_ids.append(int(ids[i][0]))

                pose = Pose()
                pose.position.x = tvecs[i][0][0]
                pose.position.y = tvecs[i][0][1]
                pose.position.z = tvecs[i][0][2]
                pose.orientation.x = rvecs[i][0][0]
                pose.orientation.y = rvecs[i][0][1]
                pose.orientation.z = rvecs[i][0][2]
                pose.orientation.w = 1.0
                poses.poses.append(pose)

                if ids[i][0] == self.origin_id:
                    x_axis_54 = self.extract_x_axis_vector(rvecs[i])
                elif ids[i][0] == self.c_id:
                    x_axis_53 = self.extract_x_axis_vector(rvecs[i])

                aruco.drawDetectedMarkers(frame, corners, ids)
                aruco.drawAxis(frame, self.mtx, self.dist, rvecs[i], tvecs[i], 0.1)

            if x_axis_54 is not None and x_axis_53 is not None:
                angle_between = self.calculate_angle_between_vectors(x_axis_54, x_axis_53)
                self.display_angle(frame, angle_between)

            detection_msg = ArucoDetections()
            detection_msg.marker_ids = marker_ids
            detection_msg.poses = poses
            self.detections_publisher.publish(detection_msg)

        # ArUCo 마커가 표시된 이미지를 토픽으로 발행
        try:
            image_message = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.image_publisher.publish(image_message)
        except Exception as e:
            self.get_logger().error(f"Failed to publish image: {e}")

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped by user.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
