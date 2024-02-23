import utils
from PyQt6.QtWidgets import QMessageBox

# this procedure can print 1 of 2 types of reports
def reportPrinter(reportType):
    if reportType is utils.ReportType.maxVols:

        try:
            if len(utils.maxVolReport) == 0:
                raise
            sortedKeys = list(utils.maxVolReport.keys())
            sortedKeys.sort()

            with open("/Users/peterzorzonello/Development/Python/fitnessTracker/reports/maxVols.log", "w") as file:
                file.write("MAX VOL REPORT\n\n")
                for key in sortedKeys:
                    file.write(key + '\n\t\t\tMax Vol: ' + str(utils.maxVolReport[key]) + ' lbs.\n\n')
            msg = QMessageBox()
            msg.setText("File: /Users/peterzorzonello/Development/Python/fitnessTracker/reports/maxVols.log created!")
            x = msg.exec()

        except:
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

            with open("/Users/peterzorzonello/Development/Python/fitnessTracker/reports/mostRecent.log", "w") as file:
                file.write("MOST RECENT REPORT\n")
                for lift in sortedKeys:
                    file.write('\n' + lift + '\n')
                    for index in utils.mostRecentRpt[lift]:
                        if 'Weight' in index:
                            file.write('\t' + str(index['Weight']) + 'lbs. for ' + str(index['Sets']) +
                                       ' sets for ' + str(index['Reps']) + ' reps\n')
                        elif 'Dur' in index:
                            file.write('\t' + str(index['Sets']) +
                                       ' sets for ' + str(index['Dur']) + '\n')
                        else:
                            file.write('\t' + str(index['Sets']) +
                                       ' sets for ' + str(index['Reps']) + ' reps\n')
            msg = QMessageBox()
            msg.setText("File: /Users/peterzorzonello/Development/Python/fitnessTracker/reports/mostRecent.log created!")
            x = msg.exec()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Could not generate mostRecent report!")
            x = msg.exec()