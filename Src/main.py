from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
import csv
import uuid
import csv
import os
import json

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

        if not username_or_email or not password:
            self.show_message("Không được để trống trường nào.", QMessageBox.Icon.Warning)
        else:
            def read_data():
                try:
                    with open("DATA.json", "r") as infile:
                        return json.load(infile)
                except (json.JSONDecodeError, FileNotFoundError):
                    return {"users": []}

            data = read_data()
            check = True
            for user in data["users"]:
                if (user["username"] == username_or_email or user["email"] == username_or_email) and user["password"] == password:
                    check = False
                    self.main_window.show()
                    self.close()
                    break
            if check:
                self.show_message("Tk/Mk sai", QMessageBox.Icon.Warning)
                

    

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
        elif not "@gmail.com" in email:
            self.show_message("Email khong hop le", QMessageBox.Icon.Warning)
        elif (not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in '[@_!#$%^&*()<>?/|}{~:]' for char in password) or len(password) > 50):  
            self.show_message("Password khong hop le", QMessageBox.Icon.Warning)
        elif (not any(char.isupper() for char in username) or not any(char.islower() for char in username) or not any(char.isdigit() for char in username) or not any(char in '[@_!#$%^&*()<>?/|}{~:]' for char in username) or len(username) > 20):  
            self.show_message("Username khong hop le", QMessageBox.Icon.Warning)
        else:
            def write_to_json(username, email, password):
                def read_data():
                    with open("DATA.json", "r") as infile:
                        return json.load(infile)

                def write_data(data):
                    with open("DATA.json", "w") as outfile:
                        json.dump(data, outfile, indent=4)

                def add_user(username, email, password):
                    data = read_data()
                    new_user = {
                        "username": username,
                        "email": email,
                        "password": password,
                        "tasks": []
                    }
                    data["users"].append(new_user)
                    write_data(data)

                add_user(username, email, password)

            write_to_json(username, email, password)

            self.show_message("Tao TK Thanh Cong!", QMessageBox.Icon.Information)
            self.signin_window.show()
            self.close()
            
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
        try:
            uic.loadUi(r"GUi\Main\Main.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load UI: {e}")


        # Connect buttons to their respective functions
        self.Myday.clicked.connect(lambda: self.switch_page(0))
        self.Important.clicked.connect(lambda: self.switch_page(1))
        self.Planned.clicked.connect(lambda: self.switch_page(2))
        self.Task.clicked.connect(lambda: self.switch_page(3))
        self.Groceries.clicked.connect(lambda: self.switch_page(4))

        self.btn_addTask.clicked.connect(self.add_task)
        self.btn_removeTask.clicked.connect(self.remove_task)

    def switch_page(self, index):
        print("Switching to page", index)
        self.stackedWidget.setCurrentIndex(index)

    def add_task(self):
        task_text = self.lineEdit_newTask.text()
        if task_text.strip():
            self.listWidget_tasks.addItem(task_text)
            self.lineEdit_newTask.clear()  # Clear the input field after adding
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty.")

    def remove_task(self):
        selected_items = self.listWidget_tasks.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to remove.")
            return
        for item in selected_items:
            self.listWidget_tasks.takeItem(self.listWidget_tasks.row(item))  # Remove selected item


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