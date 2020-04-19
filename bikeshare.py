import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']
WEEK_DAYS = ['monday', 'tuesday', 'wednesday',
             'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Enter a name of the city to analyze (enter "all" to analyze all cities):')

        if city.lower() == 'all':
            break
        elif CITY_DATA.get(city.lower()) == None:
            print('Wrong city name please enter from the list ', [
                  key for key, value in CITY_DATA.items()], ' or type all.')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'Enter a name of the month to analyze (enter "all" to analyze all month):')
        if month.lower() == 'all':
            break
        elif MONTHS.count(month.lower()) == 1:
            break
        else:
            print('Wrong month please enter from the list ',
                  [name for name in MONTHS], ' or type all.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Enter a day of week to analyze (enter "all" to analyze all week days):')
        if day.lower() == 'all':
            break
        elif WEEK_DAYS.count(day.lower()) == 1:
            break
        else:
            print('Wrong day of week please enter from the list ',
                  [name for name in WEEK_DAYS], ' or type all.')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read csv files based on input
    if city.lower() == 'all':
        df_from_each_file = (pd.read_csv(value)
                             for key, value in CITY_DATA.items())
        df = pd.concat(df_from_each_file, ignore_index=True)
    else:
        df = pd.read_csv(CITY_DATA.get(city.lower()))

    # Extract month & day of week to filter data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month.lower())+1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        day_of_week = WEEK_DAYS.index(day.lower())
        df = df[df['day_of_week'] == day_of_week]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', MONTHS[common_month-1].title())

    # TO DO: display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', WEEK_DAYS[common_week_day-1].title())

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_start_hour = df['start_hour'].mode()[0]
    print('Most common start hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip Route'] = '[' + df['Start Station'] + '] to [' + df['End Station'] + ']'
    common_trip_route = df['Trip Route'].mode()[0]
    print('most frequent combination of start station and end station trip:', common_trip_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time:', df["Trip Duration"].agg("sum"))

    # TO DO: display mean travel time
    print('Mean travel time:', df["Trip Duration"].agg("mean"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city != 'washington':
        df[['User Type', 'Gender']] = df[['User Type', 'Gender']].fillna(value='<blank>')
    else:
        df[['User Type']] = df[['User Type']].fillna(value='<blank>')

    # TO DO: Display counts of user types
    user_type_wise_counts = df.groupby(["User Type"])["User Type"].count()
    print('Counts by user types\n', user_type_wise_counts)

    if city != 'washington':
        # TO DO: Display counts of gender
        gender_wise_counts = df.groupby(["Gender"])["Gender"].count()
        print('Counts by user types\n', gender_wise_counts)

        # TO DO: Display earliest, most recent, and most common year of birth
        print('Earliest year of birth:', df["Birth Year"].min())
        print('Most recent year of birth:', df["Birth Year"].max())
        print('Most common year of birth:', df["Birth Year"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start_index = 0
    end_index = df["User Type"].count()
    
    inc = 500
    display_data = input('Do you want to see the first 5 rows of data?')
    is_displayed = False
    disp_start = 0
    disp_end = inc
    while not display_data.lower() == 'no':
        
        if not is_displayed:
            print(df.iloc[disp_start:disp_end])
            is_displayed = True

        if disp_end < end_index:
            display_data = input('Do you want to see the first 5 rows of data?')

            if display_data.lower() == 'yes':
                disp_start = disp_start + inc
                disp_end = disp_end + inc

                if disp_end > end_index:
                    disp_end = end_index

                is_displayed = False
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        #time_stats(df)
        #station_stats(df)
        #trip_duration_stats(df)
        #user_stats(df, city)
        display_data(df)
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
