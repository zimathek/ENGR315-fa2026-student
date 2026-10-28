import sys
import datetime
"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path='C:/Users/ekzim/OneDrive/Documents/GitHub/ENGR315-fa2026-student/data/covid/us-counties.csv'):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

data = parse_nyt_data()

def get_county_data(data, county_name):
    
    # gets all records for a specific VA county and adds them to list.
    county_data = []

    for entry in data:
        date, county, state, fips, cases, deaths = entry

        if state == 'Virginia' and county == county_name:
            county_data.append((date, cases))

    return county_data

def daily_cases(county_data):
    
    # converts cumulative case counts into individual daily new case counts. returns list of tuples as (date, new_cases).

    daily_cases = []

    for i in range(len(county_data)):
        date, cases = county_data[i]

        if i == 0:
            # finds days where cases actually exist (otherwise why bother).
            new_cases = cases
        else:
            previous_cases = county_data[i - 1][1]
            new_cases = cases - previous_cases

        daily_cases.append((date, new_cases))

    return daily_cases

def first_case(county_data):

    # finds date of first case in the history of ever (wherever is being analyzed).
    
    for date, cases in county_data:
        if cases > 0:
            return date

    return None

def max_daily_cases(daily_cases):
    
    # finds date on which greatest number of new cases was reported.

    max_cases = 0
    max_date = ''

    for date, cases in daily_cases:
        if cases > max_cases:
            max_cases = cases
            max_date = date

    return max_date, max_cases

def worst_seven_days(daily_cases):
    
    # finds seven consecutive days with greatest total number of new cases. returns (starting_date, ending_date, total_cases).
    
    max_total = 0
    max_start = ''
    max_end = ''

    # a SEVEN day period requires at least SEVEN data points soooooo.
    for i in range(len(daily_cases) - 6):
        total = 0

        # adds the new cases for seven consecutive days.
        for j in range(i, i + 7):
            total += daily_cases[j][1]

        if total > max_total:
            max_total = total
            max_start = daily_cases[i][0]
            max_end = daily_cases[i + 6][0]

    return max_start, max_end, max_total

#data for each county

hburg_data = get_county_data(data, 'Harrisonburg city')
rock_data = get_county_data(data, 'Rockingham')

hburg_daily = daily_cases(hburg_data)
rock_daily = daily_cases(rock_data)

#Q1: first positive case in each

hburg_first = first_case(hburg_data)
rock_first = first_case(rock_data)

print("1: First positive COVID case in Harrisonburg:", hburg_first,".")
print("First positive COVID case in Rockingham County:", rock_first, ".")

#Q2: day with greatest number of new cases

hburg_max_date, hburg_max_cases = max_daily_cases(hburg_daily)
rock_max_date, rock_max_cases = max_daily_cases(rock_daily)

print("2: Day with greatest number of new cases in Harrisonburg:", hburg_max_date, "with", hburg_max_cases, "new cases.")
print("Day with greatest number of new cases in Rockingham County:", rock_max_date, "with", rock_max_cases, "new cases.")

#Q3: worst seven-day period

hburg_start, hburg_end, hburg_total = worst_seven_days(hburg_daily)
rock_start, rock_end, rock_total = worst_seven_days(rock_daily)

print("3: Worst seven-day period in Harrisonburg: from", hburg_start, "through", hburg_end, ", with", hburg_total, "cases.")
print("Worst seven-day period in Rockingham County: from", rock_start, "through", rock_end,", with", rock_total, "cases.")