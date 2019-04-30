
""" =======================  Import dependencies ========================== """

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.close('all') #close any open plots

"""
===============================================================================
===============================================================================
============================ Question 1 =======================================
===============================================================================
===============================================================================
"""
""" ======================  Function definitions ========================== """

def generateUniformData(N, l, u, gVar):
    step = (u-l)/(N);
    x = np.arange(l+step/2,u+step/2,step)
    e = np.random.normal(0,gVar,N)
    t = np.sinc(x) + e
    return x,t

def plotData(x1,t1,x2,t2,x3=None,t3=None,legend=[]):
    '''plotData(x1,t1,x2,t2,x3=None,t3=None,legend=[]): Generate a plot of the 
       training data, the true function, and the estimated function'''
    p1 = plt.plot(x1, t1, 'bo') #plot training data
    p2 = plt.plot(x2, t2, 'g') #plot true value
    if(x3 is not None):
        p3 = plt.plot(x3, t3, 'r') #plot training data

    #add title, legend and axes labels
    plt.ylabel('t') #label x and y axes
    plt.xlabel('x')
    
    if(x3 is None):
        plt.legend((p1[0],p2[0]),legend)
    else:
        plt.legend((p1[0],p2[0],p3[0]),legend)
        
def fitdata(x,t,M):
    #generate the matrix X of the polynomials and use the equation we found in the class to find the proper ws. 
    X = np.array([x**m for m in range(M+1)]).T
    w = np.linalg.inv(X.T@X)@X.T@t
    return w

def rsme_estimate(X,Y):
    #this function is computing the root mean square error between two array which passed to it as X and Y.
    result = sum((X-Y)**2)/len(X)
    return np.sqrt(result)

""" ======================  Variable Declaration ========================== """
l = 0 #lower bound on x
u = 10 #upper bound on x
N = 78 #number of samples to generate
gVar = 0.2 #variance of error distribution
test_error_rsm = np.array([])#array to hold testing set rsm error
train_error_rsm = np.array([])#array to hold training set rsm error
Test_data_size = 200
erms_test = 0
erms_train = 0
step = (l-u)/N
M_index =0

""" =======================  Generate Training Data ======================= """

data_uniform  = np.array(generateUniformData(N, l, u, gVar)).T
    
x1 = data_uniform[:,0]
t1 = data_uniform[:,1]
x2 = np.arange(l,u,0.001)  #get equally spaced points in the xrange
t2 = np.sinc(x2) #compute the true function value
""" ======================== Generate Test Data =========================== """
    
    
"""This is where you should generate a validation testing data set.  This 
    should be generated with different parameters than the training data!   """

test_data  = np.array(generateUniformData(Test_data_size, l, u, gVar)).T   
x_test = test_data[:,0]
t_test = test_data[:,1]    
print("this is the test data:", x_test)
print("this is the true value of test data:", t_test)
  
          
""" ========================  Train the Model and test on the validation test ============================= """
for M_index  in range(0,10):  
    w_weights = fitdata(x1,t1,M_index) 
    """ train the training data on w and find the errors"""
    X = np.array([x1**m for m in range(w_weights.size)]).T
    t3 = X@w_weights
    #append the computed error for training data to a numpy array
    train_error_rsm= np.append(train_error_rsm, rsme_estimate(t1, t3))
    X_test = np.array([x_test**m for m in range(w_weights.size)]).T
    estimated_value = X_test@w_weights #compute the predicted value
    #append the computed error for testing data to a numpy array
    test_error_rsm = np.append(test_error_rsm, rsme_estimate(t_test, estimated_value))

"""============================= Plotting and printing ================================="""
#these printing functions were for the purpose of the development
#print("the w is:",w_weights)
#print("this is the estimated data:", estimated_value)
#print(" the train error", train_error_rsm)
#print(" the test error", test_error_rsm)
plt.plot(train_error_rsm, marker ='o',color ='b', label='Training set error')
plt.plot(test_error_rsm,marker ='o',color ='r', label='Testing set error')
plt.title("Polynomial fitting results")
plt.xlabel("M")
plt.ylabel("Root Mean Square Error")
plt.legend(loc='upper right')
"""
===============================================================================
===============================================================================
============================ Question 2 =======================================
===============================================================================
===============================================================================
======================  Variable Declaration ========================== """

trueMu = 4
trueVar = 2
#Initial prior distribution mean and variance
priorMu = 8
priorVar = 4
numDraws = 200
 #Number of draws from the true distribution
"""========================== Plot the true distribution =================="""
#plot true Gaussian function
step = 0.1
l = -20
u = 20
x = np.arange(l+step/2,u+step/2,step)
Draws = []
plt.subplot(121)
plt.plot(x, norm(trueMu,trueVar).pdf(x), color='b', label='True Normal Distribution')
plt.plot(x, norm(priorMu,priorVar).pdf(x), color='r', label= 'Prior Normal Distribution')
plt.title('Before Drawing numbers')
plt.legend(loc='upper right')
for draw in range(numDraws+1):
    Draws.append(np.random.normal(trueVar,trueMu,1)[0])
    #print(DrawResult)
    print('Frequentist/Maximum Likelihood Probability of Draws:' + str(sum(Draws)/len(Draws)))
    print('Bayesian/MAP Probability of Draws:' + str((trueVar**2)/(len(Draws)*priorVar**2+trueVar**2)*priorMu+len(Draws)*priorVar**2/(len(Draws)*priorVar**2+trueVar**2)*sum(Draws)/len(Draws)) )
    priorMu = (trueVar**2)/(len(Draws)*priorVar**2+trueVar**2)*priorMu+len(Draws)*priorVar**2/(len(Draws)*priorVar**2+trueVar**2)*sum(Draws)/len(Draws)
    priorVar = (priorVar*trueVar)**2 /((len(Draws)* priorVar**2)+ trueVar**2)
    print("The prior Mu is :", str(priorMu)+"after "+ str(draw)+ " draws")
    print("The prior Var is :"+ str(priorVar) +"after "+ str(draw)+ " draws")
    plt.figure()
    plt.plot(x, norm(trueMu,trueVar).pdf(x), color='b', label='True Normal Distribution')
    plt.plot(x, norm(priorMu,priorVar).pdf(x), color='r', label= 'Prior Normal Distribution')
    plt.title('After Drawing numbers')
    plt.legend(loc='upper right')

 