import numpy as np
import pickle

dataset = 'devset'

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
        medias = parts[3].split(',')
        label = '1'
        if parts[6].strip('\n\t ') == 'fake':
            label = '-1'

        posts[id] = [medias[0].strip('\n\t '), label]

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
            if f == 'null':
                feature_[index] = '-1'
            if f == 'true':
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
            if f == 'null':
                feature_[index] = '-1'
            if f == 'true':
                feature_[index] = '1'

        feature_.extend(data[id])
        feature_.append(posts[id][1])
        data[id] = feature_

# get post IDs
post_ids = list(data.keys())
features = [data[k] for k in post_ids]
for k in post_ids:
    if len(data[k]) != 26:
        print(k)
features = np.array(features, dtype =float)


np.savetxt('../output/' + dataset + '_tweet_features.dat', features, delimiter=',')
with open('../output/' + dataset + '_eff_posts.dat', 'w') as f:
    for p in post_ids:
        f.write(p+'\n')