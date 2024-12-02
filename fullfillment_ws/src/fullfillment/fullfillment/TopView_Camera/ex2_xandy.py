#ex2_xandy.py
import cv2
import cv2.aruco as aruco
import numpy as np

# 마커 크기 (단위: 미터, 예: 0.05m = 5cm)
marker_length = 0.108

# 비디오 캡처 초기화
cap = cv2.VideoCapture('/dev/video2')
# MJPG 포맷으로 설정
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# 해상도 설정: 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ArUCo 딕셔너리 선택 (DICT_4X4_50은 4x4 마커, ID 50개)``
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()

# 기준 마커 ID
origin_id = 54
x_axis_id = 55
y_axis_id = 51
c_id = 53  # 벡터 c에 사용할 마커 ID

# 카메라 캘리브레이션 데이터
from calibration import ret, mtx, dist

def draw_axes_with_vectors(frame, origin, x_axis, y_axis, c_point):
    """기준점에서 X축, Y축, C축 선으로 표시"""
    # X축
    if x_axis is not None:
        cv2.line(frame, tuple(origin), tuple(x_axis), (255, 0, 0), 2)  # 파란색
    # Y축
    if y_axis is not None:
        cv2.line(frame, tuple(origin), tuple(y_axis), (0, 255, 0), 2)  # 초록색
    # C축
    if c_point is not None:
        cv2.line(frame, tuple(origin), tuple(c_point), (0, 0, 255), 2)  # 빨간색

    # 벡터 계산
    vector_a = np.array(x_axis) - np.array(origin) if x_axis is not None else None  # 54-55
    vector_b = np.array(y_axis) - np.array(origin) if y_axis is not None else None  # 54-51
    vector_c = np.array(c_point) - np.array(origin) if c_point is not None else None  # 54-53

    return vector_a, vector_b, vector_c

def compute_projection(vector_1, vector_2):
    """일반화된 투영 계산: v1 · v2 / |v1|^2"""
    if vector_1 is not None and vector_2 is not None:
        dot_product = np.dot(vector_1, vector_2)  # v1 · v2
        v1_length_squared = np.linalg.norm(vector_1) ** 2  # |v1|^2
        if v1_length_squared != 0:
            return dot_product / v1_length_squared
    return None

def display_xy_values(frame, x_value, y_value):
    """창 하단에 x와 y 값을 표시"""
    height, width = frame.shape[:2]
    # 검은색 바 생성
    cv2.rectangle(frame, (0, height - 30), (width, height), (0, 0, 0), -1)
    # x와 y 값 텍스트 표시
    text = f"x = {x_value:.4f}" if x_value is not None else "x = N/A"
    text += f", y = {y_value:.4f}" if y_value is not None else ", y = N/A"
    cv2.putText(frame, text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ArUCo 마커 탐지
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:  # 마커가 감지된 경우
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_length, mtx, dist)

        # 기준 마커 및 축 마커의 좌표
        origin, x_axis, y_axis, c_point = None, None, None, None

        for i, id_ in enumerate(ids.flatten()):
            # 마커 중심 계산
            center_x = int(corners[i][0][:, 0].mean())
            center_y = int(corners[i][0][:, 1].mean())
            center_coordinates = (center_x, center_y)

            # ID별 처리
            if id_ == origin_id:
                origin = center_coordinates
            elif id_ == x_axis_id:
                x_axis = center_coordinates
            elif id_ == y_axis_id:
                y_axis = center_coordinates
            elif id_ == c_id:
                c_point = center_coordinates

            # ID와 중심 표시
            cv2.circle(frame, center_coordinates, 5, (0, 255, 255), -1)  # 중심점
            cv2.putText(frame, f"ID: {id_}", (center_x + 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # X축, Y축 및 C축 표시 및 벡터 계산
        if origin is not None:
            vector_a, vector_b, vector_c = draw_axes_with_vectors(frame, origin, x_axis, y_axis, c_point)
            x_value = compute_projection(vector_a, vector_c)  # x 계산
            y_value = compute_projection(vector_b, vector_c)  # y 계산
            display_xy_values(frame, x_value, y_value)

        # 탐지된 마커 표시
        aruco.drawDetectedMarkers(frame, corners, ids)

    # 결과 출력
    cv2.imshow('ArUCo Marker Detection', frame)

    # ESC 키로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
