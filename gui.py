from fit import *
import sys
import liftData
import reports
import bodyData
import utils
import os

from PyQt6.QtWidgets import QFileDialog

current_directory = ''


# create a class that will be able to display the autogen code. We cannot edit that file so all callbacks will
# need to be made in this class instead.
class Fit(Ui_MainWindow):
    # constructor
    def __init__(self, window):
        self.setupUi(window)

        # callback for when the buttons on the GUI are pressed
        self.liftsButton.clicked.connect(self.processLifts)
        self.bodyButton.clicked.connect(self.processBodyData)
        self.maxVolBtn.clicked.connect(self.runMaxVolReport)
        self.recentBtn.clicked.connect(self.runRecentReport)
        self.bodyDataButton.clicked.connect(self.loadBodyData)
        self.liftDataButton.clicked.connect(self.loadLiftData)

    def loadLiftData(self):
        fname = QFileDialog.getOpenFileName(None,
                                            "Pick a CSV for the Lifting Data",
                                            current_directory,
                                            "CSV (*.csv)")
        self.liftDataLabel.setText(fname[0])

    def loadBodyData(self):
        fname = QFileDialog.getOpenFileName(None,
                                            "Pick a CSV for the Lifting Data",
                                            current_directory,
                                            "CSV (*.csv)")
        self.bodyDataLabel.setText(fname[0])

    # this function will open a file picker, get the file and then trigger the plot generator for the lift data
    def processLifts(self):
        fname = QFileDialog.getOpenFileName(None,
                                            "Pick a CSV for the Lifting Data",
                                            current_directory,
                                            "CSV (*.csv)")
        liftData.processWeightedLifts(fname[0], self.progressBar)

    # this function will open a file picker, get the file and then trigger the plot generator for the body measurement
    # data
    def processBodyData(self):
        fName = QFileDialog.getOpenFileName(None,
                                            "Pick a CSV for the Lifting Data",
                                            current_directory,
                                            "CSV (*.csv)")
        bodyData.process_body_data(fName[0], self.progressBar)

    # this function will run the max vol report
    def runMaxVolReport(self):
        self.progressBar.setValue(0.0)
        reports.reportPrinter(utils.ReportType.maxVols)

    # this function will run the most recent lift report
    def runRecentReport(self):
        self.progressBar.setValue(0.0)
        reports.reportPrinter(utils.ReportType.mostRecent)


current_directory = os.path.dirname(os.path.abspath(__file__))
# create the app to display
app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()
ui = Fit(mainWin)
mainWin.show()
app.exec()
