# mlnd-capstone
Capstone project for Udacity Machine Learning Nano Degree

The crime data is sourced from https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-crime

Weather data is from Weather Underground via a tedious, manual process.

The crimes are broken down into 16 clusters (0.445 silhouette score), grouped
by class of crime, and will have several variables describing date and time.
Each crime entry is paired with the weather conditions that day (or hourly,
if I can get that data for free and in bulk...).

After these pre-processing steps, I hope to analyze these data to find
correlation between sector, weather conditions, time of week, time of day, and
the count of each type of crime occurring.