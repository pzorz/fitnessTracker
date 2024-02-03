from fit import *
import sys
import main


# create a class that will be able to display the autogen code. We cannot edit that file so all callbacks will
# need to be made in this class instead.
class Fit(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        # callback for when the lifts button is pressed
        self.liftsButton.clicked.connect(main.processWeightedLifts)


# create the app to display
app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()
ui = Fit(mainWin)
mainWin.show()
app.exec()
