from unicodedata import category
import numpy as np
import pandas as pd
import nltk
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.linear_model import SGDClassifier

def read_data(filename):   
    global data
    data = pd.read_csv(filename)
    return data

def show_data():
    table = open('./templates/table.html','w',encoding="utf-8")
    table.write(data.to_html(classes='table table-stripped'))
    table.close()


def preprocess():
    ps = PorterStemmer()
    corpus = []
    for i in range(len(data)):
        sentence=nltk.sent_tokenize(data['text'][i])
        sentence=[ps.stem(word) for word in sentence if not word in set(stopwords.words('english'))]
        sentence=' '.join(sentence)
        corpus.append(sentence)

    global df
    df = pd.DataFrame(corpus)
    df.rename(columns={0:'text'},inplace=True)

    table = open('./templates/table.html','w',encoding="utf-8")
    table.write(df.to_html(classes='table table-stripped'))
    table.close()


def split_data():
    cv = CountVectorizer()
    y = data['category'].replace(to_replace={'sport':0,'business':1,'politics':2,'tech':3,'entertainment':4})
    x = cv.fit_transform(df['text']).toarray()
    global x_train,y_train,x_test,y_test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=52)



def get_accuracy(algo):
    global model
    if algo == '1':
        model= SVC(kernel='rbf',C=4)
    elif algo == '2':
        model=Perceptron(penalty='elasticnet',alpha = 0.1)
    elif algo == '3':
        model = GaussianNB()
    elif algo == '4':
        model = SGDClassifier(loss='huber')
    elif algo == '5':
        model = LogisticRegression(solver='saga',penalty='l1')

    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    return accuracy_score(y_test,pred) * 100



def get_result(result):
    result = model.predict(np.array([[result]]))[0]
    msg = "The Given Article Belongs To "
    if result == 0:
        category = "Sport"
    elif result == 1:
        category = "Business"
    elif result == 2:
        category = "Politics"
    elif result == 3:
        category = "Tech"
    elif result == 4:
        category = "Entertainment"

    return msg + category
