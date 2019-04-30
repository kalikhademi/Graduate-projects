# project01-ml-is-fun
project01-ml-is-fun created by GitHub Classroom

**Dependencies**
Install Opencv software in the environment. This is necessary to convert the binary images into contour images. The current implementation is tested under Opencv 3.4.2 which could be downloaded through the following link:
https://opencv.org/releases.html



There are six main files associated with this project: classification.py, feature_extraction.py, findContours.py, 
normalization.py, train.py, and test.py. The only file that requires running is test.py, all other desired functionality from 
the previous files mentioned will be imported and used appropriately. While running this code it is essential to include a 
folder named "Traning_Images" without the quotation marks to store all of the images for testing after normalization. This 
folder is used to prevent clutter within the directory, but this can also be changed within the normalization.py file. However,
if the directory is changed it will also need to be changed in normalization.py.

This group is participating in the extra credit opportunity; therefore, to run the program the command line will require 4 
arguments instead of the initial 3 described through class communication. To run the model for the extra credit you must type,
**python test.py inData.npy out extra**. The inData.npy argument is the testing data file to be passed, out is the desired file name for the prediction lables, and extra will denote the use of the extra credit model to use. To run the model to classify a's and b's 
please type **python test.py inData.npy out ab**. All of the argument meanings are the same except for the last argument ab, which denotes the use of the model for a and b testing.


**Note:** The A-Z Handwritten Alphabets dataset, which consisted of all uppercase letters A-Z, was used in the training process for classifying unknown characters/images. This dataset was obtained through Kaggle (link: https://www.kaggle.com/sachinpatel21/csv-to-images/data). The code provided was used to convert the csv file to png images. In addition, the researchers also handwrote the lowercase letters e-g and l-z to use in the training process for classifying unknown characters/images. These datasets can be accessed in the repository - extra_data.npy & extra_labels.npy for the Kaggle dataset and extra_data_1.npy & extra_labels_1.npy for the lowercase letters e-g and l-z.
