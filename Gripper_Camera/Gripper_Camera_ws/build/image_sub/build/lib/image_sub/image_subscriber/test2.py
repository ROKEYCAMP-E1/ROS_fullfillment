import cv2
import time

# 이미지를 주기적으로 읽어와서 화면에 표시하는 함수
def show_image_periodically(filename):
    while True:
        # 이미지 읽기
        img = cv2.imread(filename)

        if img is None:
            print(f"{filename}을(를) 읽을 수 없습니다.")
            break

        # 이미지를 화면에 표시
        cv2.imshow("Detected Image", img)

        # 0.25초(250ms) 대기
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # 창 닫기
    cv2.destroyAllWindows()

# "detected_image.jpg"를 주기적으로 표시
show_image_periodically("detected_image.jpg")
