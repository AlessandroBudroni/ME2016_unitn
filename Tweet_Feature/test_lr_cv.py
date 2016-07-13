from sklearn.cross_validation import  KFold
from sklearn import svm
import numpy as np
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
import pickle

dataset = 'devset'
post_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
            'image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'

#classifier choice
classifier = 'logis' # can be 'logis' or 'svm'

#load effective posts
eff_posts = []
with open('eff_posts.nam') as f:
    for line in f:
        line = line.strip('\n\t ')
        eff_posts.append(line)

# load post to link post ID and multimedia ID
posts = None
with open('posts.pickle', 'rb') as handle:
  posts = pickle.load(handle)

# load data
data = np.loadtxt('tweet_features.dat', delimiter=',')
labels = np.array(data[:,-1],dtype=int)
count = sum(labels == -1)
data = data[:,:-1]

topic_combined_features = np.loadtxt('../Textual_Feature/topic_combined_features.dat')
eff_topics = []
with open('../Textual_Feature/devset_eff_textual_topics.top') as f:
    for line in f:
        line = line.strip('\n\t ')
        eff_topics.append(line)


# cross-validation 10 fold
n_folds = 10
kf = KFold(data.shape[0], n_folds=n_folds, shuffle = True)
score = 0
for train_index, test_index in kf:
    X_train, X_test = data[train_index], data[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    detector = None
    if classifier == 'logis':
        detector = logis(C=1e5, solver='lbfgs', multi_class='ovr')
    elif classifier == 'svm':
        detector = svm.SVC()

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    detector.fit(X_train, y_train)

    X_test = scaler.transform(X_test)
    pr_labels = detector.predict(X_test)

    acc = sum(y_test == pr_labels)*100 / y_test.shape[0]
    score += acc

    print('Acc: ', acc, '%')

print('Average acc: ', score/n_folds)