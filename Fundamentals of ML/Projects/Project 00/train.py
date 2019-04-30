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
    distance =0
    for i in range(len(X_train)):
        distance = sum([abs(test_i - train_i) for test_i, train_i in zip(X_test, X_train[i])])
        distances.append([distance, i])
    distances = sorted(distances)
    for i in range(k):
        index = distances[i][1]
        k_closest.append(Y_train[index][1])
    
    #Return most common out of k_closest
    prediction, _ = stats.mode(k_closest)
    return prediction

def kNearestNeighbor_Train(X_train, Y_train, X_test, k, test_points):
    #Stores predictions 
    predictions = []
    red_cars =[]

    #Loop over all observations
    for i in range(len(X_test)):
#        print("the test is:", X_test[i])
        ith_prediction = predict(X_train, Y_train, X_test[i], k)
        if ith_prediction == 2:
            red_cars.append(test_points[i])
        predictions.append(ith_prediction)
    
    #Remove extra dimension
    predictions = np.squeeze(predictions, axis=2)
    
    return predictions, red_cars

     

"""========================================= Cross validation=============================================="""
accuracy_score_k =[]
CV_score = []
def cross_val(training_rgb,gtruth_training_rgb,validation_rgb,Krange, test_points,gtruth_validation_rgb):
    label_values = [row[1] for row in gtruth_validation_rgb ]
    for k in Krange:
        predictions_KNN , red_cars= kNearestNeighbor_Train(training_rgb,gtruth_training_rgb,validation_rgb,k, test_points)
        accuracy_KNN = accuracy_score(label_values,predictions_KNN)
        accuracy_score_k.append(accuracy_KNN)
    CV_score.append(np.mean(accuracy_score_k))
    print("the accuracy is :",accuracy_score_k )
    index = np.argmax(accuracy_score_k)
    optimum_K = Krange[index]
    print("the optimum k is:", optimum_K)
    plt.plot(Krange, accuracy_score_k)
    plt.xlabel('Number of Neighbors K')
    plt.ylabel('Accuracy')
    plt.show()
    
    return optimum_K



