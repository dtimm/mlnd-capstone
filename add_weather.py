import pandas as pd
import numpy as np
from os.path import isfile
import requests
import json

# get weather data from 2011-01-01 through 2015-12-31 
# and associate it to each Cluster #
MIN_DATE = '2013-08-23'
MAX_DATE = '2015-12-31'

'''
# download weather data if we don't have it
key_file = open('data/api.key', 'r')
wu_key = key_file.readline()
wunderground = 'http://api.wunderground.com/api/{0}/history_{1}/q/{2}.json'
zips = [80230,80219,80211,80249,80222,80203,80239,80204,80231,80219,80206,80227,80205,80207,80202]
for i in xrange(16):
    zip = zips[i]
    if not isfile('data/{0}_weather.csv'.format(zip)):
        f = open('data/{0}_weather.csv'.format(zip), 'a')
        f.write('Date,Cluster,Max TemperatureF,Mean TemperatureF,Min TemperatureF,MeanDew PointF,Max Humidity,Mean Sea Level PressureIn,Mean VisibilityMiles,Mean Wind SpeedMPH,Max Gust SpeedMPH,PrecipitationIn\n')
        for date in pd.date_range(MIN_DATE, MAX_DATE):
            mod_date = date.strftime('%Y%m%d')
            query = wunderground.format(wu_key, mod_date, zip)
            #print query
            datum = pd.read_json(query)['history']['dailysummary']
            #print '{0} temp: {1}'.format(date.strftime('%Y-%m-%d'), datum[0])
            f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n'.format(date.strftime('%Y-%m-%d'), i, datum[0]['maxtempi'], datum[0]['meantempi'], datum[0]['mintempi'], datum[0]['meandewpti'], datum[0]['maxhumidity'], datum[0]['meanpressurei'], datum[0]['meanvisi'], datum[0]['meanwindspdi'], datum[0]['maxwspdi'], datum[0]['precipi']))
        f.close()
'''

# make sure all dates and clusters are represented
all_dates = pd.date_range(MIN_DATE, MAX_DATE)
all_dates = all_dates.to_series().apply(lambda x: x.strftime('%Y-%m-%d'))
all_clusters = range(0,16)

date_clusters = pd.MultiIndex.from_product([all_dates, all_clusters], names=['Date', 'Cluster'])

columns = [ 'all-other-crimes', 'murder','arson','auto-theft',
            'theft-from-motor-vehicle','drug-alcohol','larceny',
            'aggravated-assault','other-crimes-against-persons',
            'robbery','burglary','traffic-accident','white-collar-crime', 'public-disorder']
crime_weather = pd.DataFrame(0.0, index=date_clusters, columns=columns)

weather = pd.read_csv('data/weather.csv')

# format the weather data and drop some columns
weather['Date'] = pd.to_datetime(weather['Date'], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m-%d'))

print weather.columns
weather.drop(weather.columns.tolist()[19:], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[15:18], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[12:14], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[9:11], axis=1, inplace=True)
weather.drop(weather.columns.tolist()[6:8], axis=1, inplace=True)
weather.drop('Max Dew PointF', axis=1, inplace=True)
print weather.columns

# add descriptive time columns
weather['Weekday'] = pd.to_datetime(weather['Date']).apply(lambda x: x.strftime('%w'))
weather['Month'] = pd.to_datetime(weather['Date']).apply(lambda x: x.strftime('%m'))

# clear out-of-bounds dates and set index
weather = weather[weather['Date'] <= MAX_DATE]
weather = weather[weather['Date'] >= MIN_DATE]
weather.set_index(['Date'], inplace=True)
weather.fillna(0.0, inplace=True)

# load crime file, drom 2011 and 2016 because of incomplete data
crime = pd.read_csv('./data/data_clean.csv')
crime = crime[crime['Date'] <= MAX_DATE]
crime = crime[crime['Date'] >= MIN_DATE]

crime.set_index(['Date', 'Cluster'], inplace=True)

crime_weather.update(crime)
crime_weather = crime_weather.combine_first(weather)
#crime_weather = crime_weather.merge(crime_weather, weather, left_index=True, right_index=True, how='left')

crime_weather.to_csv('data/crime_weather.csv')

print 'Done.'