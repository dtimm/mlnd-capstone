from os.path import isfile
import pandas as pd
import numpy as np
import urllib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def cluster_results(data, preds, centers):
    '''
    Visualizes the PCA-reduced cluster data in two dimensions
    '''

    predictions = pd.DataFrame(preds, columns = ['Cluster'])
    plot_data = pd.concat([predictions, data], axis = 1)

    # Generate the cluster plot
    fig, ax = plt.subplots(figsize = (14,8))

    # Color map
    cmap = cm.get_cmap('viridis')

    # Color the points based on assigned cluster
    for i, cluster in plot_data.groupby('Cluster'):   
        cluster.plot(ax = ax, kind = 'scatter', x = 'GEO_LON', y = 'GEO_LAT', \
                     color = cmap((i)*1.0/(len(centers)-1)), label = 'Cluster %i'%(i), s=30)

    # Plot centers with indicators
    for i, c in enumerate(centers):
        ax.scatter(x = c[0], y = c[1], color = 'white', edgecolors = 'black', \
                   alpha = 1, linewidth = 2, marker = 'o', s=200)
        ax.scatter(x = c[0], y = c[1], marker='$%d$'%(i), alpha = 1, s=100)

    # Set plot title
    ax.set_title("Cluster Learning on Denver Crime Data - Centroids Marked by Number")

# analyze the data to see if we can find some clusters by location and
# by OFFENSE_CATEGORY_ID

# check for crime.csv, download it.
if not isfile('data/crime.csv'):
    urllib.urlretrieve('http://data.denvergov.org/download/gis/crime/csv/crime.csv', 'data/crime.csv')

# load crime data, remove most features.
data = pd.read_csv('./data/crime.csv')
data.drop(['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION',
            'NEIGHBORHOOD_ID','DISTRICT_ID','LAST_OCCURRENCE_DATE','REPORTED_DATE',
            'INCIDENT_ADDRESS','PRECINCT_ID','OFFENSE_TYPE_ID',
            'GEO_X','GEO_Y'], axis=1, inplace=True)

# drop points with no location data or bad location data.
data.dropna(inplace=True)
data.drop(data[data['GEO_LAT'] < 1.0].index, axis=0, inplace=True)
# drop traffic data
#data.drop(data[data['IS_CRIME'] == 0].index, axis=0, inplace=True)
data.drop(['IS_TRAFFIC','IS_CRIME'], axis=1, inplace=True)

# process dates
data['FIRST_OCCURRENCE_DATE'] = pd.to_datetime(data['FIRST_OCCURRENCE_DATE'])

# sparse encode offense categories
data = data.join(pd.get_dummies(data['OFFENSE_CATEGORY_ID']))
data.drop('OFFENSE_CATEGORY_ID', axis=1, inplace=True)

# look at some basic statistics about the data
#print data.describe()
#print data.shape

#from sklearn.decomposition import PCA

# Examine PCA values to see if anything sticks out.
#pca = PCA(copy=True).fit(data[data.columns.tolist()[1:]])
#print np.cumsum(pca.explained_variance_)

'''
crimes = {}
for col_head in data.columns.tolist()[3:]:
	# create a dict with each of the crimes as keys, reindex each from 0
	crimes[col_head] = data[data[col_head] == 1.0][data.columns.tolist()[:3]].copy(deep=False)
	crimes[col_head].reset_index(inplace=True)
	crimes[col_head].drop('index', axis=1, inplace=True)

print crimes.keys()
#plt.scatter(crime['GEO_LAT'], crime['GEO_LON'])
#plt.show()
'''

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#print crime.head()
# drop the crimes and dates from the table and re-index.
#data.drop(data.columns[3:], axis=1, inplace=True)
data.reset_index(inplace=True)
data.drop('index', axis=1, inplace=True)

# we don't need the date here anymore, it's in the crime lists
#data.drop('FIRST_OCCURRENCE_DATE', axis=1, inplace=True)

# determine a good cluster number if there is one
#for i in range(2,30):
clusterer = KMeans(random_state=42, n_clusters=16).fit(data[data.columns.tolist()[1:3]].sample(1000, random_state=42))

preds = clusterer.predict(data[data.columns.tolist()[1:3]])
predictions = pd.DataFrame(preds, columns = ['Cluster'])
data = pd.concat([predictions, data], axis = 1)

data['Date'] = pd.to_datetime(data['FIRST_OCCURRENCE_DATE']).apply(lambda x: x.strftime('%Y-%m-%d'))
data.drop('FIRST_OCCURRENCE_DATE', axis=1, inplace=True)
data.drop('GEO_LAT', axis=1, inplace=True)
data.drop('GEO_LON', axis=1, inplace=True)

aggregater = {}
for col_head in data.columns.tolist()[1:14]:
	aggregater[col_head] = 'sum'

data = data.groupby(['Date', 'Cluster']).agg(aggregater)

#data[col_head] = data.groupby(['Date','Cluster'])[col_head].agg({col_head:'sum'})#.transform('count')

data.to_csv('data/data_clean.csv')
centers = pd.DataFrame(clusterer.cluster_centers_)
centers.to_csv('data/centers.csv')

# Find the cluster centers
#centers = clusterer.cluster_centers_
#print centers
'''
# calculate silhouette scores for each crime
for crime_name, crime in crimes.iteritems():
	# Predict the cluster for each data point
	preds = clusterer.predict(crime[crime.columns.tolist()[1:3]])
	
	# Calculate the mean silhouette coefficient for the number of clusters chosen
	#score = silhouette_score(crime, preds)
	#print crime_name, score

	# Display the results of the clustering from implementation
	#cluster_results(crime, preds, centers)
	#plt.show()

	# add prediction to each data point
	predictions = pd.DataFrame(preds, columns = ['Cluster'])
	crime = pd.concat([predictions, crime], axis = 1)

	crime.to_csv('./data/'+crime_name+'.csv', index=False)
'''

print 'Done.'