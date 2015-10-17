#!usr/bin/python
# encoding=utf-8
# coding=utf-8
import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import time
import csv,cStringIO,codecs
import jieba
from predict import init_api,make_prediction

"""Main Activity to answer question for user"""
# TODO:improve the Machine Learning Model by user feedback.

mydict = {} #question database

# Get default English stopwords and extend with punctuation
stopwords = [u'／', u'，', u'。', u'、', u'；', u'：', u'？', u'「', u'」']
stopwords.extend(string.punctuation)

# List the feature that matched for each question.
def list_feature(question,features,api,mydict,DBG):
    start_time = time.time()
    jieba.load_userdict('bankdict.txt')
    tokens_b = [token.strip(string.punctuation) for token in jieba.cut_for_search(question) if (token.strip(string.punctuation) not in stopwords)]
    f = [0]*len(features)
    #f_demo  = []
    for token in tokens_b:
        if token in features:
            f[features.index(token)]=1
            #f_demo.append(token)
    #print f_demo,'for "',question,'"'
    #print f
    elapsed_time = time.time() - start_time
    if DBG:
        print 'Execution local time : %.3f' % (elapsed_time)

    label = make_prediction(api,f)
    if label not in mydict:
        print "Sorry, I don't understand your question."
    else:
        if DBG:
            print 'You are asking :',mydict[label]
        elapsed_time = time.time() - start_time
        if DBG:
            print 'Execution total time : %.3f' % (elapsed_time)
    #return f

# Setting up the features for later matching.
def init():
    features = []
    with open('question_chinese.csv', mode='r') as file:
        reader = UnicodeReader(file)
        for row in reader:
            features = row[1:]
            break
    file.close()
    #print '\nfeatures are',features
    return features

def main():
    features = init()
    api = init_api()
    #Read the question database
    with open('raw_question_chinese.csv', mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    file.close()
    #print mydict
    print ("\n").join(mydict.values())
    #Make a predicition in initial stage so the later predicitions will be faster by 10x
    list_feature(mydict['20'],features,api,mydict,False)

    #Start answering question
    while True:
        question = raw_input("\nAsk me a question : ")
        list_feature(question,features,api,mydict,True)

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

if __name__ == '__main__':
    main()
