from sklearn.cross_validation import  KFold
from sklearn import svm
from sklearn.linear_model import LogisticRegression as logis
from sklearn import preprocessing
import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score
import csv

classifier = 'randomforest'

def train():

    training_file_detail = 'devset_subtask/data.txt'
    img_dict = {}

    with open(training_file_detail, 'r') as f:
        headers = f.readline()
        lines = f.readlines()
        for l in lines:
            parts = l.split('\t')
            im_id = parts[0].strip('\n\t ')
            im_id = im_id.replace('.jpg','')
            label = parts[2].strip('\n\t ')
            if label == 'non-tampered':
                img_dict[im_id] = 1
            else:
                img_dict[im_id] = -1

    forensic_eff_images = None
    with open('output/devset_subtask_eff_images.dat') as f:
        forensic_eff_images = f.readlines()

    labels = np.zeros((len(forensic_eff_images),), dtype=int)
    for ind,im in enumerate(forensic_eff_images):
        im = im.strip('\n\t ')
        labels[ind] = img_dict[im]

    data = np.loadtxt('output/devset_subtask_forensic_features.dat', delimiter=',', dtype=float)

    X_train = data
    y_train = labels

    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    with open('output/RUN_1_subtask_scaler.pickle', 'wb') as handle:
        pickle.dump(scaler, handle)

    detector = None
    if classifier == 'logis':
        detector = logis(C=1e5, solver='liblinear', multi_class='ovr')
    elif classifier == 'svm':
        detector = svm.SVC()
    elif classifier == 'randomforest':
        detector = ExtraTreesClassifier(n_estimators=200, max_depth=None,
                                        min_samples_split=1, random_state=0)

    detector.fit(X_train, y_train)

    with open('output/RUN_1_subtask_classifier.pickle', 'wb') as handle:
        pickle.dump(detector, handle)





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

    forensic_eff_images = read_list('output/testset_subtask_eff_images.dat')

    data = np.loadtxt('output/testset_subtask_forensic_features.dat', delimiter=',', dtype=float)

    X_test = data

    scaler = None
    with open('output/RUN_1_subtask_scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    X_test = scaler.transform(X_test)

    detector = None
    with open('output/RUN_1_subtask_classifier.pickle', 'rb') as handle:
        detector = pickle.load(handle)

    pr_labels = detector.predict(X_test)

    print('\nResults of the 1st RUN of subtask \n')

    for p in testing_eff_images:
        if p in forensic_eff_images:
            ind = forensic_eff_images.index(p)
            print(p, '\t', pr_labels[ind])
        else:
            print(p, ': unknown')

    with open('first_run_subtask.txt', 'w') as csvfile:
        fieldnames = ['image_id', 'prediction', 'explanation']
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()

        for p in testing_eff_images:
            if p in forensic_eff_images:
                ind = forensic_eff_images.index(p)
                p = p.strip('\n\t ')
                label = 'tampered'
                if pr_labels[ind] == 1:
                    label = 'non-tampered'
                writer.writerow({'image_id': p, 'prediction': label,
                                 'explanation': ''})
            else:
                writer.writerow({'image_id': p, 'prediction': 'unknown',
                                 'explanation': ''})

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