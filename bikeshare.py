import pandas as pd
import numpy as np
import datetime
import time


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def Input_Check(input_str , input_type):
    while True:
        input_read = input(input_str).lower()
        try:
            if input_read in CITY_DATA and input_type == 1:
                break
            elif input_read in ('january', 'february', 'march', 'april', 'may', 'june', 'all') and input_type == 2:
                break
            elif input_read in ('sunday','monday','tuesday','wednesday','thursday','friday','saturday', 'all') and input_type == 3:
                break
            else:
                if input_type == 1:
                    print('\n Sorry, your input should be same like this ( chicago, new york city , washington ) \n')
                if input_type == 2:
                    print('\n Sorry, your input should be same like this ( january, february, march, april, may, june or all )\n') 
                if input_type == 3:
                    print('\n Sorry, your input should be same like this ( sunday, monday, tuesday, wednesday, thursday, friday, saturday or all )\n')
        except ValueError :
            print('\n Sorry, your answer is wrong.....Please enter again')
    return input_read


def Filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n     Hello! Let\'s Explore some US Bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = Input_Check('input for city (chicago, new york city, washington). \n' , 1)
    # get user input for month (all, january, february, ... , june)
    month = Input_Check('\ninput for month (january, february, march, april, may, june, all ). \n' , 2)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = Input_Check('\ninput for day of week (sunday, monday, tuesday, wednesday, thursday, friday, saturday, all). \n' , 3)
    print('\n                    Loading... Please wait.')
    return city, month, day


def Load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
        
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def stats_of_time(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...Loading.\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_most_common = months[(df['month'].mode()[0])-1]
    print('most common month is: \n',   month_most_common) 

    # TO DO: display the most common day of week
    day_of_week_most_common = df['day_of_week'].mode()[0]
    print('most common day of week is: \n',     day_of_week_most_common) 


    # display the most common start hour
    hour_of_day_most_common = df['hour'].mode()[0]
    print('most common hour of day is: \n',     hour_of_day_most_common) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n' , '*-*'*25)


def stats_of_station(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...Loading.\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_most_common = df['Start Station'].mode()[0]
    print('most common start station is: \n',   start_station_most_common) 

    # display most commonly used end station
    end_station_most_common = df['End Station'].mode()[0]
    print('most common end station is: \n',   end_station_most_common) 

    # display most frequent combination of start station and end station trip
    group_start_to_end =df.groupby(['Start Station','End Station'])
    most_common_trip = group_start_to_end.size().sort_values(ascending = False).head(1)
    print('most common trip from start to end is: \n',   most_common_trip) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*-*'*25)


def stats_of_trip_duration(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...Loading.\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time is: \n',   total_travel_time/120 , 'Hours.')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('average travel time is: \n',   average_travel_time/120 , 'Hours.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*-*'*25)


def user_of_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...Loading.\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_of_each_user_type = df['User Type'].value_counts()
    print('counts of each user type is:\n',   counts_of_each_user_type , 'For this statistic.' )

    if 'Gender' in df:
    # Display counts of gender
        counts_of_each_gender = df['Gender'].value_counts()
        print('counts of each gender is:\n',   counts_of_each_gender , 'For this statistic.\n' )
    # Display earliest, most recent, and most common year of birth
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('most common year of birth is: \n',   most_common_year_of_birth , 'For this statistic.\n' )
        recent_year = df['Birth Year'].max()
        print('recent year is: \n',   recent_year , 'For this statistic.\n' )
        earliest_year = df['Birth Year'].min()
        print('earliest year is: \n',   earliest_year , 'For this statistic.' )
    else:
        print('There is No Data of Gender and Birth Day in Washington City.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*-*'*25)
 

def main():
    while True:
        city, month, day = Filters()
        df = Load_data(city, month, day)
        print('\n        your filters is: City = {} , Month = {} , Day = {} .'.format( city, month, day ))
        print('*-*'*25)
        stats_of_time(df)
        stats_of_station(df)
        stats_of_trip_duration(df)
        user_of_stats(df,city)
        raw_data = input('\n Would you like to see some data for this statistic? Enter yes or any thing.\n')
        while raw_data.lower() == 'yes': 
            pd.set_option('display.max_columns',200)
            lines_of_raw_data = df.sample(5)
            print(lines_of_raw_data)
            raw_data = input('\n Would you like to see some data for this statistic? Enter yes or any thing.\n')

        restart = input('\n Would you like to restart this program? Enter yes or any thing.\n')
        if restart.lower() != 'yes':
            print('Goodbye... see you again.')
            break


if __name__ == "__main__":
	main()
