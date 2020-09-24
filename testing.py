

import pandas as pd
import nltk
import numpy as np
import datetime
import re
from functools import reduce  # For merging aggrated data frames together

from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.utils.tests.test_pprint import CountVectorizer
from nltk.corpus import stopwords

nltk.download('stopwords')

filename_1 = input("training filename:")
filename_2 = input("filename:")
filename_3 = input("filename:")
filename_4 = input("filename:")


data_1 = pd.read_csv(filename_1)
data_2 = pd.read_csv(filename_2)
data_3 = pd.read_csv(filename_3)
data_4 = pd.read_csv(filename_4)


datasets = [data_2, data_3, data_4]

print(data_1.keys())

#prepare training set

f_data = pd.DataFrame()
f_data_1 = pd.DataFrame()

train_data = pd.DataFrame()
train_data['year'] = data_1[' news_date'].str[-4:]

data_new = data_1[' news_date'].str.split(" ", n= 3, expand= True)
train_data['month'] = data_new[0]
t_new_day = data_new[1].str.split("|", n=2, expand= True)
train_data['day'] = t_new_day[0].fillna(0).astype(int)
train_data['day'] = t_new_day[0].fillna(0).astype(str)
#train_data['titles'] = data_1['news_title']
#concatenate all datasets per sport type
result = pd.concat(datasets)
#make year its own column
result['yr'] = result[' news_date'].str[-4:]

new = result[' news_date'].str.split(" ", n= 3, expand= True)
#fix month
result['month'] = new[0]
d: {str, int} = {'Jan': 1, 'January': 1, 'Feb': 2, 'February': 2, 'Mar': 3, 'March': 3, 'Apr': 4, 'April': 4, 'May': 5, 'Jun': 6, 'June': 6, 'July': 7, 'Jul': 7, 'Aug': 8, 'August': 8, 'Sep': 9, 'September': 9, 'Oct': 10, 'October': 10, 'Nov': 11, 'November': 11, 'Dec': 12, 'December': 12}
result['month'] = result['month'].map(d).fillna(0)
result['month'] = result['month'].astype(int)
result['month'] = result['month'].astype(str)
new_day = new[1].str.split("|", n=2, expand= True)
result['day'] = new_day[0].fillna(0).astype(int)
result['day'] = new_day[0].fillna(0).astype(str)

f_data['date'] = result['yr']+result['month']+result['day']
print(f_data['date'])

f_data['date'] = pd.to_datetime(f_data['date'], format='%Y%m%d')
result['weekday_weekend'] = f_data['date'].dt.dayofweek.fillna(0).astype(int)
result['weekday_weekend'] = result['weekday_weekend'].astype(str)

result['year'] = f_data['date'].dt.year.fillna(0).astype(int)
result['date'] = f_data['date'].astype(str)

#set month and the date to be in same format in training set
train_data['month'] = train_data['month'].map(d).fillna(0)
train_data['month'] = train_data['month'].astype(int)
train_data['month'] = train_data['month'].astype(str)

f_data_1['date'] = train_data['year']+train_data['month']+train_data['day']
f_data_1['date'] = pd.to_datetime(f_data_1['date'], format='%Y%m%d')
f_data_1['year'] = f_data_1['date'].dt.year.fillna(0).astype(int)
train_data['weekday_weekend'] = f_data_1['date'].dt.dayofweek.fillna(0).astype(int)
train_data['weekday_weekend'] = train_data['weekday_weekend'].astype(str)

#train_data['date'] = train_data['date'].astype(str)

data_yr = np.asarray(train_data['year'])

print(result.head())

top_N = 50
train_a = result['news_title'].str.lower().str.cat(sep=' ' or '|')

train_words = nltk.tokenize.word_tokenize(train_a)
train_words = [w for w in train_words if w not in stopwords.words("english")]
for i in range(len(train_words)):
    train_words[i] = re.sub(r'\W',' ',train_words[i])
    train_words[i] = re.sub(r'\s+',' ',train_words[i])
    #words[i] = re.sub("[^a-zA-Z]",' ',words[i])

t_word_dist = nltk.FreqDist(train_words)
#rslt_words = pd.DataFrame(t_word_dist, columns=['Word', 'Frequency'])


mths = np.asarray(result['month'])
days = np.asarray(result['day'])
wday = np.asarray(result['weekday_weekend'])
yr = np.asarray(result['year'])

rslt_words = pd.DataFrame(t_word_dist.most_common(len(yr)), columns=['Word', 'Frequency'])
titles = np.asarray(rslt_words['Word'])

print("----title:----")
print(titles)
print("---months---")
print(mths)
print("----days----")
print(days)
print("----weekdate----")
print(wday)
print("---year---")
print(yr)

#create label encoder
le = preprocessing.LabelEncoder()
#convert strings into numbers
#title_encoded = le.fit_transform(titles)
#print(title_encoded)

title_encoded = le.fit_transform(titles)
print(len(title_encoded))
mth_encoded = le.fit_transform(mths)
days_encoded = le.fit_transform(days)
wday_encoded = le.fit_transform(wday)
yr_encoded = le.fit_transform(yr)

#combine to be features
features_t_wday = zip(title_encoded, mth_encoded)
features_t_wday = list(features_t_wday)
print(features_t_wday)

#create Gaussian classifier
model = GaussianNB()
#traning set
model.fit(features_t_wday, wday_encoded)

#Predicted output
predicted = model.predict([[0,2]])
print("predicted value:")
print(predicted)

#split to training and testing data
train_data =train_data[~train_data.isin([np.nan, np.inf, -np.inf]).any(1)]
X_train, X_test, y_train, y_test = train_test_split(train_data, train_data.weekday_weekend, test_size=0.3, random_state=800) # 70% training and 30% test

#create gaussian classifier
gnb = GaussianNB()
gnb.fit(X_train, y_train)
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
acc = metrics.accuracy_score(y_test, y_pred)
print("-----Accuracy:------")
print(acc)



