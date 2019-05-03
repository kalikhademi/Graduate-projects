# -*- coding: utf-8 -*-
"""
Author: Kiana Alikhademi
Desc:   two-layer perceptron implmentation
If you want to use it please give the proper reference.   
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split,KFold
from scipy import stats
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



""" reading the data"""
first_data = np.load('dataset1.npy')
second_data = np.load('dataset2.npy')
third_data = np.load('dataset3.npy')


first_labels= first_data[:,first_data.shape[1]-1]
first_data = first_data[:,0:first_data.shape[1]-1]
second_labels= second_data[:,second_data.shape[1]-1]
second_data = second_data[:,0:second_data.shape[1]-1]
third_labels= third_data[:,third_data.shape[1]-1]
third_data = third_data[:,0:third_data.shape[1]-1]

"""  activation functions """

def sigmoid_severe(x):
    if x > 0:
        result = 1
    else:
        result = 0
    return result
def softmax(A):  
    expA = np.exp(A)
    #print(expA)
    return expA / expA.sum()
def Relu(x):
    return np.maximum(x,0)

def plotLine(weights, range):
    x = np.array(range)
    plt.plot(x,weights[1]*x+weights[0])
def sigmoid(x):  
    return 1/(1+np.exp(-x))
"""define a function for two layer perceptron by passing the data and weights """
"""============================================== first dataset================================================="""
""" the first option is x1 =0.5 and x1=1.5 lines to discriminate and the second example is x2 = 0.5 and x2 =1.5"""
#w1 =np.array([2,0])
#b1 = -1 
#w2 = np.array([2,0])
#b2 = -3
#w3 = np.array([2,-2])
#b3 = -1
#
#predicted_label =np.array([])
#hidden_values =np.array([])
## first phase
#for i in range(first_data.shape[0]):
#    phase 1 started here
#    hidden_values =np.array([])
#    hidden_one = np.dot(first_data[i],w1) + b1
#    hidden_two = np.dot(first_data[i],w2) +b2
#    output_one = sigmoid_severe(hidden_one)
#    phase 2
#    hidden_values= np.append(hidden_values,output_one )
#    output_two = sigmoid_severe(hidden_two)
#    hidden_values = np.append(hidden_values, output_two)
#    output_value = np.dot(w3.T, hidden_values) + b3
#    label = sigmoid_severe(output_value)
#    predicted_label= np.append(predicted_label, label)
#     
#    
#print (first_labels)
#print(predicted_label)  
#accuracy =  accuracy_score(first_labels, predicted_label)
#print(accuracy*100)
#
#plotLine([0.5,1,0],[-0.5,2.5])
#plotLine([1.5,1,0],[-0.5,2.5])
##plotLine([-1,-4,5],[-1.5,1.5])
#plt.scatter(first_data[:,0],first_data[:,1], c=predicted_label, linewidth=0)
#plt.show()

"""=====================================================================second dataset==========================================="""
""" first example with four neurons in the hidden layer"""
#w1 = np.array([2,0])
#w2 = np.array([2,0])
#w3 = np.array([2,10])
#w4_new = np.array([0,10])
#w4 = np.array([1,1,0,0])
#w5 =np.array([0,1,1,0])
#w6 = np.array([1,0,-1,0])
#
#
#b1 = -1
#b2 = 1
#b3 = -4
#b4_new = 4
#b4 =-1
#b5 = -1
#b6 = 0
#output_values =[]
#predicted_label_second = np.array([])
#for i in range(second_data.shape[0]):
#
#    hidden_values =np.array([])
# #   phase 1
#    hidden_one = np.dot(second_data[i],w1) + b1
#    hidden_two = np.dot(second_data[i],w2) +b2
#    hidden_third = np.dot(second_data[i],w3)+ b3
#    hidden_fourth = np.dot(second_data[i],w4_new)+b4_new
#    #fisrt phase activation function and storing the input for the next layer
#    output_one = sigmoid(hidden_one)
#    output_two = sigmoid(hidden_two)
#    output_three= sigmoid(hidden_third)
#    output_forth = sigmoid(hidden_fourth)
#    hidden_values = np.append(hidden_values, output_one)
#    hidden_values = np.append(hidden_values, output_two)
#    hidden_values = np.append(hidden_values, output_three)
#    hidden_values = np.append(hidden_values, output_forth)
#    
#    #phase 2 adder function with the output of previous round
#    hidden_second_one = np.dot(w4.T, hidden_values) + b4
#    hidden_second_two = np.dot(hidden_values,w5) + b5
#    hidden_second_three = np.dot(hidden_values,w6) + b6
#    
#    output_layer = [hidden_second_three, hidden_second_two, hidden_second_one]
#    output_result = softmax(output_layer)
#    label = np.argmax(output_layer)
#    predicted_label_second= np.append(predicted_label_second, label)
#      
#accuracy =  accuracy_score(second_labels, predicted_label_second)
#print(accuracy*100)
""" second examples with three neurons in the hidden layer  """
#w1 = np.array([-4,5])
#w2 = np.array([1,21])
#w3 = np.array([-1,1])
#w4 = np.array([1,-1,1])
#w5 =np.array([1,-2,2])
#w6 = np.array([4,5,0])
#b1 = -1
#b2 = -1
#b3 = -1
#b4 =-4
#b5 = -2
#b6 = 0
#output_values =[]
#hidden_nodes = 2
#output_nodes = 3
#predicted_label_second = np.array([])

#
#for i in range(second_data.shape[0]):
#
#    hidden_values =np.array([])
#    output_layer = np.array([])
#    output_values = np.array([])
#    #phase 1
#    hidden_one = np.dot(second_data[i],w1) + b1
#    hidden_two = np.dot(second_data[i],w2) +b2
#    hidden_third = np.dot(second_data[i],w3)+ b3
#    #first phase activation
#    output_one = sigmoid(hidden_one)
#    output_two = sigmoid(hidden_two)
#    output_three= sigmoid(hidden_third)
#    hidden_values = np.append(hidden_values, output_one)
#    hidden_values = np.append(hidden_values, output_two)
#    hidden_values = np.append(hidden_values, output_three)
#    
#    hidden_second_one = np.dot(w4.T, hidden_values) + b4
#    hidden_second_two = np.dot(w5.T, hidden_values) + b5
#    hidden_second_three = np.dot(w6.T, hidden_values) + b6
#    
#    #phase 2
#    output_layer =[hidden_second_one,hidden_second_two, hidden_second_three]
#    output_result = softmax(output_layer)
#    label = np.argmax(output_layer)
#    predicted_label_second= np.append(predicted_label_second, label)
#
#accuracy =  accuracy_score(second_labels, predicted_label_second)
#print(accuracy*100)
#plotLine([0.5,1,0],[-1.5,1.5])
#plotLine([-0.5,1,0],[-1.5,1.5])
#plotLine([0.4,0,1],[-1.5,1.5])
#plotLine([-0.4,0,1],[-1.5,1.5])
#plt.scatter(second_data[:,0],second_data[:,1], c=predicted_label_second, linewidth=0)
#plt.show()      
#print(second_data[np.where((np.round(second_data[:,0],1) == -1))])
"""==============================================================third dataset====================================================="""
w1 = np.array([2,0])
w2 = np.array([4,1])
w3 = np.array([2,0])
b1 = -7
b2 = -13
b3 = -3

# second phase of hidden layer 
w4 = np.array([0,-2,2])
w5 = np.array([1,2,1])
b4 = -1
b5 = -3
w6 = np.array([2,2])
b6 = -1
predicted_label_third = np.array([])
for i in range(third_data.shape[0]):
    hidden_values =np.array([])
    second_hidden_value = np.array([])
    hidden_one = np.dot(third_data[i],w1) + b1
    hidden_two = np.dot(third_data[i],w2) +b2
    hidden_three = np.dot(third_data[i], w3)+ b3
    output_one = sigmoid_severe(hidden_one)
    output_two = sigmoid_severe(hidden_two)
    output_three = sigmoid_severe(hidden_three)
    hidden_values= np.append(hidden_values,output_one )
    hidden_values = np.append(hidden_values, output_two)
    hidden_values = np.append(hidden_values, output_three)
    hidden_forth = np.dot(w4.T, hidden_values) + b4
    hidden_fifth = np.dot(hidden_values,w5)+b5
    output_forth = Relu(hidden_forth)
    output_fifth = Relu(hidden_fifth)
    second_hidden_value = np.append(second_hidden_value, output_forth)
    second_hidden_value = np.append(second_hidden_value, output_fifth)
    final_output = np.dot(second_hidden_value, w6)+b6
    label = sigmoid_severe(final_output)
    predicted_label_third= np.append(predicted_label_third, label)
    
accuracy =  accuracy_score(third_labels, predicted_label_third)
print(accuracy*100)


#plotLine([4.5,2,0],[0.5,4.5])
#plotLine([4,-2,1],[0.5,4.5])
#plotLine([0.75,-1.5,1],[0.5,4.5])
plt.ylim(-1, 6)
plt.scatter(third_data[:,0],third_data[:,1], c=predicted_label_third, linewidth=0)

plt.show()

""" plot the results"""
