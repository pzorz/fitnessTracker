import math
import dateutil
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import numpy as np
import pandas as pd
import utils
import os
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog

# create a dictionary, the keys will be the lifts. the tables will have date and volume information
master = {}


# this function will load in the CSV of lift data, process it to do data analysis on it to get
# usable, plot-able information. It will then call a function to plot that data.
def processWeightedLifts(fileName):

    try:

        data = utils.read_csv(fileName)

        # create a list of all the different lifts being tracked
        liftTypes = data.Lift.unique()

        # create a dictionary, the keys will be the lifts. the tables will have date and volume information
        for lift in liftTypes:
            utils.maxVolReport[lift] = 0
            utils.mostRecentRpt[lift] = []

            # get all the data for one kind of Lift
            new = data.loc[data['Lift'] == lift]

            # find the latest date for this kind of lift
            latestDate = new['Date'].values[len(new) - 1]

            # create a table of dates and volume/date for this kind of lift
            df = pd.DataFrame(columns=['Date', 'Vol'])

            # go over each date for this lift
            for index, row in new.iterrows():
                date = row['Date']
                weight = row['weight']

                # if this is not a body weight exercise
                if not math.isnan(weight):
                    weight = utils.to_lbs(weight, row['Units'])
                    reps = row['Num_Reps']
                    sets = row['Num_Sets']

                    # if we are processing the data for the most recent date then save it for a report
                    if date == latestDate:
                        utils.mostRecentRpt[lift].append({'Weight': weight, 'Reps': reps, 'Sets': sets, 'Date': date})

                    # calculate the total vol for this entry
                    vol = (reps * sets * weight)

                    # this is how to check if a date has multiple entries
                    if date in df.Date.unique():
                        # this date has already been seen so find it and then update it
                        rowIndex = df.index[df['Date'] == date]
                        df.loc[rowIndex, 'Vol'] = df.loc[rowIndex, 'Vol'] + vol

                    else:
                        # this is the first time this date has been seen so create a new entry
                        newRow = {"Date": row['Date'], "Vol": vol}
                        df.loc[len(df)] = newRow

                else:  # this is a body weight exercise
                    reps = row['Num_Reps']
                    sets = row['Num_Sets']
                    dur = row['Duration']

                    # if this is the latest date for the exercise then we can record it
                    if date == latestDate:
                        # if dur is a string then it has the seconds' keyword in it, otherwise its NaN
                        # we want to only save duration if this is a timed exercise since we can look at the keys later to
                        # decide how to print the report
                        if not issubclass(type(dur), str):
                            utils.mostRecentRpt[lift].append({'Reps': reps, 'Sets': sets, 'Date': date})
                        else:
                            utils.mostRecentRpt[lift].append({'Reps': reps, 'Sets': sets, 'Dur': dur, 'Date': date})

            # if the data frame is not empty (ie if this is not a body weight exercise) then add the table to a dictionary
            if not df.empty:
                master[lift] = df

                # for the max vol we need to find the date with the most weight
                for index, row in df.iterrows():
                    if row['Vol'] > utils.maxVolReport[lift]:
                        utils.maxVolReport[lift] = row['Vol']

    except Exception as e:
        print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Could not load lift data!")
        x = msg.exec()


# this function takes in the data that care about and plots it
def plot_lifts(progressBar):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    dir = QFileDialog.getExistingDirectory(None,
                                           "Pick a Directory to save the plots",
                                           current_directory)
    try:
        num = len(master.keys())
        numPerLift = 100 / num
        progress = 0.0

        for key in master.keys():
            dates = master[key]['Date'].values
            dateArray = [dateutil.parser.parse(x) for x in dates]
            x = mdates.date2num(dateArray)
            vols = master[key]['Vol'].values

            plt.plot(x, vols, marker='o')

            # add accoutrements to plots
            plt.title(key)
            plt.ylabel('Weight (lbs.)')
            plt.xlabel('Date')
            plt.grid()
            plt.autoscale()

            utils.date_formatter(x)

            # plot the trend line
            z = np.polyfit(x, vols, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), color='purple', linestyle='--')

            # save and close the figure
            plt.savefig(dir + '/' + key + '.png')
            plt.clf()
            progressBar.setValue(progress)
            QApplication.processEvents()
            progress += numPerLift

        progressBar.setValue(100)
        QApplication.processEvents()

    except Exception as e:
        print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Could not generate plots!")
        x = msg.exec()