from sklearn.cross_validation import  KFold
from sklearn import svm
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import sys
sys.path.insert(0, 'Text_Retrieval')
import check_hoax_of_fame
import csv

classifier1 = "randomforest"
classifier2 = "randomforest"

def test():

    tweet_features = np.loadtxt('output/testset_tweet_features.dat', delimiter=',')
    eff_tweets = read_list('output/testset_eff_posts.dat')
    event_testset_details = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/testset/multimedia_details.csv'

    scaler_1 = None
    with open('output/RUN_3_scaler_1.pickle', 'rb') as handle:
        scaler_1 = pickle.load(handle)

    detector_1 = None
    with open('output/RUN_3_classifier_1.pickle', 'rb') as handle:
        detector_1 = pickle.load(handle)

    tweet_features = scaler_1.transform(tweet_features)

    tweet_pr_proba = detector_1.predict_proba(tweet_features)

    # load posts dict
    posts_dict = None
    with open('output/testset_posts_dict.pickle', 'rb') as handle:
        posts_dict = pickle.load(handle)

    # load topic features
    forensic_features = np.loadtxt('output/testset_forensic_features.dat',
                                       delimiter=',', dtype=float)

    eff_forensic_topics = read_list('output/testset_eff_forensic_topics.dat')
    textual_features = np.loadtxt('output/testset_textual_features.dat',
                                  delimiter=',', dtype=float)
    eff_textual_topics = read_list('output/testset_eff_textual_topics.dat')

    eff_topics = list(eff_forensic_topics)
    eff_topics.extend(eff_textual_topics)

    mul_list = list(set(eff_topics))

    topic_features = np.zeros((len(mul_list), forensic_features.shape[1] +
                               textual_features.shape[1]), dtype=float)

    topic_labels = np.zeros((len(mul_list),), dtype=int)
    used_ind = np.ones((len(mul_list),), dtype=bool)
    for ind, m in enumerate(mul_list):
        if m in eff_forensic_topics:
            ind1 = eff_forensic_topics.index(m)
            topic_features[ind, :forensic_features.shape[1]] = forensic_features[ind1]
        if m in eff_textual_topics:
            ind2 = eff_textual_topics.index(m)
            topic_features[ind, forensic_features.shape[1]:] = textual_features[ind2]
        if not (m in eff_forensic_topics or m in eff_textual_topics):
            used_ind[ind] = False

    # remove unused topic features
    topic_features = topic_features[used_ind, :]

    scaler_2 = None
    with open('output/RUN_3_scaler_2.pickle', 'rb') as handle:
        scaler_2 = pickle.load(handle)

    detector_2 = None
    with open('output/RUN_3_classifier_2.pickle', 'rb') as handle:
        detector_2 = pickle.load(handle)

    topic_features = scaler_2.transform(topic_features)

    topic_pr_proba = detector_2.predict_proba(topic_features)
    output = {}
    missed_mul_id = {}

    # make event dict to link mul_id to event
    event_dict = {}
    with open(event_testset_details) as csvfileDetail:
        reader = csv.DictReader(csvfileDetail)
        # read row by csvfileDetails
        for row in reader:
            id = row['mul_id'].strip('\n\t ')
            event_name = row['event_name'].strip('\n\t ')
            event_dict[id] = event_name

    for ind,p in enumerate(eff_tweets):
        proba_1 = tweet_pr_proba[ind, :]
        new_proba = proba_1
        mul_id = posts_dict[p].strip('\n\t ')

        if mul_id in mul_list:
            proba_2 = topic_pr_proba[mul_list.index(mul_id), :]
            event_name = event_dict[mul_id]

            new_proba = 0.8*proba_2 + 0.2*proba_1

            output[p] = 'fake'
            if new_proba[1] > new_proba[0]:
                output[p] = 'real'
        else:
            missed_mul_id[mul_id] = 1
            output[p] = 'fake'
            if new_proba[1] > new_proba[0]:
                output[p] = 'real'

    #print out all results
    # missed_mul_id = list(missed_mul_id.keys())
    # for m in missed_mul_id:
    #     print(m)

    print('\nResults of the 3rd RUN \n')
    for p in eff_tweets:
        label = 0
        if output[p] == 'fake':
            label = -1
        elif output[p] == 'real':
            label = 1
        print(p, '\t', posts_dict[p], '\t', label)

    with open('third_run.txt', 'w') as csvfile:
        fieldnames = ['post_id', 'prediction', 'explanation']
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for p in eff_tweets:
            writer.writerow({'post_id':p, 'prediction':output[p],
                             'explanation':''})

