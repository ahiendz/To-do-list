from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QVBoxLayout, QLabel, QPushButton, QDialog, QListWidgetItem, QListWidget, QDateEdit
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sys
import json
import uuid

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

        # Khởi tạo biến user và email hiện tại
        self.current_user = None
        self.current_email = None

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
                    with open("MULTI_USER_DATA.json", "r") as infile:
                        return json.load(infile)
                except (json.JSONDecodeError, FileNotFoundError):
                    return {"users": []}

            data = read_data()
            user_found = None
            for user in data["users"]:
                if (user["username"] == username_or_email or user["email"] == username_or_email) and user["password"] == password:
                    user_found = user
                    break
            
            if user_found:
                self.current_user = user_found["username"]
                self.main_window.set_user(self.current_user)
                self.main_window.show()
                
            else:
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
                    with open("MULTI_USER_DATA.json", "r") as infile:
                        return json.load(infile)

                def write_data(data):
                    with open("MULTI_USER_DATA.json", "w") as outfile:
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

# Lớp Dialog cho tùy chọn task
class TaskDialog(QDialog):
    def __init__(self, task_item, parent=None):
        super().__init__(parent)
        self.task_item = task_item
        self.setWindowTitle("Task Options")
        layout = QVBoxLayout()
        
        self.label = QLabel(f"Task: {task_item.text()}")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        self.btn_delete = QPushButton("Delete Task")
        self.btn_important = QPushButton("Mark as Important")
        
        layout.addWidget(self.label)
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_important)
        
        self.setLayout(layout)

# Lớp MainWindow (sử dụng đúng tên object từ UI)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
        self.tasks = []

        # Load UI và kết nối object theo tên
        try:
            uic.loadUi(r"GUi\Tesst.ui", self)  # Đảm bảo file UI có đúng tên object
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load UI: {e}")
            sys.exit()

        # Kết nối sự kiện với đúng tên object
        self.lineEdit_newTask.returnPressed.connect(self.add_task)  # QLineEdit
        self.btn_toggle_completed.clicked.connect(self.toggle_completed)  # QToolButton
        self.listWidget_tasks.itemDoubleClicked.connect(self.open_task_dialog)  # QListWidget
        self.listWidget_tasks.itemChanged.connect(self.handle_task_completion)  # Xử lý checkbox
        self.btn_delete_all.clicked.connect(self.delete_all_completed_tasks)

        self.listWidget_completed.setVisible(False)
        self.btn_delete_all.setVisible(False)

    def set_user(self, username):
            """Cập nhật thông tin user sau khi đăng nhập"""
            self.username = username
            self.QLabelUsername.setText(f"Welcome, {self.username}!")

            # Tải dữ liệu và task của user
            self.load_data()
            self.load_tasks()

    # Thêm task mới
    def add_task(self):
        task_text = self.lineEdit_newTask.text().strip()
        if task_text:
            new_task = {
                "text": task_text,
                "important": False,
                "day": "",
                "completed": False
            }
            self.tasks.append(new_task)
            self.save_data()
            
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.listWidget_tasks.addItem(item)
            self.lineEdit_newTask.clear()

    # Xử lý task hoàn thành
    def handle_task_completion(self, item):
        if item.checkState() == Qt.CheckState.Checked:
            # Cập nhật JSON và chuyển task sang Completed
            for task in self.tasks:
                if task["text"] == item.text():
                    task["completed"] = True
                    self.listWidget_completed.addItem(item.text())
                    self.listWidget_tasks.takeItem(self.listWidget_tasks.row(item))
            self.save_data()

    # Thu gọn/mở rộng Completed
    def toggle_completed(self):
        is_visible = self.listWidget_completed.isVisible()
        self.listWidget_completed.setVisible(not is_visible)
        self.btn_delete_all.setVisible(not is_visible)
        self.btn_toggle_completed.setArrowType(
            Qt.ArrowType.DownArrow if is_visible else Qt.ArrowType.RightArrow
        )

    # Mở dialog tùy chọn task
    def open_task_dialog(self, item):
        dialog = TaskDialog(item)
        dialog.btn_delete.clicked.connect(lambda: self.delete_task(item))
        dialog.btn_important.clicked.connect(lambda: self.mark_important(item))
        dialog.date_edit.dateChanged.connect(lambda date: self.set_task_date(item, date))
        dialog.exec()

    # Xóa task
    def delete_task(self, item):
        self.tasks = [task for task in self.tasks if task["text"] != item.text()]
        self.save_data()
        self.listWidget_tasks.takeItem(self.listWidget_tasks.row(item))

    # Đánh dấu task quan trọng
    def mark_important(self, item):
        for task in self.tasks:
            if task["text"] == item.text():
                task["important"] = True
                item.setForeground(QColor("red"))
        self.save_data()

    # Đặt ngày hoàn thành
    def set_task_date(self, item, date):
        for task in self.tasks:
            if task["text"] == item.text():
                task["day"] = date.toString("yyyy-MM-dd")
        self.save_data()

    def delete_all_completed_tasks(self):
        # Xóa các task đã hoàn thành khỏi danh sách tasks
        self.tasks = [task for task in self.tasks if not task["completed"]]

        # Xóa tất cả item trong listWidget_completed
        self.listWidget_completed.clear()
        
        # Cập nhật lại dữ liệu và giao diện
        self.save_data()

    # ======== CẢI TIẾN PHƯƠNG THỨC XỬ LÝ USER ========
    def load_data(self):
        # Đọc dữ liệu
        with open("MULTI_USER_DATA.json", "r") as f:
            data = json.load(f)            
            print("Data loaded:", data)  # Kiểm tra dữ liệu
            # Tìm user
            
            print("Current user:", self.username)
            for user in data["users"]:
                if user["username"] == self.username:
                    print("Current user data:", user)  # Xem user có tồn tại không
                    self.tasks = user.get("tasks", [])
                    print("Tasks loaded:", self.tasks)  # Kiểm tra xem có load được không
                    break
                else:
                    print("User not found")

    def save_data(self):
        with open("MULTI_USER_DATA.json", "r+") as f:
            data = json.load(f)
            for user in data["users"]:
                if user["username"] == self.username:
                    user["tasks"] = self.tasks
                    break
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    # Tải task vào UI
    def load_tasks(self):
        for task in self.tasks:
            item = QListWidgetItem(task["text"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            
            if task["completed"]:
                item.setCheckState(Qt.CheckState.Checked)
                self.listWidget_completed.addItem(item.text())
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
                self.listWidget_tasks.addItem(item)
            
            if task["important"]:
                item.setForeground(QColor("red"))

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