import sys
import re
from bs4 import BeautifulSoup

dictionaryFile = "stopwords.txt";


def RemoveHTMLTags(source):
    soup = BeautifulSoup(source,'lxml')
    return soup.get_text()

def ReadStopWords():
    stop_words = set()
    with open(dictionaryFile) as f:
        lines = f.readlines()
    f.close()
    for line in lines:
        line = re.sub('\r\n','',line)
        stop_words.add(line)
    return stop_words


def RemoveJunkCharacters(source):
    # here I need to double check the @ before string present in c# version
    cleaned = re.sub('[^a-zA-Z0-9 \n.:_]', '', source)
    cleaned = re.sub(r'[.:,_^\s]',' ',cleaned)
    cleaned = re.sub(r'\b\d\b','',cleaned)
    cleaned = re.sub(r'\b\w{1}\b','',cleaned )
    return cleaned

def SplitWords(source):
    return source.split(' ')

def main():
    dict = {}
    outNoStopWord = []
    outNoHTML = []

    # load stop words
    stopWords = ReadStopWords();

    # read file html
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    for line in lines:
        cleanedLine = RemoveHTMLTags(line)
        cleanedLine = RemoveJunkCharacters(cleanedLine)

        if (len(cleanedLine) > 0):
            outNoHTML.append(cleanedLine)

        newLine = ''

        for subString in SplitWords(cleanedLine):
            if (len(subString) > 0):
                if (not (subString.lower() in stopWords)):
                    newLine = newLine + subString + ' '

                    if (not (subString.lower() in dict)):
                        dict[subString.lower()] = 1
                    else:
                        dict[subString.lower()] += 1;

        if (len(newLine) > 0):
            outNoStopWord.append(' '+newLine)

    # write files

    fnoHTML = open(sys.argv[1] + ".noHTML", "w")
    fnoStopWord = open(sys.argv[1] + ".noStopWord", "w")
    fKeyword = open(sys.argv[1] + ".keyword", "w")

    fnoHTML.writelines(outNoHTML)
    fnoStopWord.writelines(outNoStopWord)

    fnoHTML.close()
    fnoStopWord.close()

    # Sort by value

    # Here I should skip the first pair

    sumWords = sum(dict.values())
    freq = []

    for key, value in sorted(dict.items(), key=lambda x: x[1], reverse=True):
        freq.append(key + ', ' + str(1.0 * value / sumWords)+'\n')

    fKeyword.writelines(freq)


if __name__ == '__main__':
    main()
