# TopView_Camera_node.py

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
        # 비디오 usb포트 확인하는 방법 : ffplay /dev/video4
        self.cap = cv2.VideoCapture('/dev/video4')

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
        self.marker_length = 0.1  # 마커 크기 (미터 단위)
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        self.parameters = aruco.DetectorParameters_create()

        # JSON 파일에서 캘리브레이션 데이터 읽기
        calibration_file = 'src/fullfillment/fullfillment/TopView_Camera/calibration.json'  # JSON 파일 경로를 설정하세요
        try:
            with open(calibration_file, 'r') as file:
                calibration_data = json.load(file)
                self.mtx = np.array(calibration_data['mtx'])
                self.dist = np.array(calibration_data.get('dist', [0, 0, 0, 0, 0]))  # dist 기본값 설정
        except Exception as e:
            self.get_logger().error(f"Failed to load calibration data: {e}")
            raise

        # Timer로 detect_markers 주기 호출
        self.timer = self.create_timer(0.1, self.detect_markers)

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

            marker_ids = []
            poses = PoseArray()
            for i in range(len(ids)):
                # ID 저장
                marker_ids.append(int(ids[i][0]))

                # 위치 및 방향 저장
                pose = Pose()
                pose.position.x = tvecs[i][0][0]
                pose.position.y = tvecs[i][0][1]
                pose.position.z = tvecs[i][0][2]
                pose.orientation.x = rvecs[i][0][0]
                pose.orientation.y = rvecs[i][0][1]
                pose.orientation.z = rvecs[i][0][2]
                pose.orientation.w = 1.0  # 기본값
                poses.poses.append(pose)

                # ArUCo 마커 경계와 좌표 그리기
                aruco.drawDetectedMarkers(frame, corners, ids)
                aruco.drawAxis(frame, self.mtx, self.dist, rvecs[i], tvecs[i], 0.1)

            # 메시지 생성
            detection_msg = ArucoDetections()
            detection_msg.marker_ids = marker_ids
            detection_msg.poses = poses

            # detections 퍼블리시
            self.detections_publisher.publish(detection_msg)
        else:
            self.get_logger().info("No markers detected.")

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
