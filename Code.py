# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 07:18:23 2019

@author: Ojas A. Ramwala
"""

#NMI

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# Reading the dataset
def read_dataset ():
     df = pd.read_csv ('sonar.csv') # dataframe
     X = df[df.columns[0:60]].values # features
     y = df[df.columns[60]] # label
     
     # Encode the dependent variable
     encoder = LabelEncoder ()
     encoder.fit (y)
     y = encoder.transform (y) # Assigning 0 and 1 to rock and mine or vice versa
     Y = one_hot_encode(y)
     print (X.shape)
     return (X ,y)

# Define the encoder function
def one_hot_encode (labels):
    n_labels = len (labels)
    n_unique_labels = len (np.unique(labels))
    one_hot_encode = np.zeros ((n_labels , n_unique_labels))
    one_hot_encode[np.arange (n_labels),labels] = 1
    return one_hot_encode

# Read the dataset
X , Y = read_dataset()

# Shuffle the dataset to mix up the rows
X , Y = shuffle (X , Y , random_state = 1)

# Convert the dataset into train and test part
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.20, random_state=415)

# Inpect the shape of the training and testing.
print(train_x.shape)
print(train_y.shape)
print(test_x.shape)

# convert the important parameters and variables to work with the tensors
learning_rate = 0.3
training_epochs = 1000
cost_history = np.empty (shape = [1] , dtype = float)
n_dim = X.shape[1] # shape of features - number of columns
#print ("n_dim", n_dim)
n_class = 2 # Rocks and Mines

# Defining the number of hidden layers and number of neurons for each layer
n_hidden_1 = 60
n_hidden_2 = 60
n_hidden_3 = 60
n_hidden_4 = 60

x = tf.placeholder (tf.float32 , [None , n_dim]) # None = Can be any value 
w = tf.Variable (tf.zeros ([n_dim , n_class]))
b = tf.Variable (tf.zeros ([n_class]))
y_ = tf.placeholder (tf.float32 , [None , n_class])

# Define the weights and biases for each layer
weights = {
        'h1' : tf.Variable (tf.truncated_normal ([n_dim , n_hidden_1])),
        'h2' : tf.Variable (tf.truncated_normal ([n_hidden_1 , n_hidden_2])),
        'h3' : tf.Variable (tf.truncated_normal ([n_hidden_2 , n_hidden_3])),
        'h4' : tf.Variable (tf.truncated_normal ([n_hidden_3 , n_hidden_4])),
        'out' : tf.Variable (tf.truncated_normal ([n_hidden_4 , n_class])),
        }
# Outputs random values from a truncated normal distribution -> tf.truncated_normal
biases = {
        'b1' : tf.Variable (tf.truncated_normal([n_hidden_1])),
        'b2' : tf.Variable (tf.truncated_normal([n_hidden_2])),
        'b3' : tf.Variable (tf.truncated_normal([n_hidden_3])),
        'b4' : tf.Variable (tf.truncated_normal([n_hidden_4])),
        'out' : tf.Variable (tf.truncated_normal([n_class])),
        }


# Define the model
def multilayer_perceptron (x , weights , biases):
    
    
    # Hidden layer with RELU activationsd
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)

    # Hidden layer with sigmoid activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.sigmoid(layer_2)

    # Hidden layer with sigmoid activation
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.sigmoid(layer_3)

    # Hidden layer with RELU activation
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.relu(layer_4)

    # Output layer with linear activation
    out_layer = tf.matmul(layer_4, weights['out']) + biases['out']
    return out_layer

# Initialize all variables
init = tf.global_variables_initializer()

saver = tf.train.Saver() # saver object to save our model

# Calling the above defined model
y = multilayer_perceptron (x , weights , biases)

# Define the cost function and the optimizer
cost_function = tf.reduce_mean (tf.nn.softmax_cross_entropy_with_logits (logits = y , labels = y_)) 
#tf.reduce_mean:- Computes the mean of elements across dimensions of a tensor. (deprecated arguments)
training_step = tf.train.GradientDescentOptimizer (learning_rate).minimize (cost_function)

sess = tf.Session()
sess.run (init)

# Calculate the cost and accuracy for each epoch

mse_history = []
accuracy_history = []

for epoch in range(training_epochs):
    sess.run(training_step, feed_dict={x: train_x, y_: train_y})
    cost = sess.run(cost_function, feed_dict={x: train_x, y_: train_y})
    cost_history = np.append(cost_history, cost)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # print("Accuracy: ", (sess.run(accuracy, feed_dict={x: test_x, y_: test_y})))
    pred_y = sess.run(y, feed_dict={x: test_x})
    mse = tf.reduce_mean(tf.square(pred_y - test_y))
    mse_ = sess.run(mse)
    mse_history.append(mse_)
    accuracy = (sess.run(accuracy, feed_dict={x: train_x, y_: train_y}))
    accuracy_history.append(accuracy)

    print('epoch : ', epoch, ' - ', 'cost: ', cost, " - MSE: ", mse_, "- Train Accuracy: ", accuracy)

# Plot mse and accuracy graph

plt.plot(mse_history, 'r')
plt.show()
plt.plot(accuracy_history)
plt.show()

# Print the final accuracy

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("Test Accuracy: ", (sess.run(accuracy, feed_dict={x: test_x, y_: test_y})))

# Print the final mean square error

pred_y = sess.run(y, feed_dict={x: test_x})
mse = tf.reduce_mean(tf.square(pred_y - test_y))
print("MSE: %.4f" % sess.run(mse))



        
   
    
    
    
    
     
     
