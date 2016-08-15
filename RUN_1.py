from sklearn.cross_validation import  KFold
from sklearn import svm
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import sys
sys.path.insert(0, 'Text_Retrieval')
import csv

classifier1 = "randomforest"
classifier2 = "randomforest"

def test():

    tweet_features = np.loadtxt('output/testset_tweet_features.dat', delimiter=',')
    eff_tweets = read_list('output/testset_eff_posts.dat')
    event_testset_details = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/testset/multimedia_details.csv'

    scaler_1 = None
    with open('output/RUN_1_scaler_1.pickle', 'rb') as handle:
        scaler_1 = pickle.load(handle)

    detector_1 = None
    with open('output/RUN_1_classifier_1.pickle', 'rb') as handle:
        detector_1 = pickle.load(handle)

    tweet_features = scaler_1.transform(tweet_features)

    tweet_pr = detector_1.predict(tweet_features)

    print('\nResults of the 1st RUN \n')
    print('Sum of real:', sum(tweet_pr == 1))
    for ind,p in enumerate(eff_tweets):
       print(p, '\t', tweet_pr[ind])

    with open('first_run.txt', 'w') as csvfile:
        fieldnames = ['post_id', 'prediction', 'explanation']
        writer = csv.DictWriter(csvfile, delimiter = '\t', fieldnames=fieldnames)
        writer.writeheader()
        for ind, p in enumerate(eff_tweets):
            label = 'fake'
            if tweet_pr[ind] == 1:
                label = 'real'
            writer.writerow({'post_id':p, 'prediction':label,
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
    with open('output/RUN_1_classifier_1.pickle', 'wb') as handle:
        pickle.dump(detector, handle)
    with open('output/RUN_1_scaler_1.pickle', 'wb') as handle:
        pickle.dump(scaler_1, handle)

    print('Training statistics\n')
    print('Number of real tweets: ', sum(tweet_labels == 1))
    print('Number of fake tweets: ', sum(tweet_labels == -1))


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