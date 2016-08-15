import numpy as np
import pickle

dataset = 'testset'

post_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
                    'image-verification-corpus-master/mediaeval2016/' + dataset + '/posts.txt'

post_feature_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
                    'image-verification-corpus-master/mediaeval2016/'+ dataset + \
                    '/dataset_features/post_features.txt'

user_feature_file = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/' \
                    'image-verification-corpus-master/mediaeval2016/' + dataset + \
                    '/dataset_features/user_features.txt'

# make a dictionary to link multimedia ID and post ID, label
posts = {}
with open(post_file) as f:
    headers = f.readline()
    for line in f:
        line.strip('\n\t ')
        parts = line.split('\t')
        id = parts[0].strip('\n\t ')
        medias = parts[4].split(',')

        posts[id] = medias[0].strip('\n\t ')

# save post dictionary
with open('../output/' + dataset + '_posts_dict.pickle', 'wb') as handle:
    pickle.dump(posts, handle)

# load post features
data = {}
with open(post_feature_file) as f:
    headers = f.readline()
    for line in f:
        line = line.strip('\n\t ')
        parts = line.split(',')
        id = parts[0].strip('\n\t ')
        feature_ = parts[1:]
        for index,f in enumerate(feature_,start=0):
            if f == 'false':
                feature_[index] = '0'
            elif f == 'null':
                feature_[index] = '-1'
            elif f == 'true':
                feature_[index] = '1'

        data[id] = feature_

# load user features and concatenate with post feature
with open(user_feature_file) as f:
    headers = f.readline()
    for line in f:
        line = line.strip('\n\t ')
        parts = line.split(',')
        id = parts[0].strip('\n\t ')
        feature_ = parts[1:]
        for index,f in enumerate(feature_,start=0):
            if f == 'false':
                feature_[index] = '0'
            elif f == 'null':
                feature_[index] = '-1'
            elif f == 'true':
                feature_[index] = '1'

        feature_.extend(data[id])
        data[id] = feature_

# get post IDs
post_ids = list(data.keys())
features = [data[k] for k in post_ids]

features = np.array(features, dtype=float)

np.savetxt('../output/' + dataset + '_tweet_features.dat', features, delimiter=',')
with open('../output/' + dataset + '_eff_posts.dat', 'w') as f:
    for p in post_ids:
        f.write(p+'\n')