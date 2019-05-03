#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:55:30 2018

"""

# Code credits: from Chapter 4 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008, 2014

import numpy as np

class mlp:
    """ A Multi-Layer Perceptron"""
    
    def __init__(self,inputs,targets,nhidden,beta=0.01,momentum=0.9,outtype='logistic'):
        """ Constructor """
        # Set up network size
        self.nin = np.shape(inputs)[1]
        self.nout = np.shape(targets)[1]
        self.ndata = np.shape(inputs)[0]
        self.nhidden = nhidden

        self.beta = beta
        self.momentum = momentum
        self.outtype = outtype
    
        # Initialise network
        self.weights1 = (np.random.rand(self.nin+1,self.nhidden)-0.5)*2/np.sqrt(self.nin)
        self.weights2 = (np.random.rand(self.nhidden+1,self.nout)-0.5)*2/np.sqrt(self.nhidden)

    def earlystopping(self,inputs,targets,valid,validtargets,eta,niterations=100):
    
        valid = np.concatenate((valid,-np.ones((np.shape(valid)[0],1))),axis=1)
        
        old_val_error1 = 100002
        old_val_error2 = 100001
        new_val_error = 100000
        
        count = 0
        while (((old_val_error1 - new_val_error) > 0.001) or ((old_val_error2 - old_val_error1)>0.001)):
            count+=1
            self.mlptrain(inputs,targets,eta,niterations)
            old_val_error2 = old_val_error1
            old_val_error1 = new_val_error
            validout = self.mlpfwd(valid)
            new_val_error = 0.5*np.sum((validtargets-validout)**2)
            
        print("Stopped", new_val_error,old_val_error1, old_val_error2)
        return new_val_error
    #this is the part changed from original data to fit the purpose of homework	
    def mlptrain(self,inputs,targets,eta):
         """ Train the thing """
        
         w1_updates = np.zeros_like(self.weights1)
         w2_updates = np.zeros_like(self.weights2)
         #run the forward pass and compute Least Mean square Error to use in backpropagation
         self.outputs = self.mlpfwd(inputs)
         new_val_error = 0.5*np.sum((self.outputs-targets)**2)
         
         #find the gradient for output. The formula is : (labels - desired value)* Activationderivation
         activation_output = self.outputs*(1 - self.outputs)
         gradient_output = (self.outputs-targets)* activation_output
         
         #find the gradient of the hidden layer which is based on the formulda Activation prime of hidden * the gradient of error function
         # with the weights in output layer
         
         activation_output_hidden = self.hidden *(1-self.hidden)
         gradient_hidden = activation_output_hidden *(np.dot(gradient_output,self.weights2.T))
          
         # To compute the weights updates or correlations we use the gradient computed in the previous step dot product with input to that laye
         w1_updates = np.dot(inputs.T,gradient_hidden[:,:-1])
         w2_updates = np.dot(self.hidden.T,gradient_output)
                   
        # updating the weights by  multiplying the learning rate, this is without the momentum version. 
        #The version with momentum is commented below
         self.weights1 -= eta *w1_updates 
         self.weights2 -= eta *w2_updates 

#       self.weights1 -= eta *w1_updates + self.momentum * self.weights1
#       self.weights2 -= eta *w2_updates+ self.momentum* self.weights2   
       
       
         return new_val_error


    def mlpfwd(self,inputs):
        """ Run the network forward """
        
        self.hidden = np.dot(inputs,self.weights1);
        self.hidden = 1.0/(1.0+np.exp(-self.beta*self.hidden))
        self.hidden = np.concatenate((self.hidden,-np.ones((np.shape(inputs)[0],1))),axis=1)
        

        outputs = np.dot(self.hidden,self.weights2);

        # Different types of output neurons
        if self.outtype == 'linear':
        	return outputs
        elif self.outtype == 'logistic':
            return 1.0/(1.0+np.exp(-self.beta*outputs))
        elif self.outtype == 'softmax':
            normalisers = np.sum(np.exp(outputs),axis=1)*np.ones((1,np.shape(outputs)[0]))
            return np.transpose(np.transpose(np.exp(outputs))/normalisers)
        else:
            print("error")
    

    def confmat(self,inputs,targets):
        """Confusion matrix"""

        # Add the inputs that match the bias node
        outputs = self.mlpfwd(inputs)
        nclasses = np.shape(targets)[1]

        if nclasses==1:
            nclasses = 2
            outputs = np.where(outputs>0.5,1,0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(outputs,1)
            targets = np.argmax(targets,1)

        cm = np.zeros((nclasses,nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

        print("Confusion matrix is:")
        print(cm)
        print("Percentage Correct: ",np.trace(cm)/np.sum(cm)*100)

