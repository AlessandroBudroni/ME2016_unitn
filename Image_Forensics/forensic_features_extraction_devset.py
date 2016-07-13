# This script extract forensic features from /matlab folder
# save forensic features without labels to ../output
# then assign labels to them and save here
# only work with devset since it involves label processing


import csv
import numpy as np

dataset = 'devset'

post_detail_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL\
/image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'

media_detail_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/' + \
                    dataset + '/multimedia_details.csv'

dict = {}
with open(media_detail_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mul_id = row['mul_id'].strip("\n\t ")
        # dict[media_id] = [number of real tweets = 0, number of fake tweets = 0, numeric_labels]
        dict[mul_id] = [0,0,0]

# Open file
f = open(post_detail_file, 'r')
header = f.readline()

for line in f:
    columns = line.split('\t')
    medias = str.split(columns[3],',')
    for m in medias:
        m = m.strip("\t\n ")
        if m in dict:
            if columns[6].strip("\t\n ") == 'real':
                l = dict[m]
                l[0] += 1
                dict[m] = l
            else:
                l = dict[m]
                l[1] += 1
                dict[m] = l
f.close()

# there are topics that are not used
# save only topics which are used on the dataset
with open(dataset + '_topic_labels.csv', 'w') as csvfile:
    fieldnames = ['mul_id', 'label']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for m in dict:
        l = dict[m]
        if l[0]  != 0 or l[1] != 0:
            label = 'real'
            l[2] = 1
            if l[1] > l[0]:
                label = 'fake'
                l[2] = -1
            writer.writerow({'mul_id' : m, 'label' : label})

# Extract forensic features and assign labels, ignore videos
features = np.loadtxt('matlab/'+ dataset + '_forensic_features.dat', delimiter = ',')
numeric_labels = np.zeros((features.shape[0],1), dtype=int)

with open('matlab/' + dataset + '_eff_forensic_topics.dat', 'r') as f:

    count = 0
    used_media_indx = np.zeros((features.shape[0],),dtype = bool)
    effective_topics = []

    for line in f:
        mul_id = line.strip('\n\t ')
        l = dict[mul_id]
        print(mul_id, ':', l)
        numeric_labels[count,0] = l[2]
        if l[0]  != 0 or l[1] != 0:
            used_media_indx[count,] = True
            effective_topics.append(mul_id)
        count += 1

# save unlabelled topics to /output
np.savetxt('../output/' + dataset + '_forensic_features.dat',
           features[used_media_indx], delimiter=',')

# save effective forensic topics
f = open('../output/' + dataset + '_eff_forensic_topics.dat', 'w')
for topic in effective_topics:
    f.write(topic + '\n')
f.close()

# add label and save here
features = np.append(features, numeric_labels, axis = 1)

# remove topics that are not labelled
features = features[used_media_indx]

np.savetxt(dataset + '_forensic_features.dat', features, delimiter = ',')
f.close()

# save effective forensic topics
f = open(dataset + '_eff_forensic_topics.dat','w')
for topic in effective_topics:
    f.write(topic + '\n')
f.close()