def train():

    #
    # load tweet featurese
    #

    tweet_features = np.loadtxt('output/devset_tweet_features.dat', delimiter=',')
    tweet_labels = np.array(tweet_features[:, -1], dtype=int)
    tweet_features = tweet_features[:, :-1]

    # make the training set balanced
    training_posts = read_list('dataset_for_training/real_tweet_id.data')
    training_posts.extend(read_list('dataset_for_training/fake_tweet_id.data'))
    all_posts = read_list('output/devset_eff_posts.dat')
    used_ind = np.ones((len(all_posts),), dtype=bool)

    for ind,p in enumerate(all_posts):
        if not p in training_posts:
            used_ind[ind] = False

    tweet_features = tweet_features[used_ind, :]
    tweet_labels = tweet_labels[used_ind]

    #
    # training classifier 1
    #

    detector = None
    if classifier1 == 'logis':
        detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier1 == 'svm':
        detector = svm.SVC()
    elif classifier1 == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=200, max_depth=None,
                                        min_samples_split=1, random_state=0)

    scaler_1 = preprocessing.StandardScaler().fit(tweet_features)
    tweet_features = scaler_1.transform(tweet_features)
    detector.fit(tweet_features, tweet_labels)
    with open('output/RUN_3_classifier_1.pickle', 'wb') as handle:
        pickle.dump(detector, handle)
    with open('output/RUN_3_scaler_1.pickle', 'wb') as handle:
        pickle.dump(scaler_1, handle)

    #
    # load textual and forensic features
    #

    forensic_features = np.loadtxt('output/devset_forensic_features.dat',
                                   delimiter=',', dtype=float)
    eff_forensic_topics = read_list('output/devset_eff_forensic_topics.dat')
    textual_features = np.loadtxt('output/devset_textual_features.dat',
                                  delimiter=',', dtype=float)
    eff_textual_topics = read_list('output/devset_eff_textual_topics.dat')

    real_mul_list = read_list('dataset_for_training/real_image_id.data')
    fake_mul_list = read_list('dataset_for_training/fake_image_id.data')
    mul_list = list(real_mul_list)
    mul_list.extend(fake_mul_list)

    topic_features = np.zeros((len(mul_list),forensic_features.shape[1] +
                               textual_features.shape[1]),dtype=float)
    topic_labels = np.zeros((len(mul_list),), dtype=int)
    used_ind = np.ones((len(mul_list),), dtype=bool)
    for ind,m in enumerate(mul_list):
        if m in eff_forensic_topics:
            ind1 = eff_forensic_topics.index(m)
            topic_features[ind,:forensic_features.shape[1]] = forensic_features[ind1]
        if m in eff_textual_topics:
            ind2 = eff_textual_topics.index(m)
            topic_features[ind, forensic_features.shape[1]:] = textual_features[ind2]
        if not (m in eff_forensic_topics or m in eff_textual_topics):
            used_ind[ind] = False

        label = 1
        if m in fake_mul_list:
            label = -1

        topic_labels[ind] = label

    # remove unused topic features
    topic_features = topic_features[used_ind,:]
    topic_labels = topic_labels[used_ind]

    detector_2 = None
    if classifier2 == 'logis':
        detector_2 = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier2 == 'svm':
        detector_2 = svm.SVC()
    elif classifier2 == 'randomforest':
        detector_2 = ExtraTreesClassifier(n_estimators=200, max_depth=None,
                                        min_samples_split=1, random_state=0)

    scaler_2 = preprocessing.StandardScaler().fit(topic_features)
    topic_features = scaler_2.transform(topic_features)
    detector_2.fit(topic_features, topic_labels)
    with open('output/RUN_3_classifier_2.pickle', 'wb') as handle:
        pickle.dump(detector_2, handle)
    with open('output/RUN_3_scaler_2.pickle', 'wb') as handle:
        pickle.dump(scaler_2, handle)

    print('Training statistics\n')
    print('Number of real tweets: ', sum(tweet_labels == 1))
    print('Number of fake tweets: ', sum(tweet_labels == -1))
    print('Number of real topics: ', sum(topic_labels == 1))
    print('Number of fake topics: ', sum(topic_labels == -1))


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
    train()
    test()



if __name__ == '__main__':
    main()