import math
import matplotlib.pyplot as plt
import pandas as pd

#this reads in the lift data
def readLiftData(fileName):
    print(fileName)
    data = pd.read_csv(fileName)
    # print(data.to_string())
    # print(data.Lift.unique())
    return data

def processWeightedLifts(data):
    liftTypes = data.Lift.unique();
    master = {}
    for lift in liftTypes:
        #get all the data for one kind of Lift
        new = data.loc[data['Lift'] == lift]

        # print("**************")
        # print(lift)
        # print (new.to_string())
        # dates = new.Date.unique()
        # print(dates)

        #create a table of dates and volume/date for this kind of lift
        df = pd.DataFrame(columns=['Date','Vol'])

        # go over each date for this lift
        for index, row in new.iterrows():
             date = row['Date']
             weight = row['weight']

             #if this is not a body weight exercise
             if not math.isnan(weight):
                 # print("TEST DATE: " + date)
                 reps = row['Num_Reps']
                 sets = row['Num_Sets']
                 #calculate the total vol for this entry
                 vol = (reps * sets * weight)

                 #this is how to check if a date has mutiple entries
                 if date in df.Date.unique():
                     #this date has already been seen so find it and then update it
                     rowIndex = df.index[df['Date'] == date]
                     # print("rowIndex: " + str(rowIndex))
                     df.loc[rowIndex, 'Vol'] = df.loc[rowIndex, 'Vol'] + vol
                    # tempRow = df.loc[df['Date'] == row['Date']]
                    # oldVol = tempRow['Vol']
                    # df.loc[row['Date'], 'Vol'] = oldVol + vol
                    # df.loc[df['Date'] == row['Date']] = tempRow
                 else:
                     #this is the first time this date has been seen so create a new entry
                    # print("New date " + row['Date'])
                    newRow = {"Date" : row['Date'], "Vol" : vol}
                    df.loc[len(df)] = newRow
        if not df.empty:
            # print(df.to_string())
            # print("**************")
            master[lift] = df
        # else:
            # print("Empty Table")
            # print("**************")

    return master

def latestLiftDataReport(rawData):
    liftTypes = rawData.Lift.unique()
    master = {}
    for lift in liftTypes:
        # get all the data for one kind of Lift
        liftData = data.loc[data['Lift'] == lift]
        print(liftData.to_string())

def plotLifts(master):
    # print(master.keys())
    for key in master.keys():
        # print(key)
        # print(master[key])
        master[key].plot(x='Date', y='Vol', style='.-')
        plt.title(key)
        plt.ylabel('Weight')
        plt.xlabel('Date')
        plt.savefig(key+'.png')
        plt.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    liftsFile = input("Enter full path to file to read:")

    if liftsFile.endswith('.csv'):
        data = readLiftData(liftsFile)
        latestLiftDataReport(data)
        # master = processWeightedLifts(data)
        # plotLifts(master)
    else:
        print('File must be a CSV')