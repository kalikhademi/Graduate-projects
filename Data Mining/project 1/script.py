import pandas as pd
import numpy as np
import csv
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
#read the file 

LifeExpect = pd.read_csv("life_expectancy.csv")
labels  = LifeExpect[LifeExpect.columns[-1]]
print(list(LifeExpect))
print(LifeExpect.shape)#print the shape into a tuple of rows and columns 
#drop the last column
LifeExpect = LifeExpect.iloc[:, :-1]

#knn would accept numerical values only so we would drop countries from the data 
LifeExpect = LifeExpect.drop(labels='Country', axis=1)
feature_cols = list(LifeExpect)
uniqueLabels = ['Asia','Africa','Europe','North America','South America']
#divide the data into test and train data 
X_train, X_test, y_train, y_test = train_test_split(LifeExpect, labels, test_size=0.33, random_state=42)
print(X_test.shape)
print(X_train.shape)
print(y_test.shape)
print(y_train.shape)

#cross validattion to find the proper k parameter for k nearest neighbor
accuracy ={}
accuracyList =[]
for k in range(1,21):
	knnModel = KNeighborsClassifier(n_neighbors = k)
	knnModel.fit(X_train,y_train)
	predLabel = knnModel.predict(X_test)
	accuracy[k]= metrics.accuracy_score(y_test,predLabel)
	accuracyList.append(accuracy[k])

#find the maximum accuracy index to find the k valeu
kVlaue = np.argmax(accuracyList)
print("the optimum value of k is:",kVlaue)

Knn = KNeighborsClassifier(n_neighbors = kVlaue)
y_pred = Knn.fit(X_train,y_train).predict(X_test)
FinalAcc = metrics.accuracy_score(y_test,y_pred)
print("the final accuracy of knn is :",FinalAcc)

#naive bayes definition
#first define the gaussian naive object and then fit it with the data
GNB = GaussianNB()
GNBFit = GNB.fit(X_train,y_train)
y_pred_NB = GNBFit.predict(X_test)
FinalAcc_NB = metrics.accuracy_score(y_test,y_pred_NB)
print("the final accuracy of NB is :", FinalAcc_NB)


#decision tree definition
DTree = DecisionTreeClassifier()
DTree = DTree.fit(X_train,y_train)
y_pred_DT = DTree.predict(X_test)
FinalAcc_DT = metrics.accuracy_score(y_test,y_pred_DT)
print("the accuracy of decision tree is :",FinalAcc_DT)

# dot_data = StringIO()
# export_graphviz(DTree, out_file=dot_data,  
#                 filled=True, rounded=True,
#                 special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
# Image(graph.create_png())




