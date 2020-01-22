import pandas as pd 
import numpy as np
import tensorflow.keras as keras
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")

# output
df_normalized = pd.read_csv('completePreprocessed.csv')
y = pd.read_csv('responses.csv', header = None)
df_normalized = df_normalized.drop(df_normalized.columns[0], axis=1)
y = y.drop(y.columns[0], axis=1)

# Replace NAN
df_normalized = df_normalized.fillna(-1)

# Split data
probs = np.random.randn(df_normalized.shape[0])
x_train = df_normalized[probs < 0.8]
x_test = df_normalized[probs > 0.2]

y_train = y[probs < 0.8]
y_test = y[probs > 0.2]

# Deep Learning Model
# Make model
model_nn = keras.models.Sequential()
model_nn.add(keras.layers.Dense(10, input_dim=np.shape(x_train)[1], activation='relu'))
model_nn.add(keras.layers.Dense(4, activation='relu'))
model_nn.add(keras.layers.Dense(1, activation='sigmoid'))

# compile the keras model
model_nn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model_nn.fit(x_train, y_train, epochs=32, batch_size=10)

# Write to file
model_nn.save_weights('weights.h5')
with open('architecture.json', 'w') as f:
    f.write(model_nn.to_json())
        
# evaluate the keras model
_, accuracy = model_nn.evaluate(x_test, y_test)
print('Accuracy: %.2f' % (accuracy*100))

