from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidgetItem, QDialog,
    QVBoxLayout, QLabel, QPushButton, QMessageBox, QDateEdit,
    QLineEdit, QListWidget, QGroupBox, QToolButton
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6 import uic
import json
from pathlib import Path
import sys

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
    def __init__(self, username):
        super().__init__()
        self.username = username
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

        # Khởi tạo dữ liệu
        self.load_data()
        self.load_tasks()

        self.listWidget_completed.setVisible(False)
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

    # Tải và lưu dữ liệu JSON
    def load_data(self):
        file_path = Path("TESTDATA.json")
        if not file_path.exists():
            with open("TESTDATA.json", "w") as f:
                json.dump({"users": []}, f, indent=4)
        
        with open("TESTDATA.json", "r") as f:
            data = json.load(f)
            for user in data["users"]:
                if user["username"] == self.username:
                    self.tasks = user.get("tasks", [])
                    break

    def save_data(self):
        with open("TESTDATA.json", "r+") as f:
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

# Chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # CSS để làm đẹp UI
    app.setStyleSheet("""
        QListWidget {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
        }
        QGroupBox {
            border: 1px solid #ccc;
            margin-top: 10px;
            font-weight: bold;
        }
        QToolButton {
            border: none;
            padding: 5px;
        }
    """)
    
    main_window = MainWindow(username="user1")
    main_window.show()
    sys.exit(app.exec())