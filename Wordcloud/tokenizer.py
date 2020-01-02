import os 
from bs4 import BeautifulSoup
from underthesea import word_tokenize, classify, pos_tag
import pandas as pd 
import numpy as np
import json

path = '/home/truongtang/Spiderum/post_lib/'
#numberOfPost = len(os.listdir(path)) #for all posts
numberOfPost = 50

#print(numberOfPost)

#create list for pd
listOfTitles = []
listOfCategories = []
listOfContent = []
listOfTokenizedText = []
classifier = []
listOfCurrentCategory = []

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
        listOfCurrentCategory.append(text['cat_id']['name'])

print('Succesfully loaded all data ')


df = pd.DataFrame(list(zip(listOfTitles, listOfContent, listOfTokenizedText, listOfCurrentCategory)), columns = ['Title', 'Body', 'Tokenized', 'Current Categories'])

print('DF CREATED!')
#print(df).
#convert all text into a mega text
allContent = list(df['Tokenized'].apply(pd.Series).stack())
allCategory = list(df['Current Categories'].apply(pd.Series).stack())
#get keywords and frequency
keywords = list(filter(lambda x: (' ' in x), allContent))

from collections import Counter

#class MyCounter(Counter):
#    def __str__(self):
#        return "\n".join('{} {}'.format(k, v) for k, v in self.items())

#keywordStatistics = MyCounter(Counter(keywords).most_common())

kwStats = Counter(keywords).most_common()
catStats = Counter(allCategory).most_common()

dfStats = pd.DataFrame(catStats, columns = ['Category', 'Freq'])
dfStats['Percentage'] = dfStats['Freq']/dfStats['Freq'].sum()

print(dfStats.sort_values(by = ['Percentage'], ascending = False))

#kwStatsAndPos = []
#for i in kwStats:
#    kwPos = pos_tag(i[0])
#    print(kwPos)

#print(kwStatsAndPos)
    

#print(kwStats[:10])

#print(keywordStatistics[:10])

#kwStatsDf = pd.DataFrame(kwStats, columns = ['keyword', 'frequency'])

#print(kwStatsDf.head())

#with open ('output.txt', 'w') as outputFile:
#    outputFile.write(str(keywordStatistics))

#print(df.head())

#with open ('categories.csv', 'w') as categoriesFile:
#df.to_csv(categoriesFile, sep='\t', encoding='utf-8')