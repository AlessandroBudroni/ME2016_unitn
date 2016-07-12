import sys
import re
import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

dictionaryFile = "stopwords.txt"


def RemoveHTMLTags(source):
    soup = BeautifulSoup(source, 'lxml')
    return soup.get_text()

def ReadStopWords():
    stop_words = set()
    with open(dictionaryFile) as f:
        lines = f.readlines()
    f.close()
    for line in lines:
        line = re.sub('\r\n', '', line)
        line = re.sub('\n', '', line)
        stop_words.add(line)
    return stop_words


def RemoveJunkCharacters(source):
    # here I need to double check the @ before string present in c# version
    cleaned = re.sub('[^a-zA-Z0-9 \n.:_]', '', source)
    cleaned = re.sub(r'[.:,_^\s]', ' ', cleaned)
    cleaned = re.sub(r'\b\d\b', '', cleaned)
    cleaned = re.sub(r'\b\w{1}\b', '', cleaned)
    return cleaned


def SplitWords(source):
    return source.split(' ')

def tag(sentence, num=0):
    #remove symbols
    import string
    for char in string.punctuation:
        sentence = sentence.replace(char, ' ')
    all_words = sentence.lower().split()
    # Create a frequency distribution
    stop_words = set(stopwords.words('english'))
    stemmer = SnowballStemmer("english")
    clean_words = [stemmer.stem(w) for w in all_words if not stemmer.stem(w) in stop_words]
    freq_clean  = nltk.FreqDist(clean_words)
    terms=[]
    freqs = []
    if freq_clean.__len__() != 0:
        if num != 0:
            mc = freq_clean.most_common(num)
        else:
            mc = freq_clean.most_common(freq_clean.__len__())

        for w in mc:
            terms.append(w[0])
            freqs.append(w[1])

    return (terms, freqs)

def extract_keywords_from_text(text):
    dict = {}

    # load stop words
    stopWords = ReadStopWords()

    cleanedText = RemoveJunkCharacters(text)

    noStopWordText = ''

    for subString in SplitWords(cleanedText):
        if (len(subString) > 0):
            if (not (subString.lower() in stopWords)):
                noStopWordText = noStopWordText + subString + ' '

                if (not (subString.lower() in dict)):
                    dict[subString.lower()] = 1
                else:
                    dict[subString.lower()] += 1

    keywords = []
    freq = []

    for key, value in sorted(dict.items(), key=lambda x: x[1], reverse=True):
        keywords.append(key)
        freq.append(1.0 * value)

    return (keywords, freq)
