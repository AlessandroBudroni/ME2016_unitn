# Extract textual features from crawled data
# This script only works on the devset since it involves label processing
# Output: textual features and their corresponding multimedia name
# Out duplicated output without labels will be saved in ../output

import csv
import sqlite3
import sys
sys.path.insert(0,'../Keywords_Extraction')
import extract_keywords_from_text as kwe
import pickle
import numpy as np
from nltk.stem.snowball import SnowballStemmer

dataset = 'devset'

db2 = 'text_from_media.db'
db2_path = '../Text_Retrieval/dataset/' + dataset + '/' + db2

multimedia_detail = 'multimedia_details.csv'
multimedia_detail_path = '../Text_Retrieval/dataset/' + dataset + '/' + multimedia_detail

all_sorted_dict = pickle.load(open(dataset + "_all_sorted_keywords.p", "rb"))

stemmer = SnowballStemmer("english")

# connect to database
conn = sqlite3.connect(db2_path)
c = conn.cursor()


# read labels of topics
label_dict = {}

with open('../Image_Forensics/' + dataset + '_topic_labels.csv') as csvfileDetail:
    reader = csv.DictReader(csvfileDetail)
    for row in reader:
        mul_id = row['mul_id'].strip("\n\t ")
        str_label = row['label']
        label_dict[mul_id] = 1
        if str_label == 'fake':
            label_dict[mul_id] = -1



# load positive words
pos_words = []

with open('positive_sentinent_words.txt') as f:
    for line in f:
        line = line.strip("\t\n ")
        stemmed = stemmer.stem(line)
        pos_words.append(stemmed)

# load negative words
neg_words = []
with open('negative_sentinent_words.txt') as f:
    for line in f:
        line = line.strip("\t\n ")
        stemmed = stemmer.stem(line)
        neg_words.append(stemmed)

# load "fake" words
fake_words = []
with open('keywords_fake_news.txt') as f:
    for line in f:
        line = line.strip("\t\n ")
        stemmed = stemmer.stem(line)
        fake_words.append(stemmed)

pos_counting_dict = dict((el, 0.0) for el in pos_words)
neg_counting_dict = dict((el, 0.0) for el in neg_words)
fake_counting_dict = dict((el, 0.0) for el in fake_words)

effective_topics = []

with open(multimedia_detail_path) as csvfileDetail:
    reader = csv.DictReader(csvfileDetail)

    features = []

    for row in reader:
        mul_id = row['mul_id'].strip("\n\t ")

        print('Processing media file: ', mul_id)

        type = row['type']
        event_name = row['event_name']
        abs_path = row['abs_path']

        tfidf_sorted_keywords = all_sorted_dict[event_name]

        c.execute('SELECT body FROM website_from_img \
                  WHERE mul_id = (?)', (mul_id,))

        all_text = c.fetchall()
        ndocuments = len(all_text)

        tfidf_counting_dict = dict((el, 0.0) for el in tfidf_sorted_keywords)

        for text in all_text:
            cleaned_text = kwe.extract_clean_text(text[0])

            for word in kwe.SplitWords(cleaned_text):
                if word in pos_words:
                    pos_counting_dict[word] += 1
                if word in neg_words:
                    neg_counting_dict[word] += 1
                if word in fake_words:
                    fake_counting_dict[word] += 1
                if word in tfidf_sorted_keywords:
                    tfidf_counting_dict[word] += 1

        # check if this topic is labelled and correctly crawled
        if ndocuments != 0 and mul_id in label_dict:
            # divided by ndocuments to avoid dominating in number of documents
            feature = [float(sum(pos_counting_dict.values())) / ndocuments, \
                       float(sum(neg_counting_dict.values())) / ndocuments]

            feature.extend(float(fake_counting_dict[kw]) / ndocuments for kw in fake_words)

            feature.extend(float(tfidf_counting_dict[kw]) / ndocuments for kw in tfidf_sorted_keywords)

            feature.append(label_dict[mul_id])

            features.append(feature)

            effective_topics.append(mul_id)

        # reset all values in dictionaries
        pos_counting_dict = pos_counting_dict.fromkeys(pos_counting_dict, 0.0)
        neg_counting_dict = neg_counting_dict.fromkeys(neg_counting_dict, 0.0)
        fake_counting_dict = fake_counting_dict.fromkeys(fake_counting_dict, 0.0)

    features = np.array(features, dtype=float)

    np.savetxt(dataset + '_textual_features.dat', features, delimiter=',')

    with open(dataset + '_eff_textual_topics.dat', 'w') as f:
        for topic in effective_topics:
            f.write(topic + '\n')

    # remove labels and save to /output
    features = features[:,:-1]
    np.savetxt('../output/' + dataset + '_textual_features.dat', features, delimiter=',')

    with open('../output/' + dataset + '_eff_textual_topics.dat','w') as f:
        for topic in effective_topics:
            f.write(topic + '\n')


conn.close()