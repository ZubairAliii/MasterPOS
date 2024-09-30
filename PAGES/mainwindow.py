#MainWINDOW

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import database
from .login import LoginWidget
from .products import ProductWidget
from .pos import PosWidget
from .Salereport import SalereportWidget



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('UI/main.ui', self)

        #LOGIN PAGE
        self.loginWidget = LoginWidget(self)
        self.loginWidget.onLogin.connect(lambda: self.stack.setCurrentIndex(1))
        self.loginPlaceholder.layout().addWidget(self.loginWidget)

        #PRODUCT PAGE
        self.productWidget = ProductWidget(self)
        self.productBtn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.productPlaceholder.layout().addWidget(self.productWidget)

        #POS PAGE
        self.posBtn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.posWidget = PosWidget(self)
        self.posPlaceholder.layout().addWidget(self.posWidget)

        #add Sale Report
        self.salereportbtn.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.salereportwidget = SalereportWidget(self)
        self.salereportPlaceholder.layout().addWidget(self.salereportwidget)

        