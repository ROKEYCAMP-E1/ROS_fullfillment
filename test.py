import cv2

cap = cv2.VideoCapture("/dev/video3")

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    print("카메라 연결 성공")

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
