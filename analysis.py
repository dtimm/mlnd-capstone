from os.path import isfile
import datetime
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

# perform some sort of analysis on the crime_weather.csv data

crime_weather = pd.read_csv('data/crime_weather.csv')

crimes = crime_weather.columns.tolist()[12:]
target = crime_weather[crimes]
crime_weather.drop(crimes, axis=1, inplace=True)
crime_weather.drop('Date', axis=1, inplace=True)
crime_weather.fillna(0.0, inplace=True)

do_yesterday = True
yesterday = []

if isfile('data/api.key'):
    key_file = open('data/api.key', 'r')
    wu_key = key_file.readline()
    today_date = datetime.date.today()
    yesterday_date = (today_date - datetime.timedelta(days=1))
    wunderground = 'http://api.wunderground.com/api/{0}/yesterday/q/80249.json'.format(wu_key)
    datum = pd.read_json(wunderground)['history']['dailysummary']

    for i in xrange(16):
        yesterday.append([i, datum[0]['maxwspdi'], datum[0]['maxtempi'], \
        datum[0]['maxhumidity'], datum[0]['meanpressurei'], datum[0]['meantempi'], \
        datum[0]['meanvisi'], datum[0]['meandewpti'], datum[0]['mintempi'], \
        yesterday_date.strftime('%m'), yesterday_date.strftime('%w')])

    yesterday = pd.DataFrame(yesterday)
else:
    do_yesterday = False
    print 'Will not predict crimes from yesterday. Please add a Weather Underground API key to data/api.key to make this prediction.' 

X_tr, X_ts, y_tr, y_ts = train_test_split(crime_weather, target, test_size=0.33, random_state=42)

scale = StandardScaler()
scale.fit(X_tr)

X_tr = scale.transform(X_tr)
X_ts = scale.transform(X_ts)

if do_yesterday:
    yesterday = scale.transform(yesterday)

# perform grid search to optimize parameters
reg = DecisionTreeRegressor(random_state=42)
#params = {}
params = { 
            'max_depth':[2, 5, 7, 10],
            'min_samples_split':[20,30,50],
            'max_features':[None, 2, 4, 8]
         }
gscv = GridSearchCV(reg, params, cv=5)

gscv.fit(X_tr, y_tr)

print gscv.best_estimator_

print 'TR Score: {0}'.format(gscv.score(X_tr, y_tr))
print 'TS Score: {0}'.format(gscv.score(X_ts, y_ts))

if do_yesterday:
    print 'Yesterday: {0}'.format(pd.DataFrame(gscv.predict(yesterday), columns=crimes))
    print 'Forecast: {0}'.format(scale.inverse_transform(yesterday[0]))

#print pd.DataFrame(gscv.predict(X_ts)).describe()
#print pd.DataFrame(y_ts).describe()