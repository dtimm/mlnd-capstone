import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Analyze the data to see if we can find some clusters by location and
# and by OFFENSE_CATEGORY_ID

# load crime data, remove most features.
data = pd.read_csv('./data/crime.csv')
data.drop(['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION',
            'NEIGHBORHOOD_ID','DISTRICT_ID','LAST_OCCURRENCE_DATE','REPORTED_DATE',
            'INCIDENT_ADDRESS','PRECINCT_ID','OFFENSE_TYPE_ID',
            'GEO_X','GEO_Y'], axis=1, inplace=True)

# drop points with no location data.
data.drop(data[data['GEO_LAT'] < 1.0].index, axis=0, inplace=True)
# drop traffic data
data.drop(data[data['IS_TRAFFIC'] == 1].index, axis=0, inplace=True)

print data.head()

plt.scatter(data['GEO_LAT'], data['GEO_LON'])
plt.show()