import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi  # .ui 파일 로드를 위한 모듈
from PyQt5.QtCore import QTimer
from datetime import datetime
from PyQt5.QtCore import pyqtSignal

class MainApp(QMainWindow):
    mypage_load = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        loadUi("UI/workspace.ui", self)

        self.control_window=ControlWindow()

        self.jobbox.activated.connect(self.update_selected_job)  
        self.selectjob.clicked.connect(self.add_job_to_list)
        self.control.clicked.connect(self.control_window.show)

        self.timer_obj = QTimer(self)
        self.timer_obj.timeout.connect(self.update_timer)  # 매초 호출할 함수 연결
        self.elapsed_time = 0  

        self.selected_list = []  # 선택된 작업 저장
        self.textBrowser_2.setText("")  # 텍스트 초기화
        self.textBrowser_3.setText("경과 시간:  초")

        self.mypage_button.clicked.connect(self.emit_mypage_load)


    def emit_mypage_load(self):
        self.mypage_load.emit()

    def update_selected_job(self):
        """현재 ComboBox에서 선택된 작업을 업데이트"""
        current_job = self.jobbox.currentText()
        self.current_job = current_job  # 선택된 작업 저장


        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 작업 시작 시간 저장

        # 타이머 초기화 및 시작
        self.elapsed_time = 0
        self.timer_obj.start(1000)  # 1초마다 update_timer 실행



    def add_job_to_list(self):
        """선택된 작업을 리스트에 누적"""
        if self.current_job:
            self.selected_list.append(self.current_job)  # 리스트에 추가
            self.textBrowser_2.append(self.current_job)  # 텍스트 브라우저에 추가

    def update_timer(self):
            """타이머를 1초 단위로 업데이트"""
            self.elapsed_time += 1  # 1초 증가
            self.textBrowser_3.setText(f"경과 시간: {self.elapsed_time} 초")  # textBrowser3에 경과 시간 표시


class ControlWindow(QMainWindow):
    def __init__(self,parent=None):
        super(ControlWindow,self).__init__(parent)
        loadUi("UI/control.ui", self)




def main():
    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()