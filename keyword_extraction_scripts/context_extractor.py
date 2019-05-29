
# coding: utf-8

# In[80]:


import pandas as pd
import json
import re
import os
import string
import random
import nltk
import math
import numpy as np
import pickle
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer


# In[85]:


nltk.download('words')


# In[14]:


def loadStopWords(filePath):
    
    with open(filePath, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)
    


# In[15]:


def nltkToWordnet(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# In[16]:


def lemmatize(tokens):
    tagged = nltk.pos_tag(tokens)
    words, tags = zip(*tagged)
    wordNetTags = []
    for i in range(0, len(tags)):
        wordNetTags.append(nltkToWordnet(tags[i]))
        
    lem = WordNetLemmatizer()
    
    lemmatizedTokens = []
    
    for i in range(0, len(tokens)):
        #if wordNetTags[i] is None:
            #lemmatizedTokens.append(lem.lemmatize(tokens[i]))
        if wordNetTags[i] is wordnet.NOUN:
            lemmatizedTokens.append(lem.lemmatize(tokens[i], wordNetTags[i]))
            
    return lemmatizedTokens
    


# In[17]:


def preProcess(text):
     # lowercase
    text=text.lower()
    
    #remove tags
    text=re.sub("</?.*?>"," <> ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
     
    # remove punctuation
    text = text.translate(str.maketrans('','',string.punctuation))    
    
    # load stopwords
    stopWords = loadStopWords('stopwords.txt')
    
    # remove stopwords
    for w in stopWords:
        pattern = r'\b' + w + r'\b'
        text = re.sub(pattern, '', text)
    
    #tokenization
    tokens = nltk.word_tokenize(text)
    
    # lemmatization
    tokens = lemmatize(tokens) 
    
    
    return tokens


# In[18]:


def getAllRelevantSections(currPaper):
    currPaper['text'] = ""
    
    if "abstractText" in currPaper:
        currPaper['text'] = currPaper['text'] + currPaper['abstractText']
        
    if "title" in currPaper:
        currPaper['text'] = currPaper['text'] + currPaper['title']
        
    if "sections" in currPaper:
         for section in currPaper['sections'][0]:
            currPaper['text'] = currPaper['text'] + section['text']
    
    currPaper['text'] = [preProcess(currPaper['text'][0])]
    
    return currPaper['text']


# In[7]:


def loadPapers():
    errorPapers = 0
    papers = []
    
    index = 0
    directory = os.fsencode('data/json/')
    all_files = [file.decode('ascii') for file in os.listdir(directory)]
    while True:
        if str(index)+'.json' not in all_files:
            break

        currPaper = pd.read_json('data/json/' + str(index) + '.json', lines = True)

        if currPaper["id"].empty or "sections" not in currPaper:
            errorPapers += 1

        else:
            currPaper['text'] = getAllRelevantSections(currPaper)
            papers.append(currPaper['text'])
        index = index + 1
    print(errorPapers, len(papers))
    print(papers[0])
    
    with open('papers', 'wb') as fp:
        pickle.dump(papers, fp)
     


# In[8]:


loadPapers()


# In[19]:


def readPapers():
    with open ('papers', 'rb') as fp:
        papers = pickle.load(fp)
    return papers


# In[20]:


readPapers()


# In[21]:


documentCountForWord = dict()
# for each word it tells how many unique documents contain that word


# In[22]:


# this function builds documentCountForWord iteratively.
def countVectorizer(listOfWords):
    setOfWords = set(listOfWords)
    # taking set will increase the count of each word by 1 for each document
    for word in setOfWords:
        documentCountForWord[word] = documentCountForWord.get(word, 0) + 1
        # get has been used because python doesn't have static types like c++
        # if the word is not present it'll not know it has to return 0


# In[23]:


def calculateTF(listOfWords, numberOfDocuments):
    
    wordCount = dict()
    # for a listOfwords it tells the count of each word
    for word in listOfWords:
        wordCount[word] = wordCount.get(word, 0) + 1
    tf = dict()
    for word in wordCount.keys():
        tf[word] = wordCount[word]/len(listOfWords)
    # please check the formula
    return tf


# In[24]:


def calculateTFIDF(paper, numberOfDocuments):
    tf = calculateTF(paper, numberOfDocuments)
    tfidf = dict()
    for word in tf.keys():
        tfidf[word] = tf[word] * math.log(float(numberOfDocuments)/documentCountForWord[word])
        # check the formula, there are many variants in wiki
    return tfidf    


# In[25]:


def findKeywords():
    #firstly build the documentCountForWord 
    papers = readPapers()
    numberOfDocuments = len(papers)

    for paper in papers:
        countVectorizer(paper[0])
    tfidf = dict()
    numberOfTopKeywords = 10  #how many keywords you want from each doc
    topKeywordsForPapers = []
    tfidfAllPapers = []

    for paper in papers:
        tfidf = calculateTFIDF(paper[0], numberOfDocuments)
        keywords = []
        for i in sorted(tfidf.items(),reverse = True,key = lambda key_value: (key_value[1], key_value[0]))[:numberOfTopKeywords]:
            keywords.append(i[0])
        topKeywordsForPapers.append(keywords)
        tfidfAllPapers.append(tfidf)
        
    with open('tfidf', 'wb') as fp:
        pickle.dump(tfidfAllPapers, fp)
    
    with open('keywords', 'wb') as fp:
        pickle.dump(topKeywordsForPapers, fp)
     


# In[26]:


findKeywords()


# In[27]:


def readTFIDF():
    with open('tfidf', 'rb') as fp:
       tfidfAllPapers =  pickle.load(fp)
    return tfidfAllPapers


# In[28]:


readTFIDF()


# In[29]:


def readKeywords():
    with open('keywords', 'rb') as fp:
        topKeywordsForPapers = pickle.load(fp)
    return topKeywordsForPapers
    #print(topKeywordsForPapers)
     


# In[30]:


readKeywords()


# In[31]:


scores = readTFIDF()
print(scores[0]['attention'])
print(scores[1]['dialog'])


# In[32]:


def fetchCollocation(targetKeywords, paperWords, windowSize, index, threshold = 0.03):
    length = len(paperWords)
    scores = readTFIDF()
    collocation = []
    for i in range(length):
        if paperWords[i] in targetKeywords:
            for j in range(max(-1*windowSize, 0), min(windowSize+1, length-1)):
                if j != 0 and (i+j)<length and paperWords[i+j] not in collocation and scores[index][paperWords[i+j]] > threshold :
                    collocation.append(paperWords[i+j])
    return collocation


# In[33]:


# C1 is collocational words surrounding keyword
def fetchC1(windowSize):
    papers = readPapers()
    topKeywordsForPapers = readKeywords()
    C1 = []
    index = 0
    for paper in topKeywordsForPapers:
        C1ForPaper = fetchCollocation(paper, papers[index][0], windowSize, index)
        keywordDict = {}
        for keyword in C1ForPaper:
            keywordDict[keyword] = keywordDict.get(keyword, 0) + 1
        C1.append(keywordDict)
        index = index + 1
    print(C1) 
    
    with open('C1', 'wb') as fp:
        pickle.dump(C1, fp)


# In[34]:


fetchC1(1)


# In[35]:


def fetchContextFromCorpus(targetKeywords, index, windowSize):
    papers = readPapers()
    context = []
    for i in range(len(papers)):
        if i != index:
            for word in targetKeywords:
                if word in papers[i][0]:
                    context += fetchCollocation([word], papers[i][0], windowSize, i)
    return context


# In[36]:


# finding collocational words around keywords from corpus 
# corpus - until now other papers in the dataset
def fetchC2(windowSize = 2):
    topKeywordsForPapers = readKeywords()
    C2 = []
    index = 0
    for paper in topKeywordsForPapers:
        C2ForPaper = fetchContextFromCorpus(paper, index, windowSize)
        keywordDict = {}
        for keyword in C2ForPaper:
            keywordDict[keyword] = keywordDict.get(keyword, 0) + 1
        C2.append(keywordDict)
        index = index + 1
    print(len(C2), len(C2[0]), len(C2[1]))
    print(C2)
    
    with open('C2', 'wb') as fp:
        pickle.dump(C2, fp)
    


# In[37]:


fetchC2()


# In[38]:


def fetchC3():
    topKeywordsForPapers = readKeywords()
    paperKeywordsSynset = []
    for paper in topKeywordsForPapers:
        keywordSynset = []
        for keyword in paper:
            synsetForWord = wordnet.synsets(keyword)
            synsetWordNames = ([i.lemmas()[0].name() for i in synsetForWord]) # contains only names
            uniqueNames = set(synsetWordNames)  # names repeat so only unique ones taken
            if(len(uniqueNames)>0):
                keywordSynset.extend(uniqueNames)
        keywordsDict = {}
        for keyword in keywordSynset:
            keywordsDict[keyword] = keywordsDict.get(keyword, 0) + 1
        paperKeywordsSynset.append(keywordsDict)
    print(paperKeywordsSynset)
    
    with open('C3', 'wb') as fp:
        pickle.dump(paperKeywordsSynset, fp)
    


# In[39]:


fetchC3()


# In[40]:


def readContexts(numberOfContexts):
    # in place of C1, C2.. used contexts array 
    contexts = []
    for j in range(1, numberOfContexts + 1):
        # reading the 3 contexts 
        with open('C' + str(j), 'rb') as fp:
#             print(pickle.load(fp))
            contexts.append(pickle.load(fp))
    return contexts  


# In[41]:


readContexts(3)


# In[59]:


# dumps json of all variants of context for each file separately
numberOfContexts = 3
def saveContextForPapers():
    contexts = readContexts(numberOfContexts)
    papers = readPapers()
    for index in range(len(papers)):
        contextsForCurrentPaper = {}
        for j in range(1, numberOfContexts + 1):
            #print(contexts)
            contextsForCurrentPaper['C' + str(j)] = contexts[j-1][index]
       # print(contextsForCurrentPaper)
        with open('context/' + str(index)+ '.json', 'w') as fp:
            json.dump(contextsForCurrentPaper, fp)
        


# In[60]:


saveContextForPapers()


# In[91]:


def calculateWeights():
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    papers = readPapers()
    for index in range(len(papers)):
        with open('context/' + str(index) + '.json', 'r') as fp:
            context = json.load(fp)
            for j in range(1, numberOfContexts + 1):
                for word in context['C' + str(j)]:
                    start = 0
                    end = 0
                    if word in english_vocab:
                        start = 20
                        end = 25
                    else :
                        start = 5 
                        end = 10
                    context['C' + str(j)][word] *=  random.uniform(start, end)
        with open('contextManipulated/' + str(index)+ '.json', 'w') as fp:
            json.dump(context, fp)
                        


# In[92]:


calculateWeights()

