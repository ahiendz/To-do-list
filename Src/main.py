import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'C:\Users\Phuong Mai\OneDrive\Documents\Code\DuAn\TO_DO_LIST\GUi\Signin.ui', self)

app = QApplication(sys.argv)
window = Login()

window.show()
app.exec()
