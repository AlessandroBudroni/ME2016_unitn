# this script perform cross-validation on image set using forensic feature

from sklearn.cross_validation import  KFold
import numpy as np
from sklearn.linear_model import LogisticRegression as logis
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier

# classifier choice
classifier = 'randomforest'

# load data
data = np.loadtxt('devset_forensic_features.dat', delimiter=',')

labels = np.array(data[:,-1],dtype=int)
data = data[:,:-1]


# cross-validation 10 fold
n_folds = 10
kf = KFold(data.shape[0], n_folds=n_folds, shuffle=True)
avg_score = 0
avg_acc = 0
for train_index, test_index in kf:
    X_train, X_test = data[train_index], data[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    # normalize data
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    detector = None
    if classifier == 'logis':
        detector = logis(C=1e5, solver='lbfgs', multi_class='multinomial')
    elif classifier == 'svm':
        detector = svm.SVC()
    elif classifier == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=100, max_depth=None,
                                              min_samples_split=1, random_state=0)

    detector.fit(X_train, y_train)

    X_test = scaler.transform(X_test)
    pr_labels = detector.predict(X_test)

    acc = sum(y_test == pr_labels) / y_test.shape[0]
    score = f1_score(y_test, pr_labels, average='binary')

    avg_acc += acc
    avg_score += score

    print('Acc: ', acc, '%')
    print('F1 score: ', f1_score(y_test, pr_labels, average='binary'))

print('Average accuracy: ', avg_acc*10, '%')
print('Average F1 score: ', avg_score*10, '%')



