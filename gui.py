from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import sys

Form, Window = uic.loadUiType("fit.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()