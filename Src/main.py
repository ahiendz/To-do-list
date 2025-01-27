from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys

# 1. Lớp Signin (Đăng nhập)
class SignInWindow(QMainWindow):
    def __init__(self, signup_window, main_window):
        super().__init__()
        uic.loadUi(r"GUi/Signin.ui", self)

        # Loại bỏ khung viền và nền đen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Khởi tạo cửa sổ khác
        self.signup_window = signup_window
        self.main_window = main_window

        # Hộp thoại thông báo
        self.message_box = QMessageBox()

        # Gắn sự kiện cho các nút bấm
        self.sign_in_button.clicked.connect(self.validate_login)
        self.switch_to_signup_button.clicked.connect(self.open_signup_window)
        self.closebtt.clicked.connect(self.close)

    def validate_login(self):
        """Xử lý logic đăng nhập."""
        username_or_email = self.username_or_email_input.text()
        password = self.password_input.text()

        if username_or_email == "ahiendz" and password == "huhu18072011":
            self.main_window.show()  # Hiển thị cửa sổ chính
            self.close()

        elif not username_or_email or not password:
            self.show_message("Không được để trống trường nào.", QMessageBox.Icon.Warning)

        else:
            self.show_message("Tên đăng nhập hoặc mật khẩu không đúng.", QMessageBox.Icon.Warning)

    def open_signup_window(self):
        """Mở cửa sổ đăng ký."""
        self.signup_window.show()
        self.close()

    def show_message(self, text, icon):
        """Hiển thị thông báo cho người dùng."""
        self.message_box.setText(text)
        self.message_box.setIcon(icon)
        self.message_box.exec()

# 2. Lớp Signup (Đăng ký)
class SignUpWindow(QMainWindow):
    def __init__(self, signin_window):
        super().__init__()
        uic.loadUi(r"GUi/Signup.ui", self)

        # Loại bỏ khung viền và nền đen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Khởi tạo cửa sổ đăng nhập
        self.signin_window = signin_window

        # Hộp thoại thông báo
        self.message_box = QMessageBox()

        # Gắn sự kiện cho các nút bấm
        self.sign_up_button.clicked.connect(self.process_signup)
        self.switch_to_signin_button.clicked.connect(self.open_signin_window)
        self.closebtt.clicked.connect(self.close)

    def process_signup(self):
        """Xử lý logic đăng ký."""
        email = self.email_input.text()
        password = self.password_input.text()
        username = self.username_input.text()

        if not email or not password or not username:
            self.show_message("Không được để trống trường nào.", QMessageBox.Icon.Warning)
        else:
            self.show_message("Đăng ký thành công (logic lưu trữ cần được bổ sung).", QMessageBox.Icon.Information)

    def open_signin_window(self):
        """Mở cửa sổ đăng nhập."""
        self.signin_window.show()
        self.close()

    def show_message(self, text, icon):
        """Hiển thị thông báo cho người dùng."""
        self.message_box.setText(text)
        self.message_box.setIcon(icon)
        self.message_box.exec()

# 3. Lớp Main (Giao diện chính)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"GUi/Main.ui", self)

# 4. Hàm khởi chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tạo các cửa sổ
    main_window = MainWindow()
    signin_window = SignInWindow(None, main_window)
    signup_window = SignUpWindow(signin_window)

    # Gán cửa sổ đăng ký vào cửa sổ đăng nhập
    signin_window.signup_window = signup_window

    # Hiển thị cửa sổ đăng nhập
    signin_window.show()
    sys.exit(app.exec())
