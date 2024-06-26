import utils
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import os

# this procedure can print 1 of 2 types of reports
def reportPrinter(reportType):

    current_directory = os.path.dirname(os.path.abspath(__file__))
    fileName = QFileDialog.getSaveFileName(None,
                                           "Name the report",
                                           current_directory,
                                           '*.log')

    if reportType is utils.ReportType.maxVols:

        try:

            if len(utils.maxVolReport) == 0:
                raise
            sortedKeys = list(utils.maxVolReport.keys())
            sortedKeys.sort()

            with open(fileName[0], "w") as file:
                file.write("MAX VOL REPORT\n\n")
                for key in sortedKeys:
                    file.write(key + '\n\t\t\tMax Vol: ' + str(utils.maxVolReport[key]) + ' lbs.\n\n')
            msg = QMessageBox()
            msg.setText("File: " + fileName[0] + " created!")
            x = msg.exec()

        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setText("Could not generate maxVols report!")
            msg.setIcon(QMessageBox.Icon.Critical)
            x = msg.exec()

    elif reportType is utils.ReportType.mostRecent:
        try:
            if len(utils.maxVolReport) == 0:
                raise
            sortedKeys = list(utils.mostRecentRpt.keys())
            sortedKeys.sort()

            with open(fileName[0], "w") as file:
                file.write("MOST RECENT REPORT\n")
                for lift in sortedKeys:
                    file.write('\n' + lift + '\n')
                    for index in utils.mostRecentRpt[lift]:
                        if 'Weight' in index:
                            file.write('\t' + str(index['Weight']) + 'lbs. for ' + str(index['Sets']) +
                                       ' sets for ' + str(index['Reps']) + ' reps - ' + str(index['Date']) + '\n')
                        elif 'Dur' in index:
                            file.write('\t' + str(index['Sets']) +
                                       ' sets for ' + str(index['Dur']) + ' - ' + str(index['Date']) + '\n')
                        else:
                            file.write('\t' + str(index['Sets']) +
                                       ' sets for ' + str(index['Reps']) + ' reps - ' + str(index['Date']) + '\n')
            msg = QMessageBox()
            msg.setText("File: " + fileName[0] + " created!")
            x = msg.exec()
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Could not generate mostRecent report!")
            x = msg.exec()