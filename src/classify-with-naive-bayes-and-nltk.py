#coding: utf-8
from __future__ import print_function, unicode_literals

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn import metrics

from os import listdir
from os.path import isfile, join
import shutil

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import sys

BRANCH = ''

if len(sys.argv) > 1:
    BRANCH = sys.argv[1]
else:
    print('Give parameter')
    sys.exit()

def parse_nltk(sentence):
    porter = PorterStemmer()
    stop = set(stopwords.words('english'))
    # Remove URL
    sentence = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', sentence)
    last_is_neg = ''
    phrase = ''
    for word in sentence.lower().decode('utf-8').split():
        if word == 'not' or word == 'no':
            last_is_neg = word
        if word not in stop:
            # Remove prefix
            word = porter.stem(word)
            if last_is_neg != '':
                word = last_is_neg + '_' + word
                last_is_neg = ''
            phrase = phrase + " " + word
    return phrase

# Dir of the rating that will create the template
model_dir = 'data/hadoop_messages/branch-0.1/manual'
model_train = load_files(model_dir, description=None, load_content=True, shuffle=True, encoding='utf-8', decode_error='ignore', random_state=42)

count_vect = CountVectorizer()

# Remove links, stopwords...
train_data = []
for phrase in model_train.data:
    converted_text = parse_nltk(phrase)
    train_data.append(converted_text)


X_train_counts = count_vect.fit_transform(train_data)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


clf = MultinomialNB().fit(X_train_tfidf, model_train.target)

# Dir of rating created
dir_not_evaluate = 'data/hadoop_messages/' + BRANCH + '/naivebayes'
# Dir of release unrated
dir_evaluate = 'data/hadoop_messages/' + BRANCH + '/all'
evaluate = []
for f in listdir(dir_evaluate):
    if isfile(join(dir_evaluate, f)):
        archive = open(("%s/%s" % (dir_evaluate, f)), "r")
        converted_text = parse_nltk(archive.read())
        content = [f, converted_text]
        evaluate.append(content)

docs_new = [t[1] for t in evaluate]

X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])

text_clf = text_clf.fit(train_data, model_train.target)
predicted = clf.predict(X_new_tfidf)

for index, (doc, category) in enumerate(zip(docs_new, predicted)):
    print('%d: %r => %s' % (index, doc, model_train.target_names[category]))
    shutil.copy(("%s/%s" % (dir_evaluate, evaluate[index][0])),
                ("%s/%s/%s" % (dir_not_evaluate, model_train.target_names[category], evaluate[index][0])))


# AVALIANDO O DESEMPENHO
twenty_test = model_train
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
print('Usando Naive Bayes com NLTK, a precisão é de %.d%%' % (np.mean(predicted == twenty_test.target) * 100))

print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
print(metrics.confusion_matrix(twenty_test.target, predicted))


