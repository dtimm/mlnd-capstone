import pandas as pd
import numpy as np
import requests
import json

# get weather data from 2011-01-01 through 2015-12-31 
# and associate it to each Cluster #

weather = pd.read_csv('./data/80219_2011.csv')
weather = pd.concat([weather, pd.read_csv('./data/80219_2012.csv')])
weather = pd.concat([weather, pd.read_csv('./data/80219_2013.csv')])
weather = pd.concat([weather, pd.read_csv('./data/80219_2014.csv')])
weather = pd.concat([weather, pd.read_csv('./data/80219_2015.csv')])

weather['Date'] = pd.to_datetime(weather['Date'], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m-%d'))

crime = pd.read_csv('./data/data_clean.csv')
crime = crime[crime['Date'] < '2016-01-01']

print crime['all-other-crimes'].max()