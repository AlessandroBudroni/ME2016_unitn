from sklearn.cross_validation import  KFold
from sklearn import svm
import numpy as np
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
from sklearn.metrics import f1_score
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier


classifier = 'randomforest'
dataset = 'devset'
post_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
            'image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'


def extract_topic_feature(mul_list):
    forensic_features = np.loadtxt('output/devset_forensic_features.dat',
                                   delimiter=',', dtype=float)

    eff_forensic_topics = read_list('output/devset_eff_forensic_topics.dat')

    textual_features = np.loadtxt('output/devset_textual_features.dat',
                                  delimiter=',', dtype=float)

    eff_textual_topics = read_list('output/devset_eff_textual_topics.dat')

    forensic_feature_ind = np.array(range(0, forensic_features.shape[1]), dtype=int)
    textual_feature_ind = np.array(range(forensic_features.shape[1],
                                         forensic_features.shape[1] + textual_features.shape[1]), dtype=int)

    data = np.zeros((len(mul_list), forensic_features.shape[1] +
                     textual_features.shape[1]))

    used_ind = np.ones((len(mul_list),), dtype=bool)

    non_eff_topics = []
    eff_topics = []
    for ind, m in enumerate(mul_list):
        if m in eff_textual_topics:
            ind1 = eff_textual_topics.index(m)
            data[ind, textual_feature_ind] = textual_features[ind1,]
            eff_topics.append(m)
        if m in eff_forensic_topics:
            ind2 = eff_forensic_topics.index(m)
            data[ind, forensic_feature_ind] = forensic_features[ind2,]
            if not m in eff_topics:
                eff_topics.append(m)
        if not (m in eff_textual_topics or m in eff_forensic_topics):
            used_ind[ind,] = False
            non_eff_topics.append(m)

    return data[used_ind,:], eff_topics


def read_list(file_name):
    l = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip('\n\t ')
            l.append(line)
    return l


def write_list(file_name, l):
    with open(file_name, 'w') as f:
        for e in l:
            f.write('{}\n'.format(e))


def main():
    # load tweet features
    data = np.loadtxt('output/' + dataset + '_tweet_features.dat', delimiter=',')
    labels = np.array(data[:, -1], dtype=int)
    count = sum(labels == -1)
    data = data[:, :-1]

    # load effective posts
    eff_posts = []
    with open('output/' + dataset + '_eff_posts.dat') as f:
        for line in f:
            line = line.strip('\n\t ')
            eff_posts.append(line)

    use_topic_feature = 0
    concat_data = None

    if use_topic_feature == 1:
        # load posts dict
        posts_dict = None
        with open('output/' + dataset + '_posts_dict.pickle', 'rb') as handle:
            posts_dict = pickle.load(handle)

        # concatenate features together

        mul_list = {}
        for p in eff_posts:
            mul_id = posts_dict[p][0].strip('\n\t ')
            mul_list[mul_id] = 1

        mul_list = list(mul_list.keys())

        topic_features, eff_topics = extract_topic_feature(mul_list)
        concat_data = np.zeros((data.shape[0], data.shape[1] + topic_features.shape[1]))

        for ind, p in enumerate(eff_posts):
            mul_id = posts_dict[p][0].strip('\n\t ')
            concat_data[ind, :data.shape[1]] = data[ind, :]
            if mul_id in eff_topics:
                concat_data[ind, data.shape[1]:] = topic_features[eff_topics.index(mul_id)]
    else:
        concat_data = data

    # cross-validation 10 folds
    n_folds = 20
    kf = KFold(data.shape[0], n_folds=n_folds, shuffle = True)
    score = 0
    count = 1
    avg_score = 0
    avg_acc = 0

    for train_index, test_index in kf:
        X_train, X_test = concat_data[train_index], concat_data[test_index]
        y_train, y_test = labels[train_index], labels[test_index]

        scaler = preprocessing.StandardScaler().fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        detector = None
        if classifier == 'logis':
            detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
        elif classifier == 'svm':
            detector = svm.SVC()
        elif classifier == 'randomforest':
            detector = ExtraTreesClassifier(n_estimators=100, max_depth=None,
                                            min_samples_split=1, random_state=0)

        detector.fit(X_train, y_train)

        pr_labels = detector.predict(X_test)
        # pr_proba = detector.predict_proba(X_test_scaled)

        score = f1_score(y_test, pr_labels, average='binary')
        avg_score += score

        acc = sum(y_test == pr_labels) / X_test.shape[0]
        avg_acc += acc

        print('\nLoop ', count, '\n')
        print('F1 score: ', score*100, '%')
        print('Acc: ', acc, '%')

        count += 1

    print('Average F1 score: ', avg_score * 100 / n_folds, '%')
    print('Average accuracy: ', avg_acc * 100 / n_folds, '%')

if __name__ == '__main__':
    main()


