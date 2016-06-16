import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

# perform some sort of analysis on the crime_weather.csv data

crime_weather = pd.read_csv('data/crime_weather.csv')
target = crime_weather['all-other-crimes']

crimes = crime_weather.columns.tolist()[12:]
crime_weather.drop(crimes, axis=1, inplace=True)
crime_weather.drop('Date', axis=1, inplace=True)
crime_weather.fillna(0.0, inplace=True)

today = []
for i in xrange(16):
    today.append([i, 15, 88, 8, 29.72, 74, 10, 24, 62, 6, 4])

today = pd.DataFrame(today)

X_tr, X_ts, y_tr, y_ts = train_test_split(crime_weather, target, test_size=0.33, random_state=42)

scale = StandardScaler()
scale.fit(X_tr)

X_tr = scale.transform(X_tr)
X_ts = scale.transform(X_ts)
today = scale.transform(today)

#reg = BayesianRidge()
#params = {}
reg = Perceptron(class_weight='balanced')
params = {'alpha':[1e-3,1e-2,1e-1,1.0], 'penalty':[None,'l1','l2','elasticnet']}
gscv = GridSearchCV(reg, params)

gscv.fit(X_tr, y_tr)
print gscv.best_estimator_

print gscv.predict(today)
predictions = gscv.predict(X_ts)
print pd.Series(y_ts).describe(), pd.Series(predictions).describe()
#print scale.inverse_transform(X_ts[predictions == 0])
print gscv.score(X_tr, y_tr), gscv.score(X_ts, y_ts)