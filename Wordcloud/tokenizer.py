import os 
from bs4 import BeautifulSoup
from underthesea import word_tokenize, classify
import pandas as pd 
import numpy as np
import json

path = '/home/truongtang/Spiderum/post_lib/'
numberOfPost = len(os.listdir(path)) 

#print(numberOfPost)

#create list for pd
listOfTitles = []
listOfCategories = []
listOfContent = []
listOfTokenizedText = []
classifier = []


for i in range(1,numberOfPost):
    
    fileName = path + 'posts-' + str(i) + '.json'
    
    with open (fileName, 'r') as textFile:
        data = textFile.read()
        text = json.loads(data)

        #using bs to elimiate all tags in html bbody
        soup = BeautifulSoup(text['body'], features='lxml')
        allText = ' '.join(soup.findAll(text=True))
        
        #creat lists for the df
        listOfContent.append(allText)
        listOfTitles.append(text['title'])
        listOfTokenizedText.append(word_tokenize(allText))
        listOfCategories.append(classify(text['title']))


df = pd.DataFrame(list(zip(listOfTitles, listOfContent, listOfTokenizedText, listOfCategories)), columns = ['Title', 'Body', 'Tokenized', 'Categories'])

allContent = list(df['Tokenized'].apply(pd.Series).stack())

keywords = list(filter(lambda x: (' ' in x), allContent))

from collections import Counter

#class MyCounter(Counter):
#    def __str__(self):
#        return "\n".join('{} {}'.format(k, v) for k, v in self.items())

#keywordStatistics = MyCounter(Counter(keywords).most_common())

kwStats = Counter(keywords).most_common()

#print(keywordStatistics[:10])

kwStatsDf = pd.DataFrame(kwStats, columns = ['keyword', 'frequency'])

print(kwStatsDf.head())

#with open ('output.txt', 'w') as outputFile:
#    outputFile.write(str(keywordStatistics))

#print(df.head())

#with open ('categories.csv', 'w') as categoriesFile:
#    df.to_csv(categoriesFile, sep='\t', encoding='utf-8')

from underthesea import pos_tag

kwStats['pos'] =  pos_tag(kwStats['keyword'])

print(kwStats.head(100))