import os
from bs4 import BeautifulSoup
from underthesea import word_tokenize, classify, pos_tag
import pandas as pd 
import numpy as np 
import json 
import time
from tqdm import tqdm

def makeData (path):
    #path = ''
    #numberOfPost = len(os.listdir(path))
    numberOfPost =  10

    listOfTitles = []
    listOfCategories = []
    listOfContent = []
    listOfTokenizedText = []

    for i in tqdm(range(1, numberOfPost)):
        fileName = path + 'posts-' + str(i) + '.json'
        time.sleep(3)
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

path1 = '/home/truongtang/Spiderum/post_lib_50/'

allContentDF = makeData(path1)

categoryList = allContentDF['Category'].drop_duplicates().values.tolist()

print(categoryList)

print(allContentDF.head())

def eliminateDuplicate(list):
    return list(dict.fromkeys(list))

def keyword(df):
    allContent = list(df['Tokenized'].apply(pd.Series).stack())
    keywords = list(filter(lambda x: ( ' ' in x), allContent))
    from collections import Counter
    kwStats = Counter(keywords).most_common(100)
    df = pd.DataFrame(kwStats, columns = ['keyword', 'freq']) 
    return df
    #for value, count in kwStats:
    #    print(value,count)

class subDf():
    def __init__ (self, name, dataFrame, noOfSub):
        self.name = name
        self.dataFrame = dataFrame
        self.noOfSub = noOfSub

    def kwStats(self):
        dataFrame = self.dataFrame
        return keyword(dataFrame)

df1 = subDf('Quan điểm tranh luận', allContentDF[allContentDF.Category == 'Quan điểm - Tranh luận'], 50)

print(df1.kwStats())


#export_csv = dfKeyword.to_csv('keywordfreq-QDTL.csv', sep = '\t', encoding = 'utf-8')

