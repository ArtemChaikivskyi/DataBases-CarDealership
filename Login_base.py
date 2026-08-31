import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget

from Elite_Motors import Autosalon_UI
from Login import Ui_Form

class LoginWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Login_action)
        self.lineEdit.returnPressed.connect(self.Login_action)
        self.lineEdit_2.returnPressed.connect(self.Login_action)

    def Login_action(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        correct_username = "admin"
        correct_password = "1234"

        if username == correct_username and password == correct_password:
            app = QApplication.instance()
            app.main_w = Autosalon_UI()
            app.main_w.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Incorrect username or password")
            self.lineEdit_2.clear()
            self.lineEdit.clear()
            self.lineEdit.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())