import pandas as pd 
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import f1_score
import lime
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import tensorflow as tf
from lime.lime_tabular import LimeTabularExplainer
import warnings
warnings.filterwarnings("ignore")

# Importing data
df_asr = pd.read_csv('PatientSummary.csv')
df_comp = pd.read_table('LabSurvival.txt', sep="\t", encoding='utf-16')

# Fix LabFlag
df_comp.LabFlag = ['N' if i == '@' else i for i in df_comp.LabFlag]
df_comp.LabFlag2 = ['N' if i == '@' else i for i in df_comp.LabFlag2]

# Fix Loinc
df_comp['Loinc'] = df_comp['Loinc'].replace('-', '', regex=True).astype(int)

# Remove Facts
df_comp = df_comp.drop(['Facts'], 1)

# Drop prediction column
y = df_comp.Alive
df_comp = df_comp.drop(['Alive'], 1)

df_comp_lr = df_comp

# Replace categorical with values
df_comp_lr.Sex = [1 if i == 'F' else 0 for i in df_comp.Sex]
cat_vars = ['Race', 'Loinc', 'LabFlag', 'LabFlag2', 'LabWeekday', 'LabWeekday2']
df_comp_lr = pd.get_dummies(df_comp_lr, prefix_sep="__", columns=cat_vars)

# Normalize
min_max_scaler = MinMaxScaler()
df_normalized = min_max_scaler.fit_transform(df_comp_lr)
df_normalized = pd.DataFrame(df_normalized)
df_normalized.columns = df_comp_lr.columns.values

# Split data
probs = np.random.randn(df_normalized.shape[0])
x_train = df_normalized[probs < 0.8]
x_test = df_normalized[probs > 0.2]
x_train_orig = df_comp_lr[probs < 0.8]
x_test_orig = df_comp_lr[probs > 0.2]

y_train = y[probs < 0.8]
y_test = y[probs > 0.2]

# Logistic Regression Model
model_lr = LogisticRegression()
model_lr.fit(x_train, y_train)
y_pred_lr = model_lr.predict(x_test)

# Sort function
def sorting(numbers_array):
    vals = [abs(x) for x in numbers_array]
    return np.argsort(vals)

# Print out the results of LR explanations
import matplotlib.pyplot as plt
coefs = model_lr.coef_.reshape(-1).tolist()
ind = sorting(coefs)
plt.bar(np.arange(0,10), coefs[ind[0:10]])
plt.xticks(np.arange(0,10), tuple(x_train.columns[ind[0:10]]), rotation=45)
plt.savefig('medical_lr_explanation.png')
plt.show()
