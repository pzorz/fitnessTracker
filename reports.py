import utils
from PyQt6.QtWidgets import QMessageBox

# this procedure can print 1 of 2 types of reports
def reportPrinter(reportType):
    if reportType is utils.ReportType.maxVols:
        with open("/Users/peterzorzonello/Development/Python/fitnessTracker/reports/maxVols.log", "w") as file:
            file.write("MAX VOL REPORT\n\n")
            for key in utils.maxVolReport.keys():
                file.write(key + '\n\t\t\tMax Vol: ' + str(utils.maxVolReport[key]) + ' lbs.\n\n')
        msg = QMessageBox()
        msg.setText("File: /Users/peterzorzonello/Development/Python/fitnessTracker/reports/maxVols.log created!")
        x = msg.exec()

    elif reportType is utils.ReportType.mostRecent:
        with open("/Users/peterzorzonello/Development/Python/fitnessTracker/reports/mostRecent.log", "w") as file:
            file.write("MOST RECENT REPORT\n")
            for lift in utils.mostRecentRpt.keys():
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