from fit import *
# from PySide6 import QtCore, QtWidgets, QtGui
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PyQt6 import uic
import sys
import main


class Fit(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.liftsButton.clicked.connect(main.processWeightedLifts)

    def ClickMe(self):
        print("Lift Button Pressed")

app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()

ui = Fit(mainWin)
mainWin.show()
app.exec()

# Form, Window = uic.loadUiType("fit.ui")
#
# app = QApplication([])
# window = Window()
# form = Form()
# form.setupUi(window)
# window.show()
# app.exec()
