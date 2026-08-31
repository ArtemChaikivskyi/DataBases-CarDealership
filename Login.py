from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(301, 420)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(-30, -40, 370, 480))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"    background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(72, 6, 143, 255), stop:1 rgba(192, 83, 255, 255));\n"
"     color: rgba(255, 255, 255, 210); \n"
"    border-radius: 5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"    background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(78, 15, 150, 255), stop:1 rgba(205, 100, 255, 255));\n"
"}\n"
"QPushButton#pushButton:pressed{\n"
"    padding-left: 5px; \n"
"    padding-top: 5px;\n"
"    background-color:rgba(105, 118, 132, 200);\n"
"}")
        self.widget.setObjectName("widget")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(130, 100, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 160, 200, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0); \n"
"border:none;\n"
"border-bottom: 2px solid rgba(105, 118, 132, 255);\n"
"color :rgba(255, 255, 255, 230);\n"
"padding-bottom: 7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 210, 200, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0); \n"
"border:none;\n"
"border-bottom: 2px solid rgba(105, 118, 132, 255);\n"
"color :rgba(255, 255, 255, 230);\n"
"padding-bottom: 7px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(80, 330, 200, 41))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Armenian")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 40, 301, 420))
        self.label.setStyleSheet("border-image: url(car2.png);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(40, 70, 280, 390))
        self.label_3.setStyleSheet("background-color:rgba(0, 0, 0, 100); \n"
"border-radius: 15px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.pushButton.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Log In"))
        self.lineEdit.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "L o g   I n"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    window = Ui_Form()
    window.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())





