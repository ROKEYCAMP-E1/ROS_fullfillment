import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

# 파일 경로
DATA_FILE = "/home/rokey/Fullfillment_ws/UI/user_data.json"
login_window_ui = '/home/rokey/Fullfillment_ws/UI/login_window.ui'
mypage_window_ui = '/home/rokey/Fullfillment_ws/UI/mypage_window.ui'


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
    def __init__(self):
        super().__init__()
        loadUi(login_window_ui, self)
        
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        

        # Verify credentials
        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            self.status_label.setText("Login successful!")
            self.open_home_page()
        else:
            self.status_label.setText("Invalid username or password.")

    def open_home_page(self):
        self.home_page = HomePageWindow()
        self.home_page.show()
        self.close()

class HomePageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.setGeometry(100, 100, 1300, 885)

        # Widgets
        self.welcome_label = QLabel(f"Welcome, {USER_DATA['username']}!", self)
        self.my_page_button = QPushButton("Go to My Page", self)
        self.my_page_button.clicked.connect(self.open_my_page)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.my_page_button)
        self.setLayout(layout)

    def open_my_page(self):
        self.my_page = MyPageWindow()
        self.my_page.show()

class MyPageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(mypage_window_ui, self)

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
