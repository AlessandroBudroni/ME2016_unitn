# Extracts all crawled text from keywords
# From text, calculate tf-idf and extract 100 keywords with highest scores
# Input: dataset {devset or testset}
# Output: a dictionary containing all sorted keywords


from sklearn.feature_extraction.text import TfidfVectorizer
import sys
sys.path.insert(0,'../Keywords_Extraction')
import extract_keywords_from_text as kwe
import sqlite3
import pickle

dataset = 'testset_subtask' # or test set

db1 = 'text_from_keywords.db'
db1_path = '../Text_Retrieval/dataset/' + dataset + '/' + db1

multimedia_detail = 'multimedia_details.csv'
multimedia_detail_path = '../Text_Retrieval/dataset/' + dataset + '/' + multimedia_detail

# connect to database
conn = sqlite3.connect(db1_path)
c = conn.cursor()

c.execute('SELECT DISTINCT event from website_from_keywords')
res = c.fetchall()

all_sorted_keywords = {}

for r in res:
    event_name = r[0]

    print('Processing event: ', event_name)

    c.execute('SELECT body from website_from_keywords  \
                         WHERE event = (?)', (event_name,))

    all_text = c.fetchall()

    corpus = []

    for text in all_text:
        cleaned_text = kwe.extract_clean_text(text[0])
        corpus.append(cleaned_text)

    vectorizer = TfidfVectorizer(max_features=100) # choose 100 best words
    vectorizer.fit_transform(corpus)

    idf = vectorizer.idf_
    unsorted_dict = dict(zip(vectorizer.get_feature_names(), idf))

    # sort the dictionary
    sorted_dict = sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)

    # extract 100 words
    all_sorted_keywords[event_name] = [s[0] for s in sorted_dict]

conn.close()


pickle.dump(all_sorted_keywords, open(dataset + "_all_sorted_keywords.p", "wb"))
