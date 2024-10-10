import os
import glob
import sys
from nltk.tokenize import WordPunctTokenizer

### Utility function, do not modify this file.
def load_dir(dirname):
    '''
    Loads all the files in a directory into a list of lists of tokens, one
    list per file. Tokenizes.
    '''
    wpt = WordPunctTokenizer()

    lists = []
    for filename in glob.glob('{}/*.txt'.format(dirname)):
        words = []
        with open(filename, "r") as textfile:
            for line in textfile.readlines():
                words += [word.lower() for word in wpt.tokenize(line)]
        lists.append(words)
        

    return lists

            
