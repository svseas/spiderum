import os
from bs4 import BeautifulSoup
from underthesea import word_tokenize, classify, pos_tag
import pandas as pd 
import numpy as np 
import json 

def makeData (path):
    #path = ''
    numberOfPost = len(os.listdir(path))

    listOfTitles = []
    listOfCategories = []
    listOfContent = []
    listOfTokenizedText = []

    for i in range(1, numberOfPost):
        fileName = path + 'posts-' + str(i) + '.json'

        with open (fileName, 'r') as textFile:
            data = textFile.read()
            text = json.loads(data)
            soup = BeautifulSoup(text['body'], features = 'lxml')
            allText = ' '.join(soup.findAll(text=True))

            #list for df
            listOfContent.append(allText)
            listOfTitles.append(text['title'])
            listOfTokenizedText.append(word_tokenize(allText))
            listOfCategories.append(text['cat_id']['name'])
    print('Succesfully loaded all data')

    df = pd.DataFrame(list(zip(listOfTitles, listOfContent, listOfTokenizedText, listOfCategories)), columns = ['Title', 'Body', 'Tokenized', 'Category'])

    print('DF CREATED!')
    #print(df.head(50))
    return (df)

path1 = '/home/truongtang/Spiderum/post_lib_sample/'

sampleDF = makeData(path1)

def eliminateDuplicate(list):
    return list(dict.fromkeys(list))

def keyword(df,column):
    allContent = list(df[column].apply(pd.Series).stack())
    keywords = list(filter(lambda x: ( ' ' in x), allContent))
    from collections import Counter
    kwStats = Counter(keywords).most_common()
    for value, count in kwStats:
        print(value,count)

print(keyword(sampleDF, 'Tokenized'))

