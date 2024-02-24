from fit import *
import sys
import liftData
import reports
import bodyData
import utils
import os

from PyQt6.QtWidgets import QFileDialog


# create a class that will be able to display the autogen code. We cannot edit that file so all callbacks will
# need to be made in this class instead.
class Fit(Ui_MainWindow):
    # constructor
    def __init__(self, window):
        self.setupUi(window)

        # callbacks for when the buttons on the GUI are pressed
        self.liftsButton.clicked.connect(self.processLifts)
        self.bodyButton.clicked.connect(self.processBodyData)
        self.maxVolBtn.clicked.connect(self.runMaxVolReport)
        self.recentBtn.clicked.connect(self.runRecentReport)
        self.bodyDataButton.clicked.connect(self.loadBodyData)
        self.liftDataButton.clicked.connect(self.loadLiftData)

    # display a file picker and then load in the lift data. Process the lift data so it us usable for running reports
    # and printing plots
    def loadLiftData(self):
        f_name = QFileDialog.getOpenFileName(None,
                                             "Pick a CSV for the Lifting Data",
                                             utils.current_directory,
                                             "CSV (*.csv)")
        self.liftDataLabel.setText(f_name[0])
        liftData.processWeightedLifts(f_name[0])

    # set the file that we will use for any of the body measurement data
    def loadBodyData(self):
        f_name = QFileDialog.getOpenFileName(None,
                                             "Pick a CSV for the Lifting Data",
                                             utils.current_directory,
                                             "CSV (*.csv)")
        self.bodyDataLabel.setText(f_name[0])
        bodyData.fileName = f_name[0]

    # this function will generate plots for the lift data
    def processLifts(self):
        liftData.plot_lifts(self.progressBar)

    # this function will plot the body measurement data.
    def processBodyData(self):
        bodyData.process_body_data(self.progressBar)

    # this function will run the max vol report
    def runMaxVolReport(self):
        self.progressBar.setValue(0)
        reports.reportPrinter(utils.ReportType.maxVols)

    # this function will run the most recent lift report
    def runRecentReport(self):
        self.progressBar.setValue(0)
        reports.reportPrinter(utils.ReportType.mostRecent)


# get the current directory we are running the GUI from. This is used for the file dialog default paths
utils.current_directory = os.path.dirname(os.path.abspath(__file__))

# create the app to display
app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()
ui = Fit(mainWin)
mainWin.show()
app.exec()
