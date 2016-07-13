from nltk.stem.snowball import SnowballStemmer

f = open('keywords_fake_news.txt')
stemmer = SnowballStemmer("english")
for line in f:
    print(line)
    words = line.split('|')
    for w in words:
        w = w.strip('\n\t ')
        print(stemmer.stem(w))


