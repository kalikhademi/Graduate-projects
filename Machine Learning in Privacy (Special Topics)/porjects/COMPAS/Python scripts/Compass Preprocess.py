#!/usr/bin/env python
# coding: utf-8

# In[1]:



import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib as plt
import os 
import math


# In[2]:


data = pd.read_csv("/Users/kianamac/Dropbox (UFL)/courses/Fall 2019/Machine learning in privacy/porjects/compas-scores_cleaned.csv")


# In[3]:


data.shape


# In[4]:


data.isna().sum()


# In[5]:


data = data[[ 'age', 'c_charge_degree', 'race', 'age_cat', 'score_text', 'sex', 'priors_count','days_b_screening_arrest', 'decile_score', 'is_recid', 'c_jail_in', 'c_jail_out']]


# In[6]:


data.isna().sum()


# In[7]:


data.score_text = data.score_text.fillna(data.score_text.value_counts().idxmax())


# In[8]:


data.isna().sum()


# In[14]:


data.days_b_screening_arrest  = data.days_b_screening_arrest .fillna(data.days_b_screening_arrest .value_counts().idxmax())
data.c_jail_in = data.c_jail_in.fillna(data.c_jail_in.value_counts().idxmax())
data.c_jail_out = data.c_jail_out.fillna(data.c_jail_out.value_counts().idxmax())
data['new_in'] = pd.to_datetime(data['c_jail_in']).dt.date
data['new_out'] = pd.to_datetime(data['c_jail_out']).dt.date
data['LengthOfStay'] = np.absolute((data['new_out'] - data['new_in']).dt.days)
data.head()


# In[18]:


data.to_csv("clean_compass.csv", index=False)


# In[ ]:





# In[ ]:




