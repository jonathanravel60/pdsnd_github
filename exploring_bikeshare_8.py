import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_names = ['chicago', 'new york city', 'washington']
month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_names = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city, allowing for 1 choice of 3 cities. Solves for case and entries not in dataset.
    while True:
        city = input('Please select one of the following cities: Chicago, New York City or Washington.\n').lower()
        if city not in city_names:
            print('Invalid entry, please enter one of the three cities above.')
        else:
            break

    # Gets user input for month, either selection of signle month in dataset or all. Solves for case and entries not in dataset.
    while True:
        month = input('Please select one month from the following, or all: January, February, March, April, May, June, or all.\n').lower()
        if month not in month_names:
            print('Invalid entry, please enter one of the months listed above or all.')
        else:
            break

    # Gets user input for day, either selection of single day in dataset or all. Solves for case and entries not in dataset.
    while True:
        day = input('Please select a day of the week or all: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or all.\n').lower()
        if day not in day_names:
            print('Invalid entry, please enter one of the days listed above or all.')
        else:
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month_names'] = df['Start Time'].dt.month
    df['day_names'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month_names'] == month]

    if day != 'all':
        day_name = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = day_name.index(day) + 1
        df = df[df['day_names'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = df['month_names'].mode()[0]
    print('Most common month:', common_month)

    # Displays the most common day of week
    common_day = df['day_names'].mode()[0]
    print('Most common day of the week:', common_day)

    # Displays the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    start_station = df['Start Station'].mode().values[0]
    print('Most commonly used start station is:', start_station)

    # Displays most commonly used end station
    end_station = df['End Station'].mode().values[0]
    print('Most commonly used end station is:', end_station)

    # Displays most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most combination of start station and end station trip is\n {}'.format((df['combination'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    time_adj = df['Trip Duration'].sum()
    time_adj =float(time_adj)
    day = time_adj // (24 * 3600)
    time_adj = time_adj % (24 * 3600)
    hour = time_adj // 3600
    time_adj %= 3600
    minutes = time_adj // 60
    time_adj %= 60
    seconds = time_adj
    print('Total travel duration in days, hours, minutes and seconds is: %d:%d:%d:%d' % (day, hour, minutes, seconds))

    # Displays mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print('The average trip duration in seconds is:', avg_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of user types:', user_types)

    # Displays counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Number of users of each gender (if applicable):', gender_count)
    else:
        print('Sorry, no data available for selected city')

    # Displays earliest, most recent, and most common year of birth
    # Data includes birthyear prior to 1900; to investigate and possibly filter.
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('The oldest birth year is:', oldest)
        print('The youngest birth year is:', youngest)
        print('The most common birth year is:', most_common)
    else:
        print('Sorry, no data available for selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)
        # Allows viewer to restart to select new combination of variables or quit
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
# Allows viewer to view 5 rows of data, and then 5 more, etc
def raw(df):
    raw = input('\nWould you like to view 5 rows of data? Enter yes or no:\n').lower()
    pd.set_option('display.max_columns',200)
    i = 0
    while raw.lower() == 'yes':
        print(df.iloc[i:i+5])
        i +=5
        raw = input('\nWould you like to view 5 more rows? Enter yes or no:\n').lower()
        if raw.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
