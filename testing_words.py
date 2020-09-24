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

sport_vectors = []

for i in range(2):
    filename_1 = input("filename:")
    filename_2 = input("filename:")
    filename_3 = input("filename:")
    filename_4 = input("filename:")

    # w_filename = input("write to filename:")
    # f = open(w_filename, "w")

    data_1 = pd.read_csv(filename_1)
    data_2 = pd.read_csv(filename_2)
    data_3 = pd.read_csv(filename_3)
    data_4 = pd.read_csv(filename_4)
    datasets = [data_2, data_3, data_4]
    print(data_1.keys())


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
    result['day'] = new_day[0]

    result['date'] = result['yr']+result['month']+result['day']
    print(result['date'])
    result['date'] = pd.to_datetime(result['date'], format='%Y%m%d')
    result['weekday_weekend'] = result['date'].dt.dayofweek.fillna(0).astype(int)
    result['weekday_weekend'] = result['weekday_weekend'].astype(str)
    print(result.head())

    result['yr'] = result[' news_date'].str[-4:]
    new = result[' news_date'].str.split(" ", n= 3, expand= True)
    #fix month
    result['month'] = new[0]
    d: {str, int} = {'Jan': 1, 'January': 1, 'Feb': 2, 'February': 2, 'Mar': 3, 'March': 3, 'Apr': 4, 'April': 4, 'May': 5, 'Jun': 6, 'June': 6, 'July': 7, 'Jul': 7, 'Aug': 8, 'August': 8, 'Sep': 9, 'September': 9, 'Oct': 10, 'October': 10, 'Nov': 11, 'November': 11, 'Dec': 12, 'December': 12}
    result['month'] = result['month'].map(d).fillna(0)
    result['month'] = result['month'].astype(int)
    result['month'] = result['month'].astype(str)
    new_day = new[1].str.split("|", n=2, expand= True)
    result['day'] = new_day[0]

    print("----working on train set (2020)-----")
    data_1['date'] = data_1['yr']+data_1['month']+data_1['day']
    print(data_1['date'])
    data_1['date'] = pd.to_datetime(data_1['date'], format='%Y%m%d')
    data_1['weekday_weekend'] = data_1['date'].dt.dayofweek.fillna(0).astype(int)
    data_1['weekday_weekend'] = data_1['weekday_weekend'].astype(str)
    print(data_1.head())

    train_data = pd.DataFrame(data_1['news_title'], data_1['weekday_weekend'])

    #convert date into datetime format

    #print(data_1.shape)
    print(data_2.shape)
    print(data_3.shape)
    print(data_4.shape)

    # merge datasets
    wordcount_holder = {}
    i = 0
    # for dataset in datasets:
    #     word2count = {}
    #     for data in dataset:
    #         words = nltk.word_tokenize(data)
    #         for word in words:
    #             if word not in word2count.keys():
    #                 word2count[word] = 1
    #             else:
    #                 word2count[word] += 1
    #
    #     wordcount_holder[i] = word2count
    #     i = i + 1
    #
    # print(wordcount_holder)




    top_N = 50
    top_D = 3
    a = result['news_title'].str.lower().str.cat(sep=' ' or '|')
    b = result['weekday_weekend'].str.cat(sep=' ')
    c = result['month'].str.cat(sep=' ')

    dayofweek = nltk.tokenize.word_tokenize(b)
    months = nltk.tokenize.word_tokenize(c)
    words = nltk.tokenize.word_tokenize(a)
    words = [w for w in words if w not in stopwords.words("english")]
    for i in range(len(words)):
        words[i] = re.sub(r'\W',' ',words[i])
        words[i] = re.sub(r'\s+',' ',words[i])
        #words[i] = re.sub("[^a-zA-Z]",' ',words[i])

    word_dist = nltk.FreqDist(words)
    day_dist = nltk.FreqDist(dayofweek)
    mth_dist = nltk.FreqDist(months)
    print(word_dist)
    print("------")
    print(day_dist)
    print("------")
    print(mth_dist)
    print(len(words))

    print('All frquencies')
    print('=' * 60)

    rslt_words = pd.DataFrame(word_dist.most_common(top_N), columns=['Word', 'Frequency'])
    print(rslt_words)
    print('=' * 60)


    rslt_day = pd.DataFrame(day_dist.most_common(top_D), columns=['WeekDate', 'Frequency'])
    print(rslt_day)
    print('=' * 60)
    #rslt.to_csv(r'{}'.format(w_filename), index=False, header=True)
    #f.close()`
    rslt_mth = pd.DataFrame(mth_dist.most_common(top_D), columns=['Month', 'Frequency'])
    print(rslt_mth)
    print('=' * 60)


    from sklearn.feature_extraction.text import CountVectorizer

    weekday = str(input("which was the top weekdate: "))
    stmt_docs = [data_1['news_title'] for index, row in train_data.iterrows() if data_1['weekday_weekend'] == weekday]

    vec_s = CountVectorizer()
    X_s = vec_s.fit_transform(stmt_docs)
    tdm_s = pd.DataFrame(X_s.toarray(), columns=vec_s.get_feature_names())

    tdm_s

    weekday_1 = str(input("which was the top weekdate: "))
    q_docs = [data_1['sent'] for index,row in train_data.iterrows() if data_1['weekday_weekend'] == weekday_1]

    vec_q = CountVectorizer()
    X_q = vec_q.fit_transform(q_docs)
    tdm_q = pd.DataFrame(X_q.toarray(), columns=vec_q.get_feature_names())

    tdm_q

    word_list_s = vec_s.get_feature_names();
    count_list_s = X_s.toarray().sum(axis=0)
    freq_s = dict(zip(word_list_s, count_list_s))
    freq_s

    word_list_q = vec_q.get_feature_names();
    count_list_q = X_q.toarray().sum(axis=0)
    freq_q = dict(zip(word_list_q,count_list_q))
    freq_q

    #count features
    from sklearn.feature_extraction.text import CountVectorizer

    docs = [data_1['news_title'] for index, row in train_data.iterrows()]

    vec = CountVectorizer()
    X = vec.fit_transform(docs)

    total_features = len(vec.get_feature_names())
    total_features

    #total count of all features in the training set
    total_cnts_features_s = count_list_s.sum(axis=0)
    total_cnts_features_q = count_list_q.sum(axis=0)


    top_N = 50
    train_a = data_1['news_title'].str.lower().str.cat(sep=' ' or '|')

    train_words = nltk.tokenize.word_tokenize(train_a)
    train_words = [w for w in train_words if w not in stopwords.words("english")]
    for i in range(len(train_words)):
        train_words[i] = re.sub(r'\W',' ',train_words[i])
        train_words[i] = re.sub(r'\s+',' ',train_words[i])
        #words[i] = re.sub("[^a-zA-Z]",' ',words[i])

    t_word_dist = nltk.FreqDist(train_words)

    print(t_word_dist)
    print("------")


    print('All frquencies')
    print('=' * 60)

    t_rslt_words = pd.DataFrame(t_word_dist.most_common(top_N), columns=['Word', 'Frequency'])
    print(t_rslt_words)
    print('=' * 60)

    #total frequency
    from nltk.tokenize import word_tokenize
    new_sentence = data_1['news_title']
    prob_s_with_ls = []
    for n in new_sentence:
        new_word_list = word_tokenize(n)
        for word in new_word_list:
            if word in freq_s.keys():
                count = freq_s[word]
            else:
                count = 0
            prob_s_with_ls.append((count + 1)/(total_cnts_features_s + total_features))
        dict(zip(new_word_list,prob_s_with_ls))


    prob_q_with_ls = []
    for n in new_sentence:
        new_word_list = word_tokenize(n)
        for word in new_word_list:
            if word in freq_q.keys():
                count = freq_q[word]
            else:
                count = 0
            prob_q_with_ls.append((count + 1)/(total_cnts_features_q + total_features))
        dict(zip(new_word_list,prob_q_with_ls))