# script to turn all easter dates into all significant dates for that year
import pandas as pd
from termcolor import colored
import time
import datetime
import json

# filenames
inputFilename                   =   'all_easter_sundays.csv'
outputFilename                  =   'all_easter_dates.csv'

# welcome user
print colored('Date Processor', 'yellow', attrs=['bold', 'underline'])

# load in all Easter Sunday dates, courtesy of the Astronomical Society of
# South Australia, via: http://tlarsen2.tripod.com/anthonypolumbo/apeasterdates.html
allDates                        =   pd.read_csv(inputFilename, index_col=1)
datesToCalc                     =   [
    ('maundyThursday', datetime.timedelta(days=-3)),
    ('goodFriday', datetime.timedelta(days=-2)),
    ('easterSaturday', datetime.timedelta(days=-1)),
    ('whitSunday', datetime.timedelta(days=(7*7))),
    ('shroveTuesday', datetime.timedelta(days=-47)),
    ('firstDayLent', datetime.timedelta(days=-46))
]

# add new columns to our dataframe
for (series, operation) in datesToCalc:
    allDates[series]            =   None

# loop through each Easter
for (rowId, yearRow) in allDates.iterrows():
    # find out when Easter was
    easterSundayTime            =   datetime.datetime.strptime(yearRow['easterSunday'], '%d %B %Y').date()
    print '\n\n {0:4d}'.format(rowId), colored(easterSundayTime.year, 'cyan', attrs=['underline'])
    # start out by displaying Sunday
    print ' - Easter Sunday: ', colored('{0}/{1}'.format(easterSundayTime.day, easterSundayTime.month), 'cyan')
    allDates.loc[rowId, 'easterSunday'] =   easterSundayTime

    # display all dates to the user
    for (calcDateName, interval) in datesToCalc:
        calcDate                =   easterSundayTime + interval
        print ' - {0}: '.format(calcDateName), colored('{0}/{1}'.format(calcDate.day, calcDate.month), 'cyan')
        allDates.loc[rowId, calcDateName]  = calcDate

# sort
allDates.sort(['easterSunday'], inplace=True)

# save to csv
allDates.to_csv(outputFilename)
