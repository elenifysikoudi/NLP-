import sys
import os
import argparse
import math
from loader import load_dir
from collections import Counter
import nltk
import pandas
from nltk.corpus import brown
import random

def load_data(rootdir):
    '''
    Loads all the data by searching the given directory for
    subdirectories, each of which represent a class.  Then returns a
    dictionary of class vs. text document instances.
    '''

    classdict = {}
    for classdir in os.listdir(rootdir):
        fullpath = os.path.join(rootdir, classdir)
        print("Loading from {}.".format(fullpath))
        if os.path.isdir(fullpath):
            classdict[classdir] = load_dir(fullpath)
    return classdict

def calc_prob(classdict, classname, word):
    '''
    Calculates p(classname|word) given the corpus in classdict.
    '''
    all_words_in_genre = []
    for lyric in classdict[classname]:
        for every_word in lyric:
            all_words_in_genre.append(every_word)
            no_of_words = len(all_words_in_genre)
    #print(no_of_words)
    word_freq = dict(nltk.probability.FreqDist(all_words_in_genre))
    #print(word_freq)
    count_in_genre = word_freq[word]
    #print(count_in_genre)
    probability = count_in_genre/no_of_words   
    print(probability)
    return probability

def calc_prob_bigram(classdict, classname, w1, w2):

    for lyric in classdict[classname]:
        bigrams = list(nltk.bigrams(lyric))
        frequency = nltk.probability.ConditionalFreqDist(bigrams)
        probab = frequency[w1].freq(w2)

    return probab

#Since there was ambiguousness I decided for the rest of the functions to count 
#the words of the whole corpus,Pop and Metal seperately so all of them are available.
#I understand that this makes my code super long and perhaps the results as well but I wanted to have all.

def count_words(data):
    count_all_corpus = 0
    for song in data.values():
        for lyric in song:
            for word in lyric:
                count_all_corpus+=1
    count_Pop = 0
    for lyric in data['Pop']:
        for word in lyric:
            count_Pop+=1
    count_Metal = 0
    for lyric in data['Metal']:
        for word in lyric:
            count_Metal+=1

    return count_all_corpus, count_Pop, count_Metal

def count_unique_words(data):
    unique_words = {}
    no_of_unique_words_all_corpus=0
    for song in data.values():
        for lyric in song:
            for word in lyric:
                if word not in unique_words:
                    no_of_unique_words_all_corpus+=1
                    unique_words[word]= 1
                unique_words[word]+=1 

    unique_words_Pop = {}
    no_of_unique_words_Pop = 0
    for lyric in data['Pop']:
        for word in lyric:
            if word not in unique_words_Pop:
                no_of_unique_words_Pop+=1
                unique_words_Pop[word]=0
            unique_words_Pop[word]+=1
    
    unique_words_Metal={}
    no_of_unique_words_Metal = 0
    for lyric in data['Metal']:
        for word in lyric:
            if word not in unique_words_Metal:
                no_of_unique_words_Metal+=1
                unique_words_Metal[word]=0
            unique_words_Metal[word]+=1

    return no_of_unique_words_all_corpus, no_of_unique_words_Pop, no_of_unique_words_Metal

def most_frequent_words(data):
    words_all_corpus = []
    for song in data.values():
        for lyric in song:
            for word in lyric:
                words_all_corpus.append(word)
    most_frequent_words_all_corpus=Counter(words_all_corpus).most_common(10)

    words_Pop = []
    for lyric in data['Pop']:
        for word in lyric:
            words_Pop.append(word)
    most_frequent_words_Pop = Counter(words_Pop).most_common(10)

    words_Metal=[]
    for lyric in data['Metal']:
        for word in lyric:
            words_Metal.append(word)
    most_frequent_words_Metal = Counter(words_Metal).most_common(10)

    return most_frequent_words_all_corpus, most_frequent_words_Pop, most_frequent_words_Metal

def bigram(data):
    bigram_pairs_all_corpus = {}
    for song in data.values():
        for lyric in song:
            bigrams = tuple(zip(lyric,lyric[1:]))
            for pair in bigrams:
                if pair not in bigram_pairs_all_corpus:
                    bigram_pairs_all_corpus[pair]= 0
                bigram_pairs_all_corpus[pair]+=1
    top20_pairs_all_corpus=Counter(bigram_pairs_all_corpus).most_common(20)

    bigram_pairs_Pop={}
    for lyric in data['Pop']:
        bigrams_Pop = tuple(zip(lyric,lyric[1:]))
        for pair in bigrams_Pop:
            if pair not in bigram_pairs_Pop:
                bigram_pairs_Pop[pair]= 0
            bigram_pairs_Pop[pair]+=1
    top20_pairs_Pop=Counter(bigram_pairs_Pop).most_common(20)

    bigram_pairs_Metal={}
    for lyric in data['Metal']:
        bigrams_Metal = tuple(zip(lyric,lyric[1:]))
        for pair in bigrams_Metal:
            if pair not in bigram_pairs_Metal:
                bigram_pairs_Metal[pair]= 0
            bigram_pairs_Metal[pair]+=1
    top20_pairs_Metal=Counter(bigram_pairs_Metal).most_common(20)

    return top20_pairs_all_corpus, top20_pairs_Pop , top20_pairs_Metal

def ngram(data,n):
    ngram_counts_all_corpus = {}
    for song in data.values():
        for lyric in song:
            for i in range(len(lyric)-n+1):
                ngrams = tuple(lyric[i:i+n])
                if ngrams not in ngram_counts_all_corpus:
                    ngram_counts_all_corpus[ngrams] = 0
            
                ngram_counts_all_corpus[ngrams] += 1

    ngram_counts_Pop={}
    for lyric in data['Pop']:
        for i in range(len(lyric)-n+1):
            ngram_Pop = tuple(lyric[i:i+n])
            if ngram_Pop not in ngram_counts_Pop:
                ngram_counts_Pop[ngram_Pop] = 0
            
            ngram_counts_Pop[ngram_Pop] += 1

    ngram_counts_Metal={}
    for lyric in data['Metal']:
        for i in range(len(lyric)-n+1):
            ngram_Metal = tuple(lyric[i:i+n])
            if ngram_Metal not in ngram_counts_Metal:
                ngram_counts_Metal[ngram_Metal] = 0
            
            ngram_counts_Metal[ngram_Metal] += 1

    return ngram_counts_all_corpus, ngram_counts_Pop, ngram_counts_Metal

#This is my attempt for the VG part of the assignment. It takes quite a lot
#of time to run the program I didn't know how to make this faster.

def pos_tagger(data):
    train_size= int(len(data)*0.8)
    train_set_unedited= data[:train_size]
    test_set_unedited = data[train_size:]
    test_set = [(t[0].lower(), t[1]) for t in test_set_unedited]
    train_set = [(t[0].lower(), t[1]) for t in train_set_unedited]

    train_set_count ={}
    for word in train_set:
        if word not in train_set_count:
            train_set_count[word]=0
        train_set_count[word]+=1
        
    word_tag_count={}
    for word_tag, count in train_set_count.items():
        word = word_tag[0]
        tag = word_tag[1]
        if word not in word_tag_count:
            word_tag_count[word]={}
        if tag not in word_tag_count[word]:
            word_tag_count[word][tag] = count
        else:
         word_tag_count[word][tag] += count
    
   
    for word,tags in word_tag_count.items():
        if len(tags)>1:
           combined_count = sum(tags.values())
           tags['combined']= combined_count
    #print(dict(list(word_tag_count.items())[:30]))

    probab_tag={}
    for word,tags in word_tag_count.items():
        for tag,count in word_tag_count[word].items():
            if word not in probab_tag:
                probab_tag[word]= {}
            if tag!= 'combined':
                if tag not in probab_tag[word]:
                    if len(tags)>1:
                        total_count = tags['combined']
                        probab_tag[word][tag]=count/total_count
                    else:
                        #total_count = count
                        probab_tag[word][tag]= 1.0
    #print(dict(list(probab_tag.items())[:30]))

    test_set_test_tags = {}
    test_words =[]
    for word in test_set:
        test_words.append(word[0])
    for train_word in probab_tag.keys():
        for test_word in test_words:
            unknown_tag = 'NN'
            if test_word not in test_set_test_tags:
                    test_set_test_tags[test_word] = unknown_tag
            if test_word == train_word:
                probabilistic_tag = max(probab_tag[train_word], key=probab_tag[train_word].get)
                test_set_test_tags[test_word] = probabilistic_tag
                
    model_tags = []
    for word,tag in test_set_test_tags.items():
       model_tags.append((word,tag)) 


    correctly_classified = 0
    all_classified = len(test_set)

    for word in test_set:
        if word in model_tags:
            correctly_classified+=1

    print(correctly_classified)
    print(all_classified)
    accuracy = correctly_classified/all_classified
    return accuracy



if __name__ == "__main__":

    '''
    Entry point for the code. We load the command-line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("filesdir", help="The root directory containing the class directories and text files.")
    parser.add_argument("classname", help="The class of interest.")
    parser.add_argument("feature", help="The word of interest for calculating -log2 p(class|feature).")
    args = parser.parse_args()

    corpus = load_data(args.filesdir)

    print("Number of classes in corpus: {}".format(len(corpus)))
    
    print("Looking up probability of class {} given word {}.".format(args.classname, args.feature))
    prob = calc_prob(corpus, args.classname, args.feature)
    if prob == 0:
        print("-log2 p({}|{}) is undefined.".format(args.classname, args.feature))
    else:
        print("-log2 p({}|{}) = {:.3f}".format(args.classname, args.feature, -math.log2(prob)))
    

    # print(count_words(corpus))
    # print(count_unique_words(corpus))
    # print(most_frequent_words(corpus))
    # print(bigram(corpus))
    # print(ngram(corpus,3))
    # print(calc_prob_bigram(corpus,'Pop',"'", "t"))
    brown_corpus = brown.tagged_words(tagset='universal')
    print(pos_tagger(brown_corpus))