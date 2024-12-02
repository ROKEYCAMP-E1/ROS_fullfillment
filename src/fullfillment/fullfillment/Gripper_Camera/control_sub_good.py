#!/usr/bin/env python3
#control_sub_good.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header, String
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand
import math
import sys
import select
import termios
import tty
import threading


class Turtlebot3ManipulationWithKeyboard(Node):
    def __init__(self):
        super().__init__('turtlebot3_keyboard_control')

        # Publishers
        self.cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)

        # Subscribers
        self.feedback_subscriber = self.create_subscription(
            String, '/feedback_topic', self.feedback_callback, 10
        )

        # Gripper Action Client
        self.gripper_action_client = ActionClient(self, GripperCommand, 'gripper_controller/gripper_cmd')

        # Twist message for movement
        self.move_cmd = Twist()
        self.move_cmd.linear.x = 0.0  # Default linear speed
        self.move_cmd.angular.z = 0.0  # Default angular speed

        # Initialize joint positions
        self.joint_positions = [0.0, 0.0, math.radians(40), math.radians(10)]

        # Initial joint state publication
        self.publish_joint_trajectory()

        self.get_logger().info(
            "Keyboard Control Node Started. "
            "Use i/k to move forward/backward, j/l to rotate left/right, "
            "1/2/3/4 to increase joint angles, q/w/e/r to decrease them, "
            "'d' to open gripper, 'f' to close gripper, "
            "'z' to move to predefined angles, 'x' to reset to origin. Press Ctrl+C to exit."
        )

        # Start keyboard input thread
        self.input_thread = threading.Thread(target=self.keyboard_input_loop, daemon=True)
        self.input_thread.start()

    def feedback_callback(self, msg):
        """피드백 메시지 처리"""
        self.get_logger().info(f"Received feedback: {msg.data}")
        # 피드백 메시지에 따라 동작을 추가적으로 정의할 수 있음
        if "left/right" in msg.data:
            self.get_logger().info("Adjusting based on feedback: Moving sideways.")
            self.move_cmd.linear.x = 0.0
            self.move_cmd.angular.z = 0.2  # Example of rotation adjustment
            self.cmd_vel.publish(self.move_cmd)
        elif "up/down" in msg.data:
            self.get_logger().info("Adjusting based on feedback: Moving fㅔㅔㅔorward/backward.")
            self.move_cmd.linear.x = 0.1
            self.move_cmd.angular.z = 0.0  # Example of linear adjustment
            self.cmd_vel.publish(self.move_cmd)

    def publish_joint_trajectory(self):
        trajectory_msg = JointTrajectory()
        trajectory_msg.header = Header()
        trajectory_msg.header.stamp = self.get_clock().now().to_msg()
        trajectory_msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

        point = JointTrajectoryPoint()
        point.positions = self.joint_positions
        point.velocities = [0.0] * 4
        point.time_from_start.sec = 1
        point.time_from_start.nanosec = 0

        trajectory_msg.points = [point]
        self.joint_pub.publish(trajectory_msg)

        self.get_logger().info(f"Published Joint Trajectory: {trajectory_msg}")

    def keyboard_input_loop(self):
        while rclpy.ok():
            key = self.get_key()
            if key:
                self.process_key(key)

    def get_key(self):
        original_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            key = None
            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
        return key

    def process_key(self, key):
        angle_increment = math.radians(5)
        if key == '1':
            self.joint_positions[0] += angle_increment
            self.publish_joint_trajectory()
        elif key == 'q':
            self.joint_positions[0] -= angle_increment
            self.publish_joint_trajectory()
        elif key == '2':
            self.joint_positions[1] += angle_increment
            self.publish_joint_trajectory()
        elif key == 'w':
            self.joint_positions[1] -= angle_increment
            self.publish_joint_trajectory()
        elif key == '3':
            self.joint_positions[2] += angle_increment
            self.publish_joint_trajectory()
        elif key == 'e':
            self.joint_positions[2] -= angle_increment
            self.publish_joint_trajectory()
        elif key == '4':
            self.joint_positions[3] += angle_increment
            self.publish_joint_trajectory()
        elif key == 'r':
            self.joint_positions[3] -= angle_increment
            self.publish_joint_trajectory()
        elif key == 'z':
            self.set_predefined_angles()
        elif key == 'x':
            self.reset_to_origin()
        elif key == 'd':
            self.send_gripper_goal(0.025)
        elif key == 'f':
            self.send_gripper_goal(-0.015)
        elif key in ['i', 'k', 'j', 'l']:
            self.update_movement(key)
        elif key == '\x03':
            raise KeyboardInterrupt

    def set_predefined_angles(self):
        self.joint_positions[1] = math.radians(40)
        self.joint_positions[2] = math.radians(10)
        self.joint_positions[3] = math.radians(-10)
        self.publish_joint_trajectory()

    def reset_to_origin(self):
        self.joint_positions[1] = 0.0
        self.joint_positions[2] = math.radians(40)
        self.joint_positions[3] = math.radians(10)
        self.publish_joint_trajectory()

    def update_movement(self, key):
        if key == 'i':
            self.move_cmd.linear.x = -0.1
            self.move_cmd.angular.z = 0.0
        elif key == 'k':
            self.move_cmd.linear.x = 0.1
            self.move_cmd.angular.z = 0.0
        elif key == 'j':
            self.move_cmd.linear.x = 0.0
            self.move_cmd.angular.z = 0.25
        elif key == 'l':
            self.move_cmd.linear.x = 0.0
            self.move_cmd.angular.z = -0.25

        self.cmd_vel.publish(self.move_cmd)

    def send_gripper_goal(self, position):
        goal = GripperCommand.Goal()
        goal.command.position = position
        goal.command.max_effort = -1.0

        if not self.gripper_action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Gripper action server not available!")
            return

        self.gripper_action_client.send_goal_async(goal)

    def run(self):
        try:
            while rclpy.ok():
                rclpy.spin_once(self)
        except KeyboardInterrupt:
            self.get_logger().info("Ctrl+C detected. Exiting...")
        finally:
            self.get_logger().info("Shutting down Turtlebot3 Keyboard Control Node.")


def main(args=None):
    rclpy.init(args=args)
    node = Turtlebot3ManipulationWithKeyboard()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
