from fit import *
import sys
import main

from PyQt6.QtWidgets import QFileDialog


# create a class that will be able to display the autogen code. We cannot edit that file so all callbacks will
# need to be made in this class instead.
class Fit(Ui_MainWindow):
    #constructor
    def __init__(self, window):
        self.setupUi(window)
        # callback for when the lifts button is pressed
        self.liftsButton.clicked.connect(self.processLifts)

    # this function will open a file picker, get the file and then trigger the plot generator
    def processLifts(self):
        fname = QFileDialog.getOpenFileName(None,
                                            "Pick a CSV for the Lifting Data",
                                            "/Users/peterzorzonello/Development/Python/fitnessTracker/inputData/",
                                            "CSV (*.csv)")
        main.processWeightedLifts(fname[0], self.progressBar)


# create the app to display
app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()
ui = Fit(mainWin)
mainWin.show()
app.exec()
