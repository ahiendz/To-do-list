from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import sys

class Signin(QMainWindow):
    def __init__(self, sign_up, main_window):
        super().__init__()
        uic.loadUi(r"GUi\Signin.ui", self)
        self.sign_up = sign_up
        self.main_window = main_window
        self.msg_box = QMessageBox()

        self.Sign_in.clicked.connect(self.check_login)

    def check_login(self):
        Username_or_email = self.Username_or_email_address.text()
        Password = self.password.text()

        if Username_or_email == "ahiendz" and Password == "huhu18072011":
            self.main_window.show()
        else:
            self.msg_box.setText("Username or password is incorrect")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    signin_window = Signin(None, None)
    signin_window.show()

    sys.exit(app.exec())