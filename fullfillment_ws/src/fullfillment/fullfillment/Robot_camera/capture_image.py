import cv2
import os
import time

# 저장 경로 설정    
save_dir = "capture"


# 카메라 초기화 (기본 카메라: 0)
cap = cv2.VideoCapture("/dev/video2")

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("스페이스바를 눌러 사진을 찍고, ESC 키를 눌러 종료하세요.")

while True:
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # 프레임 출력
    cv2.imshow("Camera Feed", frame)

    # 키 입력 대기
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC 키
        print("종료합니다.")
        break
    elif key == 32:  # 스페이스바
        # 현재 시간으로 파일 이름 생성
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(save_dir, f"purple_photo_{timestamp}.jpg")

        # 이미지 저장
        cv2.imwrite(file_name, frame)
        print(f"사진 저장됨: {file_name}")

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
