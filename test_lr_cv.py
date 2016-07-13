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

classifier1 = 'randomforest'
classifier2 = 'randomforest'


dataset = 'devset'
post_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
            'image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'


def selectively_split_data():
    training_event = ['sandy', 'boston', 'nepal']

    # load tweet features
    data = np.loadtxt('output/' + dataset + '_tweet_features.dat', delimiter=',')
    eff_posts = read_list('output/' + dataset + '_eff_posts.dat')

    posts_dict = None
    with open('output/' + dataset + '_posts_dict.pickle', 'rb') as handle:
        posts_dict = pickle.load(handle)

    training_event_dict = {'sandy':[0, 0], 'boston':[0, 0], 'nepal':[0, 0]}
    training_mul_dict = {}

    training_ind = []
    testing_ind = []

    for ind, p in enumerate(eff_posts):
        mul_id = posts_dict[p][0].strip('\n\t ')
        w = mul_id.split('_')[0]
        label = posts_dict[p][1].strip('\n\t ')
        if w in training_event_dict:
            l = training_event_dict[w]
            if l[0] < 300 and label == '-1':
                training_ind.append(ind)
                l[0] += 1
                training_event_dict[w] = l
                training_mul_dict[mul_id] = 1
            elif l[1] < 300 and label == '1':
                training_ind.append(ind)
                l[1] += 1
                training_event_dict[w] = l
                training_mul_dict[mul_id] = 1

    print('Number of topics for training: ', len(training_mul_dict), '/400')
    testing_count = [0,0]
    testing_mul_dict = {}
    for ind, p in enumerate(eff_posts):
        mul_id = posts_dict[p][0].strip('\n\t ')
        label = posts_dict[p][1].strip('\n\t ')
        if not (ind in training_ind or mul_id in training_mul_dict):
            if label == '-1' and testing_count[0] < 300:
                testing_ind.append(ind)
                testing_count[0] += 1
                testing_mul_dict[mul_id] = 1
            elif label == '1' and testing_count[1] < 300:
                testing_ind.append(ind)
                testing_count[1] += 1
                testing_mul_dict[mul_id] = 1

    print('Number of topics for testing: ', len(testing_mul_dict), '/400')

    training_ind = np.array(training_ind, dtype=int)
    testing_ind = np.array(testing_ind, dtype=int)

    X_train = data[training_ind]
    X_test = data[testing_ind]

    eff_train_posts = [eff_posts[ind] for ind in training_ind]
    eff_test_posts = [eff_posts[ind] for ind in testing_ind]

    np.savetxt('output/training_data.dat', X_train)
    np.savetxt('output/testing_data.dat', X_test)
    write_list('output/training_posts.dat', eff_train_posts)
    write_list('output/testing_posts.dat', eff_test_posts)

def split_data():
    # load tweet features
    data = np.loadtxt('output/' + dataset + '_tweet_features.dat', delimiter=',')

    # load effective posts
    eff_posts = []
    with open('output/' + dataset + '_eff_posts.dat') as f:
        for line in f:
            line = line.strip('\n\t ')
            eff_posts.append(line)

    # testing topics
    testing_event = ['sandy']

    # training topics
    training_event = ['boston']

    posts_dict = None
    with open('output/' + dataset + '_posts_dict.pickle', 'rb') as handle:
        posts_dict = pickle.load(handle)

    training_ind = []
    testing_ind = []
    for ind,p in enumerate(eff_posts):
        mul_id = posts_dict[p][0].strip('\n\t ')
        w = mul_id.split('_')[0]
        if w in testing_event:
            testing_ind.append(ind)
        else:
            training_ind.append(ind)

    training_ind = np.array(training_ind, dtype=int)
    testing_ind = np.array(testing_ind, dtype=int)

    X_train = data[training_ind]
    X_test = data[testing_ind]

    eff_train_posts = [eff_posts[ind] for ind in training_ind]
    eff_test_posts = [eff_posts[ind] for ind in testing_ind]

    np.savetxt('output/training_data.dat', X_train)
    np.savetxt('output/testing_data.dat', X_test)
    write_list('output/training_posts.dat', eff_train_posts)
    write_list('output/testing_posts.dat', eff_test_posts)

def extract_multimedia_labels():
    #training_data = np.loadtxt('output/training_data.dat')
    training_posts = read_list('output/training_posts.dat')

    posts_dict = None
    with open('output/' + dataset + '_posts_dict.pickle', 'rb') as handle:
        posts_dict = pickle.load(handle)

    mul_dict = {}
    for p in training_posts:
        mul_id = posts_dict[p][0]
        label = posts_dict[p][1]

        l = [0,0,0]
        if not mul_id in mul_dict:
            mul_dict[mul_id] = l

        l = mul_dict[mul_id]

        if label == '1':
            l[0] += 1
        elif label == '-1':
            l[1] += 1
        l[2] = 1
        if l[1] > l[0]:
            l[2] = -1

        mul_dict[mul_id] = l

    with open('output/'+dataset+'_mul_dict.pickle', 'wb') as handle:
        pickle.dump(mul_dict, handle)

