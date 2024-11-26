# workspace.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi  # .ui 파일 로드를 위한 모듈
from PyQt5.QtCore import QTimer
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
from utils.send_email import send_email
from utils.auth import load_user_data


    
class WorkspaceWindow(QMainWindow):
    mypage_load = pyqtSignal()
    control_load = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("UI/ui/workspace.ui", self)

        self.control_window = ControlWindow()
        self.control_window.send_text.connect(self.update_text_browser)

        self.jobbox.activated.connect(self.update_selected_job)  
        self.selectjob.clicked.connect(self.add_job_to_list)

        self.timer_obj = QTimer(self)
        self.timer_obj.timeout.connect(self.update_timer)  # 매초 호출할 함수 연결
        self.elapsed_time = 0  

        self.selected_list = []  # 선택된 작업 저장
        self.textBrowser.setText("")
        self.textBrowser_2.setText("")  # 텍스트 초기화
        self.textBrowser_3.setText("경과 시간:  초")

        self.mypage_button.clicked.connect(self.emit_mypage_load) 
        self.control.clicked.connect(self.emit_control_load)

        self.current_job = None


    def emit_mypage_load(self):
        self.mypage_load.emit()

    def emit_control_load(self):
        self.control_load.emit()

    def update_selected_job(self):
        """현재 ComboBox에서 선택된 작업을 업데이트"""
        current_job = self.jobbox.currentText()
        self.current_job = current_job  # 선택된 작업 저장


    def add_job_to_list(self):
        """선택된 작업을 리스트에 누적"""
        if self.current_job:
            self.selected_list.append(self.current_job)  # 리스트에 추가
            self.textBrowser_2.append(self.current_job)  # 텍스트 브라우저에 추가

            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 작업 시작 시간 저장

            # 타이머 초기화 및 시작
            self.elapsed_time = 0
            self.timer_obj.start(1000)  # 1초마다 update_timer 실행

    def update_timer(self):
            """타이머를 1초 단위로 업데이트"""
            self.elapsed_time += 1  # 1초 증가
            self.textBrowser_3.setText(f"경과 시간: {self.elapsed_time} 초")  # textBrowser3에 경과 시간 표시

    def update_text_browser(self, text):
        """ControlWindow에서 전달받은 텍스트를 textBrowser에 출력"""
        self.textBrowser.append(text)  # 텍스트 브라우저에 텍스트 추가



class ControlWindow(QMainWindow):
    send_text = pyqtSignal(str)
    _instance = None # Singleton 인스턴스 저장
    _initialized = False  # 초기화 상태 플래그

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ControlWindow, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self,parent=None):
        if not self._initialized:
            super().__init__(parent)
            loadUi("UI/ui/control_window.ui", self)

            # 버튼 연결
            self.play.clicked.connect(self.play_robot)
            self.pause.clicked.connect(self.pause_robot)
            self.stop.clicked.connect(self.stop_robot)
            self.resume.clicked.connect(self.resume_robot)
            self.run_con.clicked.connect(self.run_conveyor)
            self.stop_con.clicked.connect(self.stop_conveyor)
            self.gohome.clicked.connect(self.close)

            self._initialized = True  # 초기화 완료 플래그 설정

    def play_robot(self):
        text_to_send = "Robot play"
        self.send_text.emit(text_to_send) 
    def pause_robot(self):
        text_to_send = "Robot pause"
        self.send_text.emit(text_to_send) 
    def stop_robot(self):
        text_to_send = "Robot stop"
        self.send_text.emit(text_to_send) 
    def resume_robot(self):
        text_to_send = "Robot resume"
        self.send_text.emit(text_to_send) 

    def run_conveyor(self):
        text_to_send = "conveyor run"
        self.send_text.emit(text_to_send) 
    def stop_conveyor(self):
        text_to_send = "conveyor stop"
        self.send_text.emit(text_to_send) 


    def send_workspace_email(self, message):
        user_data = load_user_data()
        receiver_email = user_data["email"]
        subject = "Workspace Report"

        if message:
            send_email(receiver_email, subject, message)
        else:
            print("메시지가 비어 있습니다.")


