#!/usr/bin/env python
# coding: utf-8

# # 1 - download , 2 - load

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('Churn_Modelling.csv')


# In[3]:


df.head(10)


# # Univariate

# In[4]:


df['Tenure'].plot(kind='hist')
plt.show()


# In[5]:


df['CreditScore'].plot(kind='box')
plt.show()


# # Bivariate

# In[6]:


plt.scatter(df['RowNumber'],df['CreditScore'])


# In[7]:


plt.scatter(df['RowNumber'],df['Balance'])


# # Multi-variate

# In[9]:


import seaborn as sns
sns.pairplot(data = df)


# # Descriptive statistics

# In[10]:


df.info()


# In[11]:


df.describe()


# In[12]:


df.isnull().any()


# # Missing Values

# In[13]:


df.isnull().sum()


# # Find the outliers and replace the outliers

# In[15]:


sns.boxplot(df['Tenure'])


# In[16]:


sns.boxplot(df['Age'])


# In[17]:


sns.boxplot(df['CreditScore'])


# In[18]:


Q1=df['Age'].quantile(0.25)
Q3=df['Age'].quantile(0.75)
IQR=Q3-Q1
whisker_width = 1.5
age_outliers = df[(df['Age'] < Q1 - whisker_width*IQR) | (df['Age'] > Q3 + whisker_width*IQR)]
age_outliers.count()


# In[19]:


lower_whisker = Q1 -(whisker_width*IQR)
upper_whisker = Q3 + (whisker_width*IQR)
df['Age']=np.where(df['Age']>upper_whisker,upper_whisker,np.where(df['Age']<lower_whisker,lower_whisker,df['Age']))


# In[20]:


Q1=df['CreditScore'].quantile(0.25)
Q3=df['CreditScore'].quantile(0.75)
IQR=Q3-Q1
whisker_width = 1.5
credscore_outliers = df[(df['CreditScore'] < Q1 - whisker_width*IQR) | (df['CreditScore'] > Q3 + whisker_width*IQR)]
credscore_outliers.count()


# In[21]:


lower_whisker = Q1 -(whisker_width*IQR)
upper_whisker = Q3 + (whisker_width*IQR)
df['CreditScore']=np.where(df['CreditScore']>upper_whisker,upper_whisker,np.where(df['CreditScore']<lower_whisker,lower_whisker,df['CreditScore']))


# # Check for Categorical columns and perform encoding.
# 

# In[ ]:


from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
df['Geography'] = enc.fit_transform(df['Geography'])
df['Gender'] = enc.fit_transform(df[['Gender']])


# # Split the data into dependent and independent variables.

# In[23]:


X = df.iloc[:,3:-1]


# In[24]:


y = df.iloc[:,-1]


# # Scaling

# In[25]:


from sklearn.preprocessing import StandardScaler
scale = StandardScaler()
X = scale.fit_transform(X)
X


# # Split the data into training and testing

# In[26]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y ,random_state=1, shuffle=True, train_size = 0.75)
X_train.shape, X_test.shape, y_train.shape, y_test.shape


# In[27]:


from sklearn import linear_model
reg = linear_model.LogisticRegression()
reg.fit(X_train, y_train)


# In[28]:


y_pred = reg.predict(X_test)


# In[29]:


from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


# In[ ]:




