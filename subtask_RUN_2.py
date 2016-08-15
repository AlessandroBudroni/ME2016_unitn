from sklearn.cross_validation import  KFold
from sklearn import svm
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import csv

classifier = "randomforest"

def test():

    testing_file_detail = 'testset_subtask/data.txt'
    testing_eff_images = []
    with open(testing_file_detail, 'r') as f:
        headers = f.readline()
        lines = f.readlines()
        for l in lines:
            parts = l.split('\t')
            im_id = parts[0].strip('\n\t ')
            im_id = im_id.replace('.jpg', '')
            testing_eff_images.append(im_id)

    event_testset_details = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/testset_subtask/multimedia_details.csv'

    # load topic features
    forensic_features = np.loadtxt('output/testset_subtask_forensic_features.dat',
                                   delimiter=',', dtype=float)

    eff_forensic_topics = read_list('output/testset_subtask_eff_images.dat')
    textual_features = np.loadtxt('output/testset_subtask_textual_features.dat',
                                  delimiter=',', dtype=float)
    eff_textual_topics = read_list('output/testset_subtask_eff_textual_topics.dat')

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

    scaler = None
    with open('output/RUN_2_subtask_scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    detector = None
    with open('output/RUN_2_subtask_classifier.pickle', 'rb') as handle:
        detector = pickle.load(handle)

    topic_features = scaler.transform(topic_features)
    topic_pr = detector.predict(topic_features)

    print('\nResults of the 2nd RUN of subtask \n')

    for p in testing_eff_images:
        if p in mul_list:
            ind = mul_list.index(p)
            print(p, '\t', topic_pr[ind])
        else:
            print(p, ': unknown')

    with open('second_run_subtask.txt', 'w') as csvfile:
        fieldnames = ['image_id', 'prediction', 'explanation']
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()

        for p in testing_eff_images:
            if p in mul_list:
                ind = mul_list.index(p)
                p = p.strip('\n\t ')
                label = 'tampered'
                if topic_pr[ind] == 1:
                    label = 'non-tampered'
                writer.writerow({'image_id': p, 'prediction': label,
                                 'explanation': ''})
            else:
                writer.writerow({'image_id': p, 'prediction': 'unknown',
                                 'explanation': ''})


def train():

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

    detector = None
    if classifier == 'logis':
        detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier == 'svm':
        detector = svm.SVC()
    elif classifier == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=200, max_depth=None,
                                        min_samples_split=1, random_state=0)

    scaler = preprocessing.StandardScaler().fit(topic_features)
    topic_features = scaler.transform(topic_features)
    detector.fit(topic_features, topic_labels)
    with open('output/RUN_2_subtask_classifier.pickle', 'wb') as handle:
        pickle.dump(detector, handle)
    with open('output/RUN_2_subtask_scaler.pickle', 'wb') as handle:
        pickle.dump(scaler, handle)

    print('Training statistics\n')
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