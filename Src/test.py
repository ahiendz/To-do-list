from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import sys

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"GUI/Main.ui", self)
        
        self.toolButton.clicked.connect(self.close)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())