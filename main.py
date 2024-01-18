import math
import dateutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from enum import Enum


class ReportType(Enum):
    maxVols = 1
    mostRecent = 2


##############################
# GLOBAL VARS
##############################
maxVolReport = {}
mostRecentRpt = {}

# this reads in the lift data
def readLiftData(fileName):
    print(fileName)
    data = pd.read_csv(fileName)
    return data


def to_lbs(weight, unit):
    # units could be empty if this is a duration or body weight exercise
    if not unit is None:
        if unit.lower() == 'kg.':
            return weight * 2.2046
        elif unit.lower().strip() == 'lbs.':
            return weight
        else:
            print('encountered unknown unit: ' + str(unit))
            return weight


def processWeightedLifts(data):
    # create a list of all the different lifts being tracked
    liftTypes = data.Lift.unique()

    # create a dictionary, the keys will be the lifts. the tables will have date and volume information
    master = {}
    for lift in liftTypes:
        maxVolReport[lift] = 0
        mostRecentRpt[lift] = []

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
                weight = to_lbs(weight, row['Units'])
                reps = row['Num_Reps']
                sets = row['Num_Sets']

                # if we are processing the data for the most recent date then save it for a report
                if date == latestDate:
                    mostRecentRpt[lift].append({'Weight': weight, 'Reps': reps, 'Sets': sets})

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

        # if the data frame is not empty (ie if this is not a body weight exercise) then add the table to a dictionary
        if not df.empty:
            master[lift] = df

            # for the max vol we need to find the date with the most weight
            for index, row in df.iterrows():
                if row['Vol'] > maxVolReport[lift]:
                    maxVolReport[lift] = row['Vol']
    return master


def latestLiftDataReport(rawData):
    liftTypes = rawData.Lift.unique()
    master = {}
    for lift in liftTypes:
        # get all the data for one kind of Lift
        liftData = data.loc[data['Lift'] == lift]
        print(liftData.to_string())


def plot_lifts(master):
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

        # Show X-axis major tick marks as dates
        loc = mdates.AutoDateLocator()
        plt.gca().xaxis.set_major_locator(loc)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
        plt.gcf().autofmt_xdate()
        plt.xticks(x)  # make sure only the x-ticks with data are shown

        # plot the trend line
        z = np.polyfit(x, vols, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color='purple', linestyle='--')

        # save and close the figure
        plt.savefig('plots/' + key + '.png')
        plt.close()


# this procedure can print 1 of 2 types of reports
def reportPrinter(reportType):
    if reportType is ReportType.maxVols:
        with open("reports/maxVols.log", "w") as file:
            file.write("MAX VOL REPORT\n\n")
            for key in maxVolReport.keys():
                file.write(key + '\n\t\t\tMax Vol: ' + str(maxVolReport[key]) + ' lbs.\n\n')

    elif reportType is ReportType.mostRecent:
        with open("reports/mostRecent.log", "w") as file:
            file.write("MOST RECENT REPORT\n\n")
            for lift in mostRecentRpt.keys():
                file.write(lift+'\n')
                for index in mostRecentRpt[lift]:
                    file.write('\t'+str(index['Weight']) + 'lbs. for ' + str(index['Sets']) +
                               ' sets for ' + str(index['Reps']) + ' reps\n\n')


if __name__ == '__main__':
    data = readLiftData('inputData/History-Table 1.csv')
    # latestLiftDataReport(data)
    master = processWeightedLifts(data)
    reportPrinter(ReportType.mostRecent)
    # plot_lifts(master)