def extract_topic_feature_train():

    forensic_features = np.loadtxt('output/devset_forensic_features.dat',
                               delimiter=',', dtype=float)

    eff_forensic_topics = read_list('output/devset_eff_forensic_topics.dat')

    textual_features = np.loadtxt('output/devset_textual_features.dat',
                               delimiter=',', dtype=float)

    eff_textual_topics = read_list('output/devset_eff_textual_topics.dat')

    forensic_feature_ind = np.array(range(0, forensic_features.shape[1]), dtype=int)
    textual_feature_ind = np.array(range(forensic_features.shape[1],
                                          forensic_features.shape[1] + textual_features.shape[1]), dtype=int)

    # forensic features || textual features
    mul_dict = None
    with open('output/' + dataset + '_mul_dict.pickle', 'rb') as handle:
        mul_dict = pickle.load(handle)

    mul_list = list(mul_dict.keys())
    data = np.zeros((len(mul_list), forensic_features.shape[1] +
                     textual_features.shape[1] + 1)) # +1 for label

    used_ind = np.ones((len(mul_list),), dtype=bool)

    non_eff_topics = []
    eff_topics = []
    for ind,m in enumerate(mul_list):
        if m in eff_textual_topics:
            ind1 = eff_textual_topics.index(m)
            data[ind, textual_feature_ind] = textual_features[ind1,]
            data[ind, -1] = mul_dict[m][2]
            eff_topics.append(m)
        if m in eff_forensic_topics:
            ind2 = eff_forensic_topics.index(m)
            data[ind, forensic_feature_ind] = forensic_features[ind2,]
            data[ind, -1] = mul_dict[m][2]
            if not m in eff_topics:
                eff_topics.append(m)
        if not (m in eff_textual_topics or m in eff_forensic_topics):
            used_ind[ind,] = False
            non_eff_topics.append(m)

    return data[used_ind,:], eff_topics


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


