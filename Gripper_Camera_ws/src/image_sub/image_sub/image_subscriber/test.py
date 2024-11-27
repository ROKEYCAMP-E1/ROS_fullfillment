import cv2
from ultralytics import YOLO
import time

# YOLOv8 모델 로드 (사전 훈련된 모델 사용)
model = YOLO('yolov8n.pt')

# 웹캠 열기
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 웹캠에서 한 프레임을 읽어옴
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # YOLOv8 모델로 객체 탐지 수행
    results = model(frame)

    # 탐지된 객체가 있을 경우
    if len(results[0].boxes) > 0:
        # render()를 통해 바운딩 박스가 포함된 이미지를 얻음
        frame_with_boxes = results[0].plot()

        # 탐지된 이미지를 항상 같은 이름으로 덮어쓰기
        filename = "detected_image.jpg"
        cv2.imwrite(filename, frame_with_boxes)
        print(f"탐지된 이미지를 {filename}로 덮어썼습니다.")

    # 0.25초 대기 (0.25초마다 갱신)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# 웹캠 자원 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
