import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from enum import Enum


# this class is defining an enum for the types of reports we do
class ReportType(Enum):
    maxVols = 1
    mostRecent = 2


# abstracted function to formate the x-axis dates
# used by multiple plots
def date_formatter(xAxis):
    # Show X-axis major tick marks as dates
    loc = mdates.AutoDateLocator()
    plt.gca().xaxis.set_major_locator(loc)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
    plt.gcf().autofmt_xdate()
    plt.xticks(xAxis)  # make sure only the x-ticks with data are shown


# this function will find the trend line and plot it. If positive trending then its green, negative and its red,
# neutral is gray
def plot_trendline(ax, x, y):
    z = np.polyfit(x, y, 1)
    slope = z[-2]
    p = np.poly1d(z)
    if slope == 0:
        ax.plot(x, p(x), color='gray', linestyle='--')
    elif slope > 0:
        ax.plot(x, p(x), color='green', linestyle='--')
    else:
        ax.plot(x, p(x), color='red', linestyle='--')


# this reads in the lift data
def read_csv(fileName):
    print('Reading: ' + fileName)
    return pd.read_csv(fileName)


# function to convert any unit into lbs
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
