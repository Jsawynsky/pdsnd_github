import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while     loop to handle invalid inputs
    city = ' '
    while city not in CITY_DATA.keys():
        city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()
    if city not in CITY_DATA.keys():
        print('That is not a valid response. Please choose Chicago, New York City, or Washington: ')
    print('You have chosen {} as your city'.format(city.title()))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ' '
    while month not in MONTH_DATA:
        month = input('\nPlease select a month between January and June that you would like to view data from. You can view all months by responding ALL: ').lower()
        if month not in MONTH_DATA:
            print('That is not a valid repsonse. Please pick a month between January and June or pick all') 

    DAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ' '
    while day not in DAY_DATA:
        day = input('\nPlease select the day of the week you would like to see data for. To see all days respond ALL: ').lower()
    if day not in DAY_DATA: 
        print('That is not a valid response. Please respond with a day of the week or all: ') 

    print('-'*40)
# return selections
    return city, month, day 


def load_data(city, month, day):
    """
    :specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    DAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
                                     
    if month != 'all':
        df = df[df['Start Time'].dt.month == MONTH_DATA.index(month)]
                                    
    if day != 'all':
        df= df[df['Start Time'].dt.day_name() == day.title()]
    
    # return the filtered data    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    DAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("\nThe most popular month is: ", MONTH_DATA[df['Start Time'].dt.month.mode()[0]].title())

    # TO DO: display the most common day of week
    print("\nThe most popular day is: ",df['Start Time'].dt.day_name().mode()[0])

    # TO DO: display the most common start hour
    print("\nThe most popular start hour is: ",df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    #Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('\nThe most commonly used end station is: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start and end stations is: ')
    print('Start Station: ', df.groupby(['Start Station','End Station']).size().idxmax()[0])
    print('End Station: ', df.groupby(['Start Station','End Station']).size().idxmax()[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration,60)
    hour, minute = divmod(minute, 60)
    #Finds the average duration
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    hrs, mins = divmod(mins, 60)
    
    # TO DO: display total travel time
    print(f"The total travel time is {hour} hours, {minute} minutes, and {second} seconds.\n")

    # TO DO: display mean travel time
    if mins > 60:
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
      #Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    print('\nThe count of user types is: \n',df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' not in df.columns:
      print('There is no gender information available.') 
    else:
      print('The count of users by gender is: \n',df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
      print('There is no birth year information available')
    else:
      print('\nThe earliest birth year is: ', int(df['Birth Year'].min()))
      print('\nThe most recent birth year is: ', int(df['Birth Year'].max()))
      print('\nThe most common year of birth is: ', int(df['Birth Year'].mode()[0]))      

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Displays 5 rows of data per user request
    """
    start_index = 0
    chunk_size = 5
    acceptable_responses = ['yes', 'no']
    user_input = ''

    while user_input not in acceptable_responses:
        user_input = input('Would you like to see five lines of raw data? (yes/no): ').strip().lower()
        if user_input not in acceptable_responses:
            print ('\nPlease respond with yes or no')
    
    while user_input == 'yes':
        chunk = df.iloc[start_index:start_index + chunk_size]
        print(chunk)          

        start_index += chunk_size
        if start_index < len(df):
            user_input = input('Do you want to see the next 5 items? (yes/no): ').strip().lower()
            while user_input not in acceptable_responses:
                user_input = ('That input is invalid, please select yes or no: ')
    
        else:
            print("No more items to display.")
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()