import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray
from ff_interface.msg import ArucoDetections
import cv2
import cv2.aruco as aruco

# 카메라 캘리브레이션 데이터
from .calibration import mtx, dist

class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        self.publisher_ = self.create_publisher(ArucoDetections, 'aruco_detections', 10)

        # 비디오 캡처 초기화
        self.cap = cv2.VideoCapture('/dev/video4')

        # ArUCo 설정
        self.marker_length = 0.1  # 마커 크기 (미터 단위)
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        self.parameters = aruco.DetectorParameters_create()



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
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.marker_length, mtx, dist)

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
                pose.orientation.x = rvecs[i][0][0]  # 간단히 rvec를 quaternion으로 변환할 수도 있음
                pose.orientation.y = rvecs[i][0][1]
                pose.orientation.z = rvecs[i][0][2]
                pose.orientation.w = 1.0  # 기본값
                poses.poses.append(pose)

            # 메시지 생성
            detection_msg = ArucoDetections()
            detection_msg.marker_ids = marker_ids
            detection_msg.poses = poses

            # 메시지 퍼블리시
            self.publisher_.publish(detection_msg)
            self.get_logger().info(f"Published {len(marker_ids)} markers.")
        else:
            self.get_logger().info("No markers detected.")

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
