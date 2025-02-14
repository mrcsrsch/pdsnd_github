# Import relevant packages
import time
import pandas as pd
import numpy as np

# Main code
# Define global months mapping
months_map = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}
# and its inverse
months_map_inverse = {v: k for k, v in months_map.items()}

#### Functions ####
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['Chicago', 'New York City', 'Washington']
    while True:
        city = input("Enter the name of the city (Chicago, New York City or Washington) you'd like analysed:")
        # make city case insensitive. Especially take care of 'New York City'
        city = " ".join([c.lower().title() for c in city.split(" ")])
        
        if city in valid_cities:
            break

    # get user input for month (All, january, february, ... , june)
    valid_months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December', 'All']
    while True:
        month = input("Enter the month you'd like to focus on. To include All months, simply type 'All':")
        # make month insensitive. Especially take care of 'New York City'
        month = month.lower().title()

        if month not in valid_months:
            print("Try again. Either enter 'All' or the name of a month, which should be fully spelled out. For example: January")
        else: 
            break

    # get user input for day of week (All, monday, tuesday, ... sunday)
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    while True:
        day = input("Enter the day of the week you'd like to focus on. To include All days, simply type 'All':")
        # make day insensitive. Especially take care of 'New York City'
        day = day.lower().title()
        if day not in valid_days:
            print("Try again. Either enter 'All' or the name of the day of the week, which should be fully spelled out. For example: Monday")
        else: 
            break


    print('-'*40)
    return city, month, day


def load_data(city, month=None, day=None):
    """
    Load data for specified city and filter by month and day if applicable.
    
    Args:
        (str) city - name of the city
        (str) month - name of the month to filter by. Leave empty or set to 'All' to apply no filter.
        (str) day - name of the day of the week to filter by. Leave empty or set to 'All' to apply no filter. 
    Returns:
        bspd - Pandas DataFrame containing city bike data filtered by month and day (if applicable)
    """
    CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

    # get filename and load data
    filename = CITY_DATA[city]
    bspd = pd.read_csv(filename)

    # create month, hour and day_of_week columns
    ## Convert Start Time column to datetime 
    bspd['Start Time'] = pd.to_datetime(bspd['Start Time'])
    # extract information 
    bspd['month'] = bspd['Start Time'].dt.month
    bspd['hour'] = bspd['Start Time'].dt.hour
    bspd['day_of_week'] = bspd['Start Time'].dt.day_name()

    # if specified filter by month
    if month is not None and month !='All': 
        bspd = bspd[bspd['month'] == months_map[month]].reset_index(drop=True)
        

    # if specified filter by day
    if day is not None and day !='All': 
        day = day.lower().title()
        bspd = bspd[bspd['day_of_week'] == day].reset_index(drop=True)
        
    # return dataset
    return bspd


def time_stats(bspd, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        mode_month = bspd['month'].mode()[0]
        print('\nMost common month is {}.'.format(months_map_inverse[mode_month]))

    # display the most common day of week
    if day == 'All':
        mode_day = bspd['day_of_week'].mode()[0]
        print('\nMost common day of the week is {}.'.format(mode_day))

    # display the most common start hour
    mode_hour = bspd['hour'].mode()[0]
    if day == 'All' and month == 'All':
        print('\nMost popular start hour is {} hrs.'.format(mode_hour))
    elif month == 'All':
        print('\nMost popular start hour on {}s is {} hrs.'.format(day, mode_hour))
    else:
        print('\nMost popular start hour on {}s in {} is {} hrs.'.format(day, month, mode_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(bspd):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = bspd['Start Station'].mode()[0]
    print('\nMost common start station is {}.'.format(start_station))

    # display most commonly used end station
    start_station = bspd['End Station'].mode()[0]
    print('\nMost common end station is {}.'.format(start_station))

    # display most frequent combination of start station and end station trip
    ## rank All combinations
    ranking = bspd[['Start Station', 'End Station']].value_counts().sort_values()
    ## display top combination 
    print('\nMost common trip is {} to {}.'.format(ranking.keys()[-1][0], ranking.keys()[-1][1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(bspd):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = bspd['Trip Duration'].sum()
    print('\nIn total the bikes were rented for {} seconds.'.format(total_travel))

    # display mean travel time
    avg_travel = bspd['Trip Duration'].mean()
    print('\nThe average trip took {} seconds.'.format(avg_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_value_counts(series, title):
    """Prints the value counts of a pandas Series in a formatted way."""
    print(f"\n{title}:")
    # Convert the value counts to a formatted string (skipping the first and last lines if desired)
    formatted_counts = '\n'.join(str(series).split('\n')[1:-1])
    print(formatted_counts)


def user_stats(bspd, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types using the helper function
    print_value_counts(bspd['User Type'].value_counts(dropna=False), "User Types and Counts")
    
    # For cities other than Washington, display additional user stats
    if city != 'Washington':
        print_value_counts(bspd['Gender'].value_counts(dropna=False), "Gender Counts")
        
        # Display birth year statistics
        birth_year_mode = int(bspd['Birth Year'].mode()[0])
        birth_year_min = int(bspd['Birth Year'].min())
        birth_year_max = int(bspd['Birth Year'].max())
        print('\nBirth years range from {} to {}. The most common is {}.'.format(birth_year_min, birth_year_max, birth_year_mode))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def indiv_data(bspd):
    """Query user about displaying additional data. If yes, display 5 rows of data and query again."""

    pos = 0
    max_pos = bspd.shape[0]

    # continue looping while still rows left to display
    while pos < max_pos:
        # get user input on whether they'd like to see individual data.
        answer = input("\nWould you like to see 5 rows of the data? Answer 'Yes' to see the data, or anything else to exit. ")
        answer = answer.lower()
        if answer!='yes':
            return
        else:
            res = bspd.iloc[pos:(pos+4), 1:]
            print('\nRows {} to {} (of {} rows):\n'.format(pos, pos+4, max_pos-1))
            print(res)
            # update pos
            pos += 5


def main():
    while True:
        city, month, day = get_filters()
        bspd = load_data(city, month, day)

        time_stats(bspd, month, day)
        station_stats(bspd)
        trip_duration_stats(bspd)
        user_stats(bspd, city)
        indiv_data(bspd)

        restart = input("\nWould you like to restart? Enter 'Yes', or anything else to exit.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
