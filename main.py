import math
import dateutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd


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
    liftTypes = data.Lift.unique();
    master = {}
    for lift in liftTypes:
        # get all the data for one kind of Lift
        new = data.loc[data['Lift'] == lift]

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
                # calculate the total vol for this entry
                vol = (reps * sets * weight)

                # this is how to check if a date has mutiple entries
                if date in df.Date.unique():
                    # this date has already been seen so find it and then update it
                    rowIndex = df.index[df['Date'] == date]
                    df.loc[rowIndex, 'Vol'] = df.loc[rowIndex, 'Vol'] + vol
                else:
                    # this is the first time this date has been seen so create a new entry
                    newRow = {"Date": row['Date'], "Vol": vol}
                    df.loc[len(df)] = newRow
        if not df.empty:
            master[lift] = df
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
        plt.xticks(x) # make sure only the x-ticks with data are shown

        # plot the trend line
        z = np.polyfit(x, vols, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color='purple', linestyle='--')

        # save and close the figure
        plt.savefig('plots/' + key + '.png')
        plt.close()


if __name__ == '__main__':
    data = readLiftData('inputData/History-Table 1.csv')
    # latestLiftDataReport(data)
    master = processWeightedLifts(data)
    plot_lifts(master)
