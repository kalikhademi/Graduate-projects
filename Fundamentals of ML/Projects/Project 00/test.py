import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from scipy import stats
from random import randint
from sklearn.metrics import accuracy_score

"""=================================================== KNN method ====================================================="""

def predict(X_train, Y_train, X_test, k):
    #Create list for distances and k_closest
    distances = []
    k_closest = []
    for i in range(len(X_train)):
        #First we compute the euclidean distance
#        distance = sum(abs(X_test - X_train[i]))
        distance = [test_i - train_i for test_i, train_i in zip(X_test, X_train[i])]
        #Add it to list of distances
        distances.append([distance, i])
    #print("distance appended")
    #Sort the list
    distances = sorted(distances)
   # print('the distances are',distances)
    #Make a list of the k neighbors' targets
   # print("finding the closest ones")
    for i in range(k):
        index = distances[i][1]
        k_closest.append(Y_train[index][1])
    
    #Return most common out of k_closest
    prediction, _ = stats.mode(k_closest)
    return prediction
red_cars =[]
def kNearestNeighbor_Test(X_train, Y_train, X_test, k, test_points):
    #Stores predictions 
    predictions = []

    #Loop over all observations
    for i in range(len(X_test)):
        ith_prediction = predict(X_train, Y_train, X_test[i], k)
        if ith_prediction == 2:
            red_cars.append(test_points[i])
        predictions.append(ith_prediction)
        
    #Remove extra dimension
    predictions = np.squeeze(predictions, axis=2)
    
    return predictions, red_cars