def extract_topic_feature_test(mul_list_test):
    forensic_features = np.loadtxt('output/devset_forensic_features.dat',
                                   delimiter=',', dtype=float)

    eff_forensic_topics = read_list('output/devset_eff_forensic_topics.dat')

    textual_features = np.loadtxt('output/devset_textual_features.dat',
                                  delimiter=',', dtype=float)

    eff_textual_topics = read_list('output/devset_eff_textual_topics.dat')

    forensic_feature_ind = np.array(range(0, forensic_features.shape[1]), dtype=int)
    textual_feature_ind = np.array(range(forensic_features.shape[1],
                                         forensic_features.shape[1] + textual_features.shape[1]), dtype=int)


    data = np.zeros((len(mul_list_test), forensic_features.shape[1] +
                     textual_features.shape[1]))

    used_ind = np.ones((len(mul_list_test), ), dtype=bool)

    non_eff_topics = []
    eff_topics = []
    for ind, m in enumerate(mul_list_test):
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

    selectively_split_data()

    #load tweet features
    X_train = np.loadtxt('output/training_data.dat', dtype=float)
    y_train = np.array(X_train[:, -1], dtype=int)
    y_train[np.where(y_train == -1)] = 0
    X_train = X_train[:,:-1]

    print('number of real training samples: ', sum(y_train == 1), '/', X_train.shape[0])

    X_test = np.loadtxt('output/testing_data.dat', dtype=float)
    y_test = np.array(X_test[:, -1], dtype=int)
    y_test[np.where(y_test == -1)] = 0
    X_test = X_test[:, :-1]

    detector = None
    if classifier1 == 'logis':
        detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier1 == 'svm':
        detector = svm.SVC()
    elif classifier1 == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=200, max_depth=None,
                                          min_samples_split=1, random_state=0)

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    detector.fit(X_train_scaled, y_train)

    pr_labels = detector.predict(X_test_scaled)
    pr_proba = detector.predict_proba(X_test_scaled)

    score = f1_score(y_test, pr_labels, average='binary')
    acc = sum(y_test == pr_labels) * 100 / X_test_scaled.shape[0]

    print('number of real testing samples: ', sum(y_test == 1), '/', y_test.shape[0])

    print('\nwithout forensic and textual features: \n')

    print('F1 score: ', score*100, '%')
    print('Acc: ', acc, '%')

    print('\nwith forensic and textual features: \n')

    topic_detector = None
    if classifier2 == 'logis':
        topic_detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier2 == 'svm':
        topic_detector = svm.SVC()
    elif classifier2 == 'randomforest':
        topic_detector = ExtraTreesClassifier(n_estimators=100, max_depth=None,
                                              min_samples_split=1, random_state=0)

    posts_dict = None
    with open('output/' + dataset + '_posts_dict.pickle', 'rb') as handle:
        posts_dict = pickle.load(handle)

    # training_posts = read_list('output/training_posts.dat')
    # mul_list_train = {}
    # for p in training_posts:
    #     mul_id = posts_dict[p][0].strip('\n\t ')
    #     mul_list_train[mul_id] = 1
    #
    # mul_list_train = list(mul_list_train.keys())
    # topic_features_train, eff_topics_train = extract_topic_feature(mul_list_train)
    #
    # concat_data_train = np.zeros((X_train.shape[0], X_train.shape[1] + topic_features_train.shape[1]))
    #
    # for ind,p in enumerate(training_posts):
    #     mul_id = posts_dict[p][0].strip('\n\t ')
    #     concat_data_train[ind,:X_train.shape[1]] = X_train[ind,:]
    #     if mul_id in eff_topics_train:
    #         concat_data_train[ind,X_train.shape[1]:] = topic_features_train[eff_topics_train.index(mul_id)]
    #
    # testing_posts = read_list('output/testing_posts.dat')
    # mul_list_test = {}
    # for p in testing_posts:
    #     mul_id = posts_dict[p][0].strip('\n\t ')
    #     mul_list_test[mul_id] = 1
    #
    # mul_list_test = list(mul_list_test.keys())
    # topic_features_test, eff_topics_test = extract_topic_feature(mul_list_test)
    #
    # concat_data_test = np.zeros((X_test.shape[0], X_test.shape[1] + topic_features_test.shape[1]))
    #
    # for ind, p in enumerate(testing_posts):
    #     mul_id = posts_dict[p][0].strip('\n\t ')
    #     concat_data_test[ind, :X_test.shape[1]] = X_test[ind,:]
    #     if mul_id in eff_topics_test:
    #         concat_data_test[ind, X_test.shape[1]:] = topic_features_test[eff_topics_test.index(mul_id)]
    #
    # # test again
    # scaler = preprocessing.StandardScaler().fit(concat_data_train)
    # concat_data_train_scaled = scaler.transform(concat_data_train)
    # concat_data_test_scaled = scaler.transform(concat_data_test)
    #
    # detector.fit(concat_data_train_scaled, y_train)
    #
    # pr_labels = detector.predict(concat_data_test_scaled)
    # #pr_proba = detector.predict_proba(X_test_scaled)
    #
    # score = f1_score(y_test, pr_labels, average='binary')
    # acc = sum(y_test == pr_labels) * 100 / concat_data_test_scaled.shape[0]
    #
    # print('F1 score: ', score*100, '%')
    # print('Acc: ', acc, '%')

    extract_multimedia_labels()

    training_posts = read_list('output/training_posts.dat')

    topic_features_train, eff_topics_train = extract_topic_feature_train()
    X_topic_train = topic_features_train
    y_topic_train = np.array(X_topic_train[:, -1], dtype=int)
    y_train[np.where(y_train == -1)] = 0
    X_topic_train = X_topic_train[:, :-1]

    scaler = preprocessing.StandardScaler().fit(X_topic_train)
    X_topic_train = scaler.transform(X_topic_train)

    topic_detector.fit(X_topic_train, y_topic_train)

    # refine results
    testing_posts = read_list('output/testing_posts.dat')


    mul_list_test = {}
    for p in testing_posts:
        mul_id = posts_dict[p][0].strip('\n\t ')
        mul_list_test[mul_id] = 1
    mul_list_test = list(mul_list_test.keys())

    topic_features_test, eff_topics_test = extract_topic_feature_test(mul_list_test)

    X_topic_test = topic_features_test
    X_topic_test = scaler.transform(X_topic_test)

    topic_pr_probas = topic_detector.predict_proba(X_topic_test)

    new_results = np.zeros((len(testing_posts),))
    for ind,p in enumerate(testing_posts):
        proba_1 = pr_proba[ind,:]
        new_proba = proba_1
        mul_id = posts_dict[p][0].strip('\n\t ')

        if mul_id in eff_topics_test:
            proba_2 = topic_pr_probas[eff_topics_test.index(mul_id),:]
            new_proba = 0.8*proba_2 + 0.2*proba_1

        new_results[ind,] = (new_proba[1] > new_proba[0])

    new_results = np.array(new_results,dtype=int)

    score = f1_score(y_test, new_results, average='binary')
    acc = sum(y_test == new_results) * 100 / y_test.shape[0]

    # print('\nFail cases:\n')
    # for ind, p in enumerate(testing_posts):
    #     mul_id = posts_dict[p][0].strip('\n\t ')
    #     if y_test[ind,] != new_results[ind,] and mul_id in eff_topics_test:
    #         print(mul_id + '\n')

    print('F1 score: ', score*100)
    print('Acc: ', acc, '%')

def feature_importance():
    # load tweet features
    X_train = np.loadtxt('output/training_data.dat', dtype=float)
    y_train = np.array(X_train[:, -1], dtype=int)
    y_train[np.where(y_train == -1)] = 0
    X_train = X_train[:, :-1]

    print('number of training samples: ', X_train.shape[0])
    print('number of real: ', sum(y_train == 1))

    # Build a forest and compute the feature importances
    forest = ExtraTreesClassifier(n_estimators=100,
                                  random_state=0)

    forest.fit(X_train, y_train)

    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    print(np.sort(indices[0:10]))
    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X_train.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X_train.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X_train.shape[1]), indices)
    plt.xlim([-1, X_train.shape[1]])
    plt.show()


if __name__ == '__main__':
    #feature_importance()
    #extract_multimedia_labels()
    #topic_features, eff_topics = extract_topic_feature_train()

    #abc = 1

    main()