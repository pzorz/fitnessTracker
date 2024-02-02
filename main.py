import math
import dateutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from enum import Enum
import utils

class ReportType(Enum):
    maxVols = 1
    mostRecent = 2


##############################
# GLOBAL VARS
##############################
maxVolReport = {}
mostRecentRpt = {}


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
                weight = utils.to_lbs(weight, row['Units'])
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
                        mostRecentRpt[lift].append({'Reps': reps, 'Sets': sets})
                    else:
                        mostRecentRpt[lift].append({'Reps': reps, 'Sets': sets, 'Dur': dur})

        # if the data frame is not empty (ie if this is not a body weight exercise) then add the table to a dictionary
        if not df.empty:
            master[lift] = df

            # for the max vol we need to find the date with the most weight
            for index, row in df.iterrows():
                if row['Vol'] > maxVolReport[lift]:
                    maxVolReport[lift] = row['Vol']
    return master


# def latestLiftDataReport(rawData):
#     liftTypes = rawData.Lift.unique()
#     master = {}
#     for lift in liftTypes:
#         # get all the data for one kind of Lift
#         liftData = data.loc[data['Lift'] == lift]
#         print(liftData.to_string())


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

        utils.date_formatter(x)

        # plot the trend line
        z = np.polyfit(x, vols, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color='purple', linestyle='--')

        # save and close the figure
        plt.savefig('plots/' + key + '.png')
        plt.close()


def process_body_data(bodyData):
    print(bodyData.to_string())
    numMeasures = bodyData.shape[1] - 1
    cols = 5

    rows = numMeasures//cols

    if numMeasures % cols != 0:
        rows += 1

    position = range(1, numMeasures + 1)

    fig = plt.figure(1)
    for k in range(numMeasures):
        ax = fig.add_subplot(rows, cols, position[k])
        ax.plot(1,1)
    plt.show()

    # dates = bodyData['Date'].values
    # dateArray = [dateutil.parser.parse(x) for x in dates]
    # x = mdates.date2num(dateArray)
    #
    #
    # fig = plt.figure(1)
    #
    # # fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    # fig.suptitle("Body Measurements")
    #
    # for key in bodyData.keys():
    #     if key != 'Date':
    #         ax = fig.add_subplot(111)
    #         ax.plot(x, bodyData[key].values, marker='o')
    #         ax.set_title(key)
    # # ax1.plot(x, bodyData['waste'].values, marker='o')
    # # utils.plot_trendline(ax1, x, bodyData['waste'].values)
    # # ax1.set_title('waste')
    # #
    # # ax2.plot(x, bodyData['hips'].values, marker='o')
    # # utils.plot_trendline(ax2, x, bodyData['hips'].values)
    # # ax2.set_title('hips')
    # #
    # # ax3.plot(x, bodyData['chest'].values, marker='o')
    # # utils.plot_trendline(ax3, x, bodyData['chest'].values)
    # # ax3.set_title('chest')
    # #
    # # utils.date_formatter(x)
    #
    # # save and close the figure
    # plt.savefig('plots/bodyData.png')
    # plt.close()
    #
    # print(dates)

# this procedure can print 1 of 2 types of reports
def reportPrinter(reportType):
    if reportType is ReportType.maxVols:
        with open("reports/maxVols.log", "w") as file:
            file.write("MAX VOL REPORT\n\n")
            for key in maxVolReport.keys():
                file.write(key + '\n\t\t\tMax Vol: ' + str(maxVolReport[key]) + ' lbs.\n\n')

    elif reportType is ReportType.mostRecent:
        with open("reports/mostRecent.log", "w") as file:
            file.write("MOST RECENT REPORT\n")
            for lift in mostRecentRpt.keys():
                file.write('\n' + lift + '\n')
                for index in mostRecentRpt[lift]:
                    if 'Weight' in index:
                        file.write('\t' + str(index['Weight']) + 'lbs. for ' + str(index['Sets']) +
                                   ' sets for ' + str(index['Reps']) + ' reps\n')
                    elif 'Dur' in index:
                        file.write('\t' + str(index['Sets']) +
                                   ' sets for ' + str(index['Dur']) + '\n')
                    else:
                        file.write('\t' + str(index['Sets']) +
                                   ' sets for ' + str(index['Reps']) + ' reps\n')


if __name__ == '__main__':
    # data = utils.read_csv('inputData/History-Table 1.csv')
    bodyData = utils.read_csv('inputData/Measurements-Table 1.csv')
    process_body_data(bodyData)

    # latestLiftDataReport(data)

    # master = processWeightedLifts(data)
    #reportPrinter(ReportType.mostRecent)
    # plot_lifts(master)
