import pandas as pd


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