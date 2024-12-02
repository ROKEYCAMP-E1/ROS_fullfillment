import cv2
import numpy as np

# ArUco 탐지 함수
def detect_aruco_pose(frame, aruco_dict, parameters, camera_matrix, dist_coeffs):
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters)
    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)  # 마커 크기: 0.05m
        for i, id in enumerate(ids):
            # 각 마커의 위치와 방향
            tvec = tvecs[i][0]  # [x, y, z]
            rvec = rvecs[i][0]  # 회전 벡터
            print(f"Marker ID {id}: Position {tvec}, Rotation {rvec}")7
            return tvec, rvec  # 첫 번째 마커의 위치와 방향 반환
    return None, None


import math

# 현재 위치 (ArUco에서 계산됨)
current_position = np.array([current_tvec[0], current_tvec[1]])  # [x, y]

# 목표 위치
goal_position = np.array([1.5, 1.0])  # [x, y] 예: 1.5m, 1.0m

# 벡터 계산g 
vector_to_goal = goal_position - current_position
distance_to_goal = np.linalg.norm(vector_to_goal)  # 거리
angle_to_goal = math.atan2(vector_to_goal[1], vector_to_goal[0])  # 목표 방향 (라디안)
print(f"Distance to goal: {distance_to_goal}, Angle to goal: {math.degrees(angle_to_goal)}°")


# 로봇의 현재 방향 (ArUco에서 추출)
robot_orientation = math.atan2(current_rvec[1], current_rvec[0])  # 라디안

# 목표 방향과 로봇 방향의 차이
angle_difference = angle_to_goal - robot_orientation
print(f"Angle difference: {math.degrees(angle_difference)}°")



from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
import time

class TurtlebotController(Node):
    def __init__(self):
        super().__init__('turtlebot_controller')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def move_to_goal(self, distance, angle):
        twist = Twist()

        # 회전
        if abs(angle) > 0.1:  # 충분히 회전 필요
            twist.linear.x = 0.0
            twist.angular.z = 0.3 if angle > 0 else -0.3  # 시계/반시계 회전
        # 직진
        elif distance > 0.1:  # 목표로 직진
            twist.linear.x = 0.2
            twist.angular.z = 0.0

        # 멈춤
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        # 명령 전송
        self.cmd_vel_publisher.publish(twist)

rclpy.init()
controller = TurtlebotController()

# 이동 루프
while distance_to_goal > 0.1:
    controller.move_to_goal(distance_to_goal, angle_difference)
    time.sleep(0.1)  # 100ms 대기
rclpy.shutdown()
