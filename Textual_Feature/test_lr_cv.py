# This script performs cross-validation on fake multimedia detection
# Need both textual features and forensic features
# Can select classification method
# Report results in Accuracy and F1 score

from sklearn.cross_validation import  KFold
from sklearn import svm
import numpy as np
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score

#classifier choice
classifier = 'randomforest' # can be 'logis', 'svm', 'forestclassifier'
use_forensics = True

# load data
textual_data = np.loadtxt('devset_textual_features.dat', delimiter=',')

data = None
if use_forensics:

    forensic_data = np.loadtxt('../Image_Forensics/devset_forensic_features.dat',
                               delimiter=',')
    forensic_data = forensic_data[:,:-1] # remove labels

    eff_forensic_topics = []
    with open('../Image_Forensics/devset_eff_forensic_topics.dat', 'r') as f:
        for line in f:
            eff_forensic_topics.append(line.strip('\n\t '))

    eff_textual_topics = []
    with open('devset_eff_textual_topics.dat', 'r') as f:
        for line in f:
            eff_textual_topics.append(line.strip('\n\t '))

    data = np.zeros((textual_data.shape[0],forensic_data.shape[1] + textual_data.shape[1]))
    for t in eff_textual_topics:
        ind1 = eff_textual_topics.index(t)
        if t in eff_forensic_topics:
            ind2 = eff_forensic_topics.index(t)
            data[ind1,] = np.append(forensic_data[ind2,],textual_data[ind1,])
        else:
            print(t)
            data[ind1,] = np.append(np.zeros((1,forensic_data.shape[1])), textual_data[ind1,])

    print('\nSave features\n')
    np.savetxt('topic_combined_features.dat', data)

else:
    data = textual_data


labels = np.array(data[:,-1],dtype=int)
data = data[:,:-1]

# cross-validation 10 fold
n_folds = 10
kf = KFold(data.shape[0], n_folds=n_folds, shuffle = True)
avg_score = 0
avg_acc = 0

for train_index, test_index in kf:
    X_train, X_test = data[train_index], data[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    detector = None
    if classifier == 'logis':
        detector = logis(C=1e5, solver='lbfgs', multi_class='ovr')
    elif classifier == 'svm':
        detector = svm.SVC()
    elif classifier == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=100, max_depth=None,
                                              min_samples_split=1, random_state=0)

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    detector.fit(X_train, y_train)

    X_test = scaler.transform(X_test)
    pr_labels = detector.predict(X_test)

    acc = sum(y_test == pr_labels) / y_test.shape[0]
    score = f1_score(y_test, pr_labels, average='binary')

    avg_acc += acc
    avg_score += score

    print('Acc: ', acc, '%')
    print('F1 score: ', score*100, '%')

print('Average F1 score: ', avg_score*10, '%')
print('Average acc: ', avg_acc*10, '%')





