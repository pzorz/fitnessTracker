from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import utils
import dateutil
from PyQt6.QtWidgets import QApplication, QMessageBox

# this function loads up body data and will plot it
def process_body_data(fileName, progressBar):
    try:
        progress = 0.0

        progressBar.setValue(progress)
        QApplication.processEvents()

        bodyData = utils.read_csv(fileName)

        colNames = bodyData.columns.values

        dates = bodyData['Date'].values
        dateArray = [dateutil.parser.parse(x) for x in dates]
        x = mdates.date2num(dateArray)

        numMeasures = bodyData.shape[1] - 1
        cols = 2

        rows = numMeasures // cols

        if numMeasures % cols != 0:
            rows += 1

        position = range(1, numMeasures + 1)

        fig = plt.figure(figsize=(12, 10), dpi=100)
        fig.suptitle("Body Measurements")

        progressStepper = 100/(numMeasures + 1)

        for k in range(1, numMeasures + 1):
            ax = fig.add_subplot(rows, cols, position[k - 1])
            ax.plot(x, bodyData[colNames[k]].values, marker='o')
            ax.title.set_text(colNames[k])
            ax.set_ylabel("Inches")
            ax.set_xlabel("Date")
            ax.grid()
            utils.plot_trendline(ax, x, bodyData[colNames[k]].values)
            utils.date_formatter(x)

            progress += progressStepper
            progressBar.setValue(progress)
            QApplication.processEvents()

        plt.savefig('/Users/peterzorzonello/Development/Python/fitnessTracker/plots/bodyData.png')
        plt.clf()

        progress = 100
        progressBar.setValue(progress)
        QApplication.processEvents()

    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Could not generate body data plots!")
        x = msg.exec()