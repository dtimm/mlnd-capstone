# mlnd-denver-crime
Capstone project for Udacity Machine Learning Nano Degree

The crime data is sourced from https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-crime

Bulk weather data is from Weather Underground via a tedious, manual process,
and today's and yesterday's weather is pulled using ther wunderground.com API.
Make sure you put your WU API key in the file data/api.key prior to running
analysis.py.

The crimes are broken down into 16 clusters (0.445 silhouette score), grouped
by class of crime, and will have several variables describing date and time.
Each crime entry is paired with the weather conditions that day (or hourly,
if I can get that data for free and in bulk...).

To make this work, run grouping.py to set up the crime data, add_weather.py to
incorporate the weather data, and finally analysis.py to get to end results.