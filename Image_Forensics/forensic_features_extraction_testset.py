# This script extract forensic features from /matlab folder
# save forensic features without labels to ../output
# only work with testset

import csv
import numpy as np

dataset = 'testset'

post_detail_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL\
/image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'

media_detail_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/' + \
                    dataset + '/multimedia_details.csv'

# Extract forensic features, ignore videos
features = np.loadtxt('matlab/'+ dataset + '_forensic_features.dat', delimiter = ',')
effective_topics = []
with open('matlab/'+ dataset + '_eff_forensic_topics.dat', 'r') as f:
    for line in f:
        line = line.strip('\n\t ')
        effective_topics.append(line)

# save unlabelled topics to /output
np.savetxt('../output/' + dataset + '_forensic_features.dat',
           features, delimiter=',')

# save effective forensic topics
f = open('../output/' + dataset + '_eff_forensic_topics.dat', 'w')
for topic in effective_topics:
    f.write(topic + '\n')
f.close()
