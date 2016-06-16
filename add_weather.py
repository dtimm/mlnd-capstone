import pandas as pd
import numpy as np
import requests
import json

# get weather data from 2011-01-01 through 2015-12-31 
# and associate it to each Cluster #
MIN_DATE = '2013-01-01'
MAX_DATE = '2015-12-31'

key_file = open('data/api.key', 'r')
wu_key = key_file.readline()
wunderground = 'http://api.wunderground.com/api/{0}/history_{1}/q/{2}.json'
#test = wunderground + '/history_20120101/q/80219.json'
#resp = requests.get(test)

'''
for zip in [80230,80219,80211,80249,80222,80203,80239,80204,
            80231,80219,80206,80227,80205,80207,80202]:
    f = open('data/{0}_weather.csv'.format(zip), 'a')
    for date in pd.date_range(MIN_DATE, MAX_DATE):
        mod_date = date.strftime('%Y%m%d')
        query = wunderground.format(wu_key, mod_date, zip)
        #print query
        datum = pd.read_json(query)['history']['dailysummary']
        #print '{0} temp: {1}'.format(date.strftime('%Y-%m-%d'), datum[0])
        f.write('{0}'.format(datum[0]))
    f.close()
'''

# make sure all dates and clusters are represented
all_dates = pd.date_range(MIN_DATE, MAX_DATE)
all_dates = all_dates.to_series().apply(lambda x: x.strftime('%Y-%m-%d'))
all_clusters = range(0,16)

date_clusters = pd.MultiIndex.from_product([all_dates, all_clusters], names=['Date','Cluster'])

columns = [ 'all-other-crimes', 'murder','arson','auto-theft',
            'theft-from-motor-vehicle','drug-alcohol','larceny',
            'aggravated-assault','other-crimes-against-persons',
            'robbery','burglary','white-collar-crime', 'public-disorder']
crime_weather = pd.DataFrame(0.0, index=date_clusters, columns=columns)

weather = pd.read_csv('data/cluster00_weather.csv')

# format the weather data and drop some columns
weather['Date'] = pd.to_datetime(weather['Date'], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m-%d'))

weather.drop(weather.columns.tolist()[18:], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[15:17], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[9:14], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[4:8], axis=1, inplace=True)

# add descriptive time columns
weather['Weekday'] = pd.to_datetime(weather['Date']).apply(lambda x: x.strftime('%w'))

# add cluster to the weather
#weather['Cluster'] = 0
weather.set_index(['Date'], inplace=True)

# load crime file, drom 2011 and 2016 because of incomplete data
crime = pd.read_csv('./data/data_clean.csv')
crime = crime[crime['Date'] < MAX_DATE]
crime = crime[crime['Date'] >= MIN_DATE]

crime.set_index(['Date', 'Cluster'], inplace=True)

crime_weather.update(crime)
crime_weather = crime_weather.combine_first(weather)
#crime_weather = crime_weather.merge(crime_weather, weather, left_index=True, right_index=True, how='left')

crime_weather.to_csv('data/crime_weather.csv')

print 'Done.'