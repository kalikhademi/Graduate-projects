import sys

import csv
import pandas
import tweepy
import numpy as np
import tensorflow as tf
import random

from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator, TransformerMixin

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Embedding, SpatialDropout1D
from keras.layers import LSTM
from keras.utils import to_categorical
from keras import regularizers
from keras.constraints import max_norm
from keras import backend as K
from keras.wrappers.scikit_learn import KerasClassifier

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, TweetTokenizer

import joblib
import pickle

import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

## start tweepy authentication
consumer_key = "dZxS92FOBUpoFNzWJnSQyGgJi"
consumer_secret = "FfNV8UBNGRxudARyG5yAboHrLXcDQYr1GoFiwPMe7e8UlMarJJ"
access_token = "2999019328-I5RS99tTyBSP7ukmbnCLv2PoUU88cou4h7cl4AJ"
access_token_secret = "AJk5BFkhx5XmxHIG8s3JorPa4zNi3C69u4urGZq8ZGtkq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

## use tweepy to get training tweets
def get_training_tweets(rows=None):
    #import training dataset
    train = pandas.read_csv(r'..\..\dataverse_files\hatespeechtwitter.tab', sep='\t', header=(0), nrows=rows)
    print(len(train))
    train.dropna(axis=0, how='any')
    print(len(train))

    duplicates = train[train.duplicated(['tweet_id'])==True].sort_values(by=['tweet_id'])
    print(len(duplicates))
    train = train.drop_duplicates(subset="tweet_id")
    print(len(train))
    train = train.replace(to_replace=["abusive", "hateful"], value="derogatory")


    #get tweet text based on IDs
    tweet_ids = train["tweet_id"].tolist()
    tweet_txt = []
    # not all the tweets will still be online so we need to save ids for those that are
    saved_ids = []
    for i in range(0, len(train), 100):
        print(i)
        tweets = api.statuses_lookup(tweet_ids[i:i+100])
        #print("return tweets length " + str(len(tweets)))
        for i in tweets:
            tweet_txt.append(i.text)
            saved_ids.append(i.id)
    print("done")


    # append tweet text to original dataframes
    # (we're keeping tweet IDs for troubleshooting for now, even though they're not used to train the model)
    train_tweets = train[train['tweet_id'].isin(saved_ids)]
    #train_tweets = train_tweets.drop_duplicates(subset="tweet_id")
    print(len(train_tweets))
    print(len(tweet_txt))
    #print(len(set(tweet_txt)))
    print(len(saved_ids))
    #print(len(set(saved_ids)))
    train_tweets = train_tweets.assign(tweets = tweet_txt)
    # import to csv
    if rows is not None:
        filename = "train_tweets" + str(rows) + "_2.csv"
    else:
        filename = "train_tweets_full_2.csv"
    train_tweets.to_csv(filename, index=False)

def get_testing_tweets(rows=None):
    test = pandas.read_csv(r'..\..\TwitterAAE-full-v1\twitteraae_limited', sep='\t', nrows=rows,
        engine="python", error_bad_lines=False, names=["tweet_id", "Time","AA","Hispanic","Other","White"])
    test.dropna()
    test = test.drop_duplicates(subset="tweet_id")

    #get tweet text based on IDs
    tweet_ids = test["tweet_id"].tolist()
    tweet_txt = []
    # not all the tweets will still be online so we need to save ids for those that are
    saved_ids = []
    for i in range(0, len(test), 100):
        print(i)
        tweets = api.statuses_lookup(tweet_ids[i:i+100])
        for i in tweets:
            tweet_txt.append(i.text)
            saved_ids.append(i.id)
    print("done")

    #get race labels
    test = test[test['tweet_id'].isin(saved_ids)]
    test = test.drop("tweet_id", axis=1)
    test = test.drop("Time", axis=1)
    race_labels = test.idxmax(axis=1)
    #pair tweet text with original labels
    test_tweets = pandas.DataFrame(list(zip(tweet_txt,race_labels)), columns=["tweet", "race"])
    test_tweets = test_tweets.assign(tweet_id = saved_ids)
    #import to csv
    if rows is not None:
        filename = "test_tweets" + str(rows) + ".csv"
    else:
        filename = "test_tweets_full.csv"
    test_tweets.to_csv(filename, index=False)

#https://towardsdatascience.com/handling-imbalanced-datasets-in-deep-learning-f48407a0e758
def focal_loss(y_true, y_pred):
    gamma = 2.0
    alpha = 0.25
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0))

def train_model_LR(X, y):
    '''X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X,y, test_size = 0.3, random_state = 0, stratify=y)'''

    skf = model_selection.StratifiedKFold(n_splits=5)

    LR_model = Pipeline([ ('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
        ('clf', LogisticRegression(solver="saga", multi_class="multinomial")),])
    #LR_model =  Pipeline([ ('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
    #    ('clf', SVC(kernel="poly", gamma="auto")),])

    X = np.array(X)
    y = np.array(y)

    for train, valid in skf.split(X, y):
        X_train = X[train]
        X_valid = X[valid]
        y_train = y[train]
        y_valid = y[valid]

        print(set(y_train))
        LR_model.fit(X_train, y_train)
        preds = LR_model.predict(X_valid)
        print("LR:")
        print(accuracy_score(y_valid, preds))
        print(set(preds))
    LR_model.fit(X, y)
    preds = LR_model.predict(X)
    print("LR:")
    print(accuracy_score(y, preds))
    print(set(preds))

    return LR_model

def train_model_RF(X, y):
    '''
    from sklearn.model_selection import RandomizedSearchCV# Number of trees in random forest
    from pprint import pprint
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]# Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}
    pprint(random_grid)

    tokenizer = Tokenizer(nb_words=2500, lower=True,split=' ')
    stop_words = set(stopwords.words('english'))
    tknzr = TweetTokenizer(strip_handles=True)
    word_tokens = [tknzr.tokenize(tweet) for tweet in X]
    #table = str.maketrans('', '', string.punctuation)
    #word_tokens = [[w.translate(table) for w in tweet if w.translate(table) is not ''] for tweet in word_tokens]
    filtered = [[w.lower() for w in tweet if w.lower() not in stop_words] for tweet in word_tokens]
    tokenizer.fit_on_texts(filtered)
    X = tokenizer.texts_to_sequences(filtered)
    X = pad_sequences(X, maxlen=40)

    '''
    RF_model = Pipeline([ ('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier(n_estimators=20, min_samples_split=10, bootstrap=True, class_weight="balanced")),])


    #rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    #RF_model = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)



    X_train, X_valid, y_train, y_valid = model_selection.train_test_split(X, y, test_size = 0.3, stratify=y)

    RF_model.fit(X_train, y_train)

    #print(RF_model.best_params_)
    preds = RF_model.predict(X_valid)
    print("RF:")
    print(accuracy_score(y_valid, preds))
    preds = RF_model.predict(X)
    count = Counter(preds)
    for val in count:
        print("%s : %s" % (val, count[val]))

    return RF_model

def train_model_LSTM(X, y, out_file="model_lstm3.h5"):
    tokenizer = Tokenizer(num_words=15000, lower=True,split=' ')
    #print(tokenizer.word_index)

    #nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tknzr = TweetTokenizer(strip_handles=True)
    word_tokens = [tknzr.tokenize(tweet) for tweet in X]
    #table = str.maketrans('', '', string.punctuation)
    #word_tokens = [[w.translate(table) for w in tweet if w.translate(table) is not ''] for tweet in word_tokens]
    filtered = [[w.lower() for w in tweet if w.lower() not in stop_words] for tweet in word_tokens]
    tokenizer.fit_on_texts(filtered)
    X = tokenizer.texts_to_sequences(filtered)
    X = pad_sequences(X, maxlen=40)
    X_orig = X

    '''
    normal = [X[i] for i in range(len(y)) if y[i] == "normal" and random.choice([True, False]) is True]
    normal_y = ["normal" for i in range(len(normal))]
    spam = [X[i] for i in range(len(y)) if y[i] == "spam"]
    spam_y = ["spam" for i in range(len(spam))]
    derog = [X[i] for i in range(len(y)) if y[i] == "derogatory"]
    derog_y = ["derogatory" for i in range(len(derog))]

    normal = normal[:1000]
    normal_y = normal_y[:1000]
    spam = spam[:200]
    spam_y = spam_y[:200]
    derog = derog[:240]
    derog_y = derog_y[:240]

    X = normal + spam + derog
    y = normal_y + spam_y + derog_y
    c = list(zip(X, y))
    random.shuffle(c)
    X, y = zip(*c)
    X = np.asarray(X)
    y = np.asarray(y)
    count = Counter(y)
    for val in count:
        print("%s : %s" % (val, count[val]))
    '''
    y_p = y
    le = LabelEncoder()
    le.fit(y)
    y = le.transform(y)
    y_orig = y

    y = to_categorical(y)

    #y = [one_hot(i, 1) for i in y]
    #print(y)

    embed_dim = 100
    lstm_out = 50
    batch_size = 64

    print("input length")
    print(X.shape[1])

    model = Sequential()
    model.add(Embedding(15000, embed_dim,input_length = X.shape[1]))
    model.add(SpatialDropout1D(rate=0.7))
    #model.add(LSTM(lstm_out, return_sequences=True, dropout=0.2, recurrent_dropout=0.2))
    #model.add(LSTM(lstm_out, return_sequences=True, dropout=0.6, recurrent_dropout=0.6))
    model.add(LSTM(lstm_out, dropout=0.7, recurrent_dropout=0.7, kernel_constraint=max_norm(2), recurrent_constraint=max_norm(2)))
    model.add(Dense(3,activation='softmax',kernel_regularizer=regularizers.l2(0.001)))
    model.compile(loss =[focal_loss], optimizer='adam',metrics = ['accuracy'])
    print(model.summary())

    X_train, X_valid, y_train, y_valid = model_selection.train_test_split(X, y, test_size = 0.3, stratify=y)

    y_integers = np.argmax(y, axis=1)
    print(y)
    print(y_integers)
    print(le.inverse_transform(y_integers))
    class_weights = compute_class_weight('balanced', np.unique(y_integers), y_integers)
    d_class_weights = dict(enumerate(class_weights))
    print(d_class_weights)

    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=50,  verbose=1, shuffle=True, validation_split=0.2, class_weight=d_class_weights)

    '''
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model train vs validation accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
    '''

    score,acc = model.evaluate(X_valid, y_valid, verbose=1, batch_size=batch_size)
    print("Score: %.2f" % (score))
    print("Validation set Accuracy: %.2f" % (acc))


    preds = model.predict(X_orig)
    preds = [np.argmax(i) for i in preds]
    preds = le.inverse_transform(preds)
    label_preds = zip(preds, y_p)

    count = Counter(preds)
    for val in count:
        print("%s : %s" % (val, count[val]))

    f1 = f1_score(y_p, preds, average="micro")
    print(f1)

    model.save(out_file)
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return model

def saveModel(model, filename="model.pkl"):
    joblib.dump(model, filename)

def main():
    command = sys.argv[1]
    if command == "get-train":
        rows = int(sys.argv[2]) if sys.argv[2] != "None" else None
        print("train get start")
        get_training_tweets(rows)
        print("train get end")
    elif command == "get-test":
        rows = int(sys.argv[2]) if sys.argv[2] != "None" else None
        print("test get start")
        get_testing_tweets(rows)
        print("test get end")
    elif command == "make-model":
        print("import data")
        filename = sys.argv[2]
        out_file = sys.argv[3] if sys.argv[3] != None else "model.pkl"
        ## get training data
        train = pandas.read_csv(filename,header=(0))
        train.dropna()
        X = list(train["tweets"])
        y = list(train["maj_label"])
        count = Counter(y)
        for val in count:
            print("%s : %s" % (val, count[val]))
        #print(y.index(np.nan))
        #print(train.iloc[y.index(np.nan)])
        print("model training start")

        model = train_model_LSTM2(X, y)#, out_file)
        print("model trained")

        saveModel(model,out_file)
        print("model saved in " + out_file)
    elif command == "predict":
        #do we want to use a neural net model?
        net = False
        # get data we want to make predictions for
        input = sys.argv[2]
        test = pandas.read_csv(input, header=(0))
        X = list(test["tweet"])
        X_orig = X
        # get ML model
        model = sys.argv[3]
        preds = []
        if net is False:
            model = joblib.load(model)
            # make predictions
            preds = model.predict(X)
        else:
            LSTM_model = load_model(model, custom_objects={'focal_loss': focal_loss})
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            X = tokenizer.texts_to_sequences(X)
            X = pad_sequences(X, maxlen=40)
            print(X.ndim)
            print(X[0].ndim)
            print('*')
            print(X.shape[0])
            print(X.shape[1])
            preds = LSTM_model.predict(X, batch_size=8)
            preds = [np.argmax(i) for i in preds]
            for i in range(len(preds)):
                if preds[i] == 0:
                    preds[i] = "derogatory"
                    #print(X_orig[i])
                elif preds[i] == 1:
                    preds[i] = "normal"
                else:
                    preds[i] = "spam"
            #print(preds)
        print(set(preds))
        test["labels"] = np.asarray(preds)
        # compare classes by race
        sns.set(style="whitegrid")
        sns.set(font_scale=4)
        ax = sns.countplot(x="race", hue="labels", data=test)
        plt.show()
        races = set(test['labels'])
        count_race_labels = test.loc[test['labels'] == 'derogatory']
        count_race_labels = count_race_labels.groupby(['labels', 'race'])["tweet"].size().reset_index(name="abusive_counts")
        print(count_race_labels)
        count_race =  test.groupby('race')["tweet"].size().reset_index(name="counts")
        count_race_labels["proportion"] = count_race_labels["abusive_counts"] / count_race["counts"]
        print(count_race_labels)
        ax = sns.barplot(x="race", y='proportion', data=count_race_labels)
        plt.show()
    else:
        print("not a valid command")

if __name__ == '__main__':
    main()
