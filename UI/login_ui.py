import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

# 파일 경로
DATA_FILE = "UI/user_data.json"


# 사용자 데이터 로드 함수
def load_user_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# 사용자 데이터 저장 함수
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 사용자 데이터 초기화
USER_DATA = load_user_data()

class LoginWindow(QMainWindow):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("UI/login_window.ui", self)
        
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        

        # Verify credentials
        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            self.status_label.setText("Login successful!")
            # 로그인 성공 시 신호 방출
            self.login_success.emit()
        else:
            self.status_label.setText("Invalid username or password.")


class MyPageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/mypage_window.ui", self)

        # Widgets
        self.current_id_value_label.setText(USER_DATA["username"])
        self.current_email_value_label.setText(USER_DATA["email"])

        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.update_button.clicked.connect(self.update_info)


    def update_info(self):
        current_password = self.current_password_input.text()
        new_email = self.new_email_input.text()
        new_password = self.new_password_input.text()

        # Verify current password
        USER_DATA = load_user_data()
        if current_password != USER_DATA["password"]:
            self.status_label.setText("Current password is incorrect.")
            return

        # Update email and password
        if new_email:
            USER_DATA["email"] = new_email
        if new_password:
            USER_DATA["password"] = new_password

        # Save updated data to file
        save_user_data(USER_DATA)

        self.status_label.setText("Information updated successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
