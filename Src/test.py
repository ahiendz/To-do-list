from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QVBoxLayout, QLabel, QPushButton, QDialog, QListWidgetItem, QListWidget, QDateEdit
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sys
import json

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
        self.tasks = []

        uic.loadUi(r"GUi\PHATRIENMAINui.ui", self)

        self.qline_add_task.returnPressed.connect(self.add_task)

        self.btn_toggle_completed_Myday.clicked.connect(self.toggle_completed)
        self.btn_toggle_completed_Important.clicked.connect(self.toggle_completed)
        self.btn_toggle_completed_Planned.clicked.connect(self.toggle_completed)
        self.btn_toggle_completed_Task.clicked.connect(self.toggle_completed)
        self.btn_toggle_completed_Groceries.clicked.connect(self.toggle_completed)


        self.listWidget_Myday.itemDoubleClicked.connect(self.open_task_dialog)
        self.listWidget_Important.itemDoubleClicked.connect(self.open_task_dialog)
        self.listWidget_Planned.itemDoubleClicked.connect(self.open_task_dialog)
        self.listWidget_Task.itemDoubleClicked.connect(self.open_task_dialog)
        self.listWidget_Groceries.itemDoubleClicked.connect(self.open_task_dialog)

        self.listWidget_Myday.itemChanged.connect(self.handle_task_completion)
        self.listWidget_Important.itemChanged.connect(self.handle_task_completion)
        self.listWidget_Planned.itemChanged.connect(self.handle_task_completion)
        self.listWidget_Task.itemChanged.connect(self.handle_task_completion)
        self.listWidget_Groceries.itemChanged.connect(self.handle_task_completion)



        self.btn_delete_all_Myday.clicked.connect(self.delete_all_completed_tasks)
        self.btn_delete_all_Important.clicked.connect(self.delete_all_completed_tasks)
        self.btn_delete_all_Planned.clicked.connect(self.delete_all_completed_tasks)
        self.btn_delete_all_Task.clicked.connect(self.delete_all_completed_tasks)
        self.btn_delete_all_Groceries.clicked.connect(self.delete_all_completed_tasks)



        # Kết nối nút bấm với các trang trong QStackedWidget
        self.btn_myday.clicked.connect(lambda: self.switch_page(0))
        self.btn_important.clicked.connect(lambda: self.switch_page(1))
        self.btn_planned.clicked.connect(lambda: self.switch_page(2))
        self.btn_task.clicked.connect(lambda: self.switch_page(3))
        self.btn_groceries.clicked.connect(lambda: self.switch_page(4))



        self.listWidget_completed_Myday.setVisible(False)
        self.btn_delete_all_Myday.setVisible(False)

        self.listWidget_completed_Important.setVisible(False)
        self.btn_delete_all_Important.setVisible(False)

        self.listWidget_completed_Planned.setVisible(False)
        self.btn_delete_all_Planned.setVisible(False)

        self.listWidget_completed_Task.setVisible(False)
        self.btn_delete_all_Task.setVisible(False)

        self.listWidget_completed_Groceries.setVisible(False)
        self.btn_delete_all_Groceries.setVisible(False)

    def switch_page(self, index):
            """Chuyển đổi trang trong QStackedWidget theo index"""
            self.stackedWidget.setCurrentIndex(index)

    def get_current_page(self):
        """Trả về tên của trang hiện tại trong QStackedWidget"""
        return self.stackedWidget.currentWidget().objectName()

    def set_user(self, username):
            """Cập nhật thông tin user sau khi đăng nhập"""
            self.username = username

            # Tải dữ liệu và task của user
            self.load_data()
            self.load_tasks()

    # Thêm task mới
    def add_task(self):
        task_text = self.qline_add_task.text().strip()
        if task_text:
            if main_window.get_current_page() == "Myday":
                new_task = {
                    "text": task_text,
                    "important": False,
                    "day": QDate.currentDate().toString("yyyy-MM-dd"),
                    "is_planned": False,
                    "completed": False
                }
                self.tasks.append(new_task)
                self.save_data()
            elif main_window.get_current_page() == "Important":
                new_task = {
                    "text": task_text,
                    "important": True,
                    "day": "",
                    "is_planned": False,
                    "completed": False
                }
                self.tasks.append(new_task)
                self.save_data()
            elif main_window.get_current_page() == "Planned":
                new_task = {
                    "text": task_text,
                    "important": False,
                    "day": QDate.currentDate().toString("yyyy-MM-dd"),
                    "is_planned": True,
                    "completed": False
                }
                self.tasks.append(new_task)
                self.save_data()
            elif main_window.get_current_page() == "Task":
                new_task = {
                    "text": task_text,
                    "important": False,
                    "day": "",
                    "is_planned": False,
                    "completed": False
                }
                self.tasks.append(new_task)
                self.save_data()
            else:
                pass

            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)

            if main_window.get_current_page() == "Myday":
                self.listWidget_Myday.addItem(item)
            elif main_window.get_current_page() == "Important":
                self.listWidget_Important.addItem(item)
            elif main_window.get_current_page() == "Planned":
                self.listWidget_Planned.addItem(item)
            elif main_window.get_current_page() == "Task":
                self.listWidget_Task.addItem(item)
            else:
                pass

            self.qline_add_task.clear()

        main_window.load_tasks()

    # Xử lý task hoàn thành
    def handle_task_completion(self, item):
        if item.checkState() == Qt.CheckState.Checked:
            # Cập nhật JSON và chuyển task sang Completed
            for task in self.tasks:
                if task["text"] == item.text():
                    task["completed"] = True
                    break
            self.save_data()

    # Thu gọn/mở rộng Completed
    def toggle_completed(self):
        # Lấy trang hiện tại trong QStackedWidget
        current_page = self.get_current_page()

        # Xác định các widget tương ứng với trang hiện tại
        if current_page == "Myday":
            list_widget_completed = self.listWidget_completed_Myday
            btn_delete_all = self.btn_delete_all_Myday
            btn_toggle_completed = self.btn_toggle_completed_Myday
        elif current_page == "Important":
            list_widget_completed = self.listWidget_completed_Important
            btn_delete_all = self.btn_delete_all_Important
            btn_toggle_completed = self.btn_toggle_completed_Important
        elif current_page == "Planned":
            list_widget_completed = self.listWidget_completed_Planned
            btn_delete_all = self.btn_delete_all_Planned
            btn_toggle_completed = self.btn_toggle_completed_Planned
        elif current_page == "Task":
            list_widget_completed = self.listWidget_completed_Task
            btn_delete_all = self.btn_delete_all_Task
            btn_toggle_completed = self.btn_toggle_completed_Task
        elif current_page == "Groceries":
            list_widget_completed = self.listWidget_completed_Groceries
            btn_delete_all = self.btn_delete_all_Groceries
            btn_toggle_completed = self.btn_toggle_completed_Groceries


        # Đảo ngược trạng thái hiển thị của list_widget_completed và btn_delete_all
        is_visible = list_widget_completed.isVisible()
        list_widget_completed.setVisible(not is_visible)
        btn_delete_all.setVisible(not is_visible)

        # Thay đổi biểu tượng mũi tên trên btn_toggle_completed
        btn_toggle_completed.setArrowType(
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
        # Lọc ra các task chưa hoàn thành (completed = False)
        self.tasks = [task for task in self.tasks if not task["completed"]]

        # Xóa tất cả các task đã hoàn thành khỏi các danh sách UI
        self.listWidget_completed_Task.clear()
        self.listWidget_completed_Myday.clear()
        self.listWidget_completed_Important.clear()
        self.listWidget_completed_Planned.clear()
        self.listWidget_completed_Groceries.clear()

        # Lưu dữ liệu mới vào file JSON
        self.save_data()


    def load_data(self):
        with open("MULTI_USER_DATA.json", "r") as f:
            data = json.load(f)
            # Tìm user
            for user in data["users"]:
                if user["username"] == self.username:
                    self.tasks = user.get("tasks", [])
                    break
            else:
                # Nếu user không tồn tại, tạo mới
                self.tasks = []
                new_user = {
                    "username": self.username,
                    "email": "lyahien18072011@gmail.com",
                    "password": "Huhu18072011@",
                    "tasks": []
                }
                data["users"].append(new_user)
                with open("MULTI_USER_DATA.json", "r+") as f:
                    json.dump(data, f, indent=4)
                    f.truncate()

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
        main_window.load_tasks()

    # Tải task vào UI
    def load_tasks(self):
        self.listWidget_Task.clear()
        self.listWidget_Important.clear()
        self.listWidget_Planned.clear()
        self.listWidget_Myday.clear()
        self.listWidget_completed_Task.clear()
        self.listWidget_completed_Important.clear()
        self.listWidget_completed_Planned.clear()
        self.listWidget_completed_Myday.clear()

        for task in self.tasks:

            # Tạo một QListWidgetItem mới cho mỗi danh sách
            item_task = QListWidgetItem(task["text"])
            item_task.setFlags(item_task.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            
            item_myday = QListWidgetItem(task["text"])
            item_myday.setFlags(item_myday.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            item_important = QListWidgetItem(task["text"])
            item_important.setFlags(item_important.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            item_planned = QListWidgetItem(task["text"])
            item_planned.setFlags(item_planned.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            # Thiết lập trạng thái checked/unchecked dựa trên thuộc tính completed
            if task["completed"]:
                item_task.setCheckState(Qt.CheckState.Checked)
                item_myday.setCheckState(Qt.CheckState.Checked)
                item_important.setCheckState(Qt.CheckState.Checked)
                item_planned.setCheckState(Qt.CheckState.Checked)
            else:
                item_task.setCheckState(Qt.CheckState.Unchecked)
                item_myday.setCheckState(Qt.CheckState.Unchecked)
                item_important.setCheckState(Qt.CheckState.Unchecked)
                item_planned.setCheckState(Qt.CheckState.Unchecked)

            if task["completed"]:
                self.listWidget_completed_Task.addItem(item_task)
            else:
                self.listWidget_Task.addItem(item_task)

            if task["day"] == QDate.currentDate().toString("yyyy-MM-dd"):
                if task["completed"]:
                    self.listWidget_completed_Myday.addItem(item_myday)
                else:
                    self.listWidget_Myday.addItem(item_myday)

            if task["important"]:
                if task["completed"]:
                    self.listWidget_completed_Important.addItem(item_important)
                else:
                    self.listWidget_Important.addItem(item_important)

            if task["is_planned"]:
                if task["completed"]:
                    self.listWidget_completed_Planned.addItem(item_planned)
                else:
                    self.listWidget_Planned.addItem(item_planned)

# 4. Hàm khởi chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tạo các cửa sổ
    main_window = MainWindow()
    main_window.set_user("ahiendz")

    main_window.show()
    sys.exit(app.exec())