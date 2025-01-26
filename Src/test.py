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
        self.Sign_up_2.clicked.connect(self.show_signup)

    def check_login(self):
        Username_or_email = self.Username_or_email_address.text()
        Password = self.password.text()

        if Username_or_email == "ahiendz" and Password == "huhu18072011":
            self.main_window.show()
            self.close()

        elif Username_or_email == "" or Password == "":
            self.msg_box.setText("Dont leave any field empty")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

        else:
            self.msg_box.setText("Username or password is incorrect")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

    def show_signup(self):
        self.sign_up.show()
        self.close()

class Signup(QMainWindow):
    def __init__(self, sign_in):
        super().__init__()
        uic.loadUi(r"GUi\Signup.ui", self)
        self.sign_in = sign_in
        self.msg_box = QMessageBox()

        self.Sign_up.clicked.connect(self.check_signup)
        self.Sign_in.clicked.connect(self.show_signin)
    def check_signup(self):

        Username = self.Username.text()
        Email = self.Email.text()
        Password = self.Password.text()
        Confirm_password = self.Confirm_password.text()

        if Username == "" or Email == "" or Password == "" or Confirm_password == "":
            self.msg_box.setText("Dont leave any field empty")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

        elif Password != Confirm_password:
            self.msg_box.setText("Password does not match")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

        else:
            self.sign_in.show()

    def show_signin(self):
        self.sign_in.show()
        self.close()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"GUi\Main.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    Main_window = Main()
    signin_window = Signin(None, Main_window)
    signup_window = Signup(signin_window)
    signin_window.sign_up = signup_window

    signin_window.show()

    sys.exit(app.exec())