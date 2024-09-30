#LOGIN PAGE

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from database import *
#imprt pyqtSignal
from PyQt5.QtCore import pyqtSignal

class LoginWidget(QtWidgets.QWidget):
    onLogin = pyqtSignal(object)
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        uic.loadUi('UI/LoginWidget.ui', self)
        self.loginBtn.clicked.connect(self.login)
        self.username.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.login)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        if DBlogin(username, password):
            self.username.clear()
            self.password.clear()
            self.username.setFocus()
            self.onLogin.emit(self)
            
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Username or Password')

    