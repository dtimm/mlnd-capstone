import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split, KFold
from sklearn.preprocessing import StandardScaler

import tensorflow as tf

# Create model
def mlp(x, weights, biases):
    # Hidden layer 1, relu activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer 2, relu activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output, linear activation
    out = tf.matmul(layer_2, weights['out']) + biases['out']
    return out

# perform some sort of analysis on the crime_weather.csv data

crime_weather = pd.read_csv('data/crime_weather.csv')

crimes = crime_weather.columns.tolist()[12:]
target = crime_weather[crimes]
crime_weather.drop(crimes, axis=1, inplace=True)
crime_weather.drop('Date', axis=1, inplace=True)
crime_weather.fillna(0.0, inplace=True)

today = []
for i in xrange(1):
    today.append([i, 15, 88, 8, 29.72, 74, 10, 24, 62, 6, 4])

today = pd.DataFrame(today)

X_tr, X_ts, y_tr, y_ts = train_test_split(crime_weather, target, test_size=0.33, random_state=42)

scale = StandardScaler()
scale.fit(X_tr)

X_tr = scale.transform(X_tr)
X_ts = scale.transform(X_ts)
today = scale.transform(today)

#X_tr.reset_index(drop=True)
#y_tr.reset_index(drop=True)
X_tr = pd.DataFrame(X_tr)
y_tr = pd.DataFrame(y_tr)

input_count = len(crime_weather.columns)
hidden1 = 32
hidden2 = 32
output_count = len(crimes)

X = tf.placeholder('float', [None, input_count])
y = tf.placeholder('float', [None, output_count])

weights = {
    'h1': tf.Variable(tf.random_normal([input_count, hidden1])),
    'h2': tf.Variable(tf.random_normal([hidden1, hidden2])),
    'out': tf.Variable(tf.random_normal([hidden2, output_count]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([hidden1])),
    'b2': tf.Variable(tf.random_normal([hidden2])),
    'out': tf.Variable(tf.random_normal([output_count]))
}

predictor = mlp(X, weights, biases)

cost = tf.reduce_mean(tf.square(predictor - y))
optimize = tf.train.GradientDescentOptimizer(learning_rate=0.0001).minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)

    epoch_count = 20
    batch_count = 10
    for i in xrange(epoch_count):
        average_cost = 0.0
        kf = KFold(len(X_tr), n_folds=batch_count)
        for train_index, test_index in kf:
            _, c = sess.run([optimize, cost], feed_dict={   X: X_tr.iloc[train_index],
                                                            y: y_tr.iloc[train_index]})

            average_cost += c
        print 'epoch {0}: {1}'.format(i, average_cost / batch_count)

    correct_prediction = tf.equal(tf.argmax(predictor, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print "Accuracy Train: ", accuracy.eval({X: X_tr, y: y_tr})
    print "Accuracy Test:  ", accuracy.eval({X: X_ts, y: y_ts})
    
    today_predictions = sess.run(predictor, feed_dict={X:today})
    today_predictions = pd.DataFrame(today_predictions, columns=crimes)
    print today_predictions







