import numpy as np
import matplotlib.pyplot as plt
import math 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from decimal import Decimal
from sklearn.decomposition import PCA

""" ====================================== Generating Multivariate Normal Data with Highly varied variance=============="""
mean=[2,2]
cov=[[0.2,-1.5],[-1.5,20]]
x=np.random.multivariate_normal(mean,cov,500)


""" Centeradize the data by subtracting mean from the original Data """
X_update = np.array([])
X_update_first = x[:,0]- mean[0]
X_update_second = x[:,1]-mean[1]
X_update = np.column_stack((X_update_first , X_update_second))


"""Apply singular decomposition vector on covariance to compute eigen values and eigen vectors"""
cov_mat = np.cov(X_update.T)
print("the original covariance is ", cov_mat)
eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)
#print('\nEigenvalues \n', eigen_vals)
#print('eigen vectors are', eigen_vecs)
eigen_pairs = [(eigen_vals[i], eigen_vecs[:,i]) for i in range(len(eigen_vals))]
eigen_pairs.sort(reverse=True)
#print("the matrix is:", eigen_pairs)
w = np.hstack((eigen_pairs[0][1][:, np.newaxis], eigen_pairs[1][1][:, np.newaxis]))
print('Matrix W:\n', w)

""" Implement PCA on the Centeradize data which is X_update"""
X_pca = X_update.dot(w.T)
print("the covariance after pc is:", np.cov(X_pca.T))
cov_pca = np.cov(X_pca.T)



"""Data whitening"""
Eigen_value_sort = [eigen_pairs[0][0],eigen_pairs[1][0]]
#print(Eigen_value_sort)
D=np.diag(1/(np.sqrt(Eigen_value_sort)))
#print("The matrix of D^ -1/2 is ", D)
w_whitening = np.dot(D,w.T)
cov_inv = np.linalg.inv(cov_mat)
X_white= np.dot(X_update,w_whitening.T)
print("X_white cov is equal to",np.cov(X_white.T))

""" Implmenting the PCA from Scikit Learn to compare with our methods"""
scikit_pca = PCA(n_components = 2)
X_spca = scikit_pca.fit_transform(x)

""" Plotting the different data points"""
plt.scatter(x[:,0], x[:,1], c='b')
plt.title('Original Data')
plt.xlabel('First Feature')
plt.ylabel('Second Feature')
plt.show()
plt.scatter( X_white[:,1],X_white[:,0], c='r')
plt.title('Whitening Data')
plt.xlabel('points')
plt.ylabel('Range')
plt.show()
plt.scatter(X_spca[:,1],X_spca[:,0], c='b')
plt.title('PCA Datascikit learn')
plt.xlabel('points')
plt.ylabel('Range')
plt.show()
plt.scatter( X_pca[:,1], X_pca[:,0], c='g')
plt.title('PCA Data')
plt.xlabel('points')
plt.ylabel('Range')
plt.show()