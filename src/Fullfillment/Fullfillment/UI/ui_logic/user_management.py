# user_management.py

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from utils.auth import load_user_data, save_user_data


class LoginWindow(QMainWindow):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("src/Fullfillment/Fullfillment/UI/ui/login_window.ui", self) 
        
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        user_data = load_user_data() # 데이터 로드

        # Verify credentials
        if username == user_data["username"] and password == user_data["password"]:
            self.status_label.setText("로그인에 성공했습니다!")
            # 로그인 성공 시 신호 방출
            self.login_success.emit()
        else:
            self.status_label.setText("아이디 혹은 비밀번호가 잘못되었습니다.")


class MyPageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("src/Fullfillment/Fullfillment/UI/ui/mypage_window.ui", self)

        # Widgets
        user_data = load_user_data() # 데이터로드
        self.current_id_value_label.setText(user_data["username"])
        self.current_email_value_label.setText(user_data["email"])

        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.update_button.clicked.connect(self.update_info)


    def update_info(self):
        current_password = self.current_password_input.text()
        new_email = self.new_email_input.text()
        new_password = self.new_password_input.text()

        user_data = load_user_data() # 데이터 로드

        # Verify current password
        if current_password != user_data["password"]:
            self.status_label.setText("Current password is incorrect.")
            return

        # Update email and password
        if new_email:
            user_data["email"] = new_email
        if new_password:
            user_data["password"] = new_password

        # Save updated data to file
        save_user_data(user_data) # 데이터 저장

        self.status_label.setText("Information updated successfully!")
