#RUN MAINWINDOW
from PyQt5.QtWidgets import QApplication
from PAGES.mainwindow import *
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

