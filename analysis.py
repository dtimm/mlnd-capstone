import pandas as pd
import numpy as np
import matplotlib.pylab as plt

from sklearn.cross_validation import train_test_split
from sklearn.svm import SVR
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler

# perform some sort of analysis on the crime_weather.csv data

crime_weather = pd.read_csv('data/crime_weather.csv')
target = crime_weather['all-other-crimes']
crime_weather.drop(crime_weather.columns.tolist()[9:], axis=1, inplace=True)
crime_weather.drop('Date', axis=1, inplace=True)
'''
crime_weather.drop('Mean VisibilityMiles', axis=1, inplace=True)
crime_weather.drop('Mean Wind SpeedMPH', axis=1, inplace=True)
crime_weather.drop('Min TemperatureF', axis=1, inplace=True)
crime_weather.drop('Mean TemperatureF', axis=1, inplace=True)
crime_weather.drop('Mean Humidity', axis=1, inplace=True)
crime_weather.drop('Max TemperatureF', axis=1, inplace=True)
'''

print crime_weather.columns

X_tr, X_ts, y_tr, y_ts = train_test_split(crime_weather, target, test_size=0.3, random_state=42)

scale = StandardScaler()
scale.fit(X_tr)

X_tr = scale.transform(X_tr)
X_ts = scale.transform(X_ts)

reg = SVR(max_iter=5000)
params = {'C':[0.1, 1.0, 5.0, 10.0], 'kernel':['poly'], 'coef0':[0.0, 0.01, 0.1, 1.0]}
gscv = GridSearchCV(reg, params)

gscv.fit(X_tr, y_tr)
print gscv.best_estimator_ 

predictions = gscv.predict(X_ts)
print np.max(target), np.max(predictions)
print predictions[:15]
print gscv.score(X_tr, y_tr), gscv.score(X_ts, y_ts)