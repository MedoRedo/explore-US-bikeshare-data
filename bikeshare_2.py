import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please, enter the city name (chicago, new york city, washington)\n').lower()
        if city in {'chicago', 'new york city', 'washington'}:
            break
    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Which month? (all, january, february, ... , june)\n').lower()
        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Which day? (all, monday, tuesday, ... sunday)\n').lower()
        if day in days:
            break
        
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    path = f'Data/{CITY_DATA[city]}'
    df = pd.read_csv(path)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Common Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    
    print('Most Common Day of the Week:', popular_day)

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
        
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Common Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Common End Station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    popular_combination = (df['Start Station']+' => '+df['End Station']).mode()[0]
    
    print('Most Frequent Combination of Start Station and End Station:', popular_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Traval Time:', total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    
    print('Mean Travel Time:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, is_washington):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_type_counts)
    if not is_washington:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()

        print('\nCounts of gender:')
        print(gender_counts)
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('\nEarliest year of birth:', earliest_year)
        
        most_recent_year = df['Birth Year'].max()
        print('Most recent year of birth:', most_recent_year)
        
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year of birth:', most_common_year)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, start):
    """Displays individual trip data."""
    n = df.shape[0]
    last = start+5
    while start < last and start < n:
        print(df.iloc[start, 1:],'\n')
        start += 1

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city == 'washington')
        
        start = 0
        while True:
            display_raw_data = input('\nWould you like to view individual trip data? Type yes or no.\n')
            if display_raw_data.lower() == 'yes':
                raw_data(df, start)
                start += 5
            else:
                break

            if start >= df.shape[0]:
                print('\nNo more raw data to display.')
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
