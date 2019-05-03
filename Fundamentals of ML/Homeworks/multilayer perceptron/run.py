"""
author: Kiana Alikhademi
Desc: to investigate the multilayer percetron on given data and documen the perfromance regarding parameters which impact it most
"""
import numpy as np
import mlp
import matplotlib.pyplot as plt


""" import the data"""
data = np.load('dataSet.npy')

labels= data[:,data.shape[1]-1]
data_only = data[:,0:data.shape[1]-1]

"""Set up Neural Network"""
hidden_layers = 9
data_in = data_only
target_in = (labels.reshape(1,np.shape(data_in)[0])).T
NN = mlp.mlp(data_in,target_in,hidden_layers)

#Analyze Neural Network Performance
""" investigating the impact of different numbers of itterations"""
Error_list=[]
error = 0
data_in = np.concatenate((data_in,-np.ones((data_in.shape[0],1))),axis=1)
niterations = np.arange(0,1000000)
for i in range(1000000):
    error = NN.mlptrain(data_in,target_in,0.01)
    Error_list.append(error)

NN.confmat(data_in,target_in)
plt.plot(np.arange(0,1000000),Error_list)
plt.ylabel('Error')
plt.xlabel('Iterations')
plt.show()

""" investigating the impact of different number of hidden nodes"""
Error_list1=[]
hidden_nodes= [3,5,7,9]
for nodes in hidden_nodes:
   NN = mlp.mlp(data_in,target_in,nodes)
   error = NN.mlptrain(data_in,target_in,1)
   Error_list1.append(error)
   
#NN.confmat(data_in,target_in)

plt.plot(hidden_nodes,Error_list1)
plt.ylabel('Error')
plt.xlabel('hidden nodes')
plt.show()

""" investigating the impact of different learning rates """
Error_list2=[]   
learning_rates =[0.001,0.01,0.1,0.5,1]
for rates in learning_rates:
   for i in range(100000):
       error = NN.mlptrain(data_in,target_in,rates)
   Error_list2.append(error)
   

NN.confmat(data_in,target_in)
plt.plot(learning_rates,Error_list2)
plt.ylabel('Error')
plt.xlabel('learning parameters')
plt.show()
