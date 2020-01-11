import os
from bs4 import BeautifulSoup
from underthesea import word_tokenize, classify, pos_tag
import pandas as pd 
import numpy as np 
import json 
import time
from tqdm import tqdm
from collections import Counter

#Create DF for Category to count the number of subcriber in each Category
catDf = pd.read_json('/home/truongtang/Spiderum/sub_by_cat/subcribeCatByUser.json').sort_values(by = ['count'], ascending = False)

#function to make data from folder of articles
def makeData (path):
    #path = ''
    numberOfPost = len(os.listdir(path))
    #numberOfPost =  10

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

noList = [10, 20, 30, 40, 50]
pathList = []
allContentDFList = []

if __name__ == "__main__":
    for i in noList:
        path = '/home/truongtang/Spiderum/post_lib_' + str(i) + '/'
        pathList.append(path)
        allContentDF = makeData(path)
        allContentDFList.append(allContentDF)

#For post with more than 50 upvotes
#path50 = '/home/truongtang/Spiderum/post_lib_50/'
#allContentDF50 = makeData(path50)
#categoryList50 = allContentDF50['Category'].drop_duplicates().values.tolist()

#print(categoryList50)
#print(allContentDF50.head())

#drop dub function (just in case)
def eliminateDuplicate(list):
    return list(dict.fromkeys(list))


#function for counting keywords 
def keyword(df):
    allContent = list(df['Tokenized'].apply(pd.Series).stack())
    keywords = list(filter(lambda x: ( ' ' in x), allContent))

   
    kwStats = Counter(keywords).most_common(100)
    df = pd.DataFrame(kwStats, columns = ['keyword', 'freq']) 

    return df
    #for value, count in kwStats:
    #    print(value,count)


#class for getting separate reports 
class subDf():
    def __init__ (self, name, dataFrame ):
        self.name = name
        self.dataFrame = dataFrame
    
    #def kwStats(self):
        
    #    return keyword(self.dataFrame)
    
    def noOfSub(self):

        noOfSub = catDf.loc[catDf
        
        ['cat_name'] == str(self.name), 'count'].iloc[0]
        
        return noOfSub
    
    def noOfArticle(self):
        
        allCategory = list(self.dataFrame['Category'].apply(pd.Series).stack())
        
        noOfArticle = pd.DataFrame(Counter(allCategory).most_common(), columns = ['Category', 'Number of Article'])

        return noOfArticle
        
#df10 = subDf('Quan điểm - Tranh luận', allContentDFList[0][allContentDFList[0].Category == 'Quan điểm - Tranh luận'])

#print(df10.kwStats())
#print(df10.noOfSub())
#print(df10.noOfArticle())
import pickle

if __name__ == '__main__':
    df10 = subDf('upvote count: 10', allContentDFList[0])
    df20 = subDf('upvote count: 20', allContentDFList[1])
    df30 = subDf('upvote count: 30', allContentDFList[2])
    df40 = subDf('upvote count: 40', allContentDFList[3])
    df50 = subDf('upvote count: 50', allContentDFList[4])

    f = open('data.pickle', 'wb')

    pickle.dump(df10, f)
    pickle.dump(df20, f)
    pickle.dump(df30, f)
    pickle.dump(df40, f)
    pickle.dump(df50, f)
    f.close()

    f = open('data.pickle', 'rb')

    df10 = pickle.load(f)
    df20 = pickle.load(f)
    df30 = pickle.load(f)
    df40 = pickle.load(f)
    df50 = pickle.load(f)






#df20 = subDf('Quan điểm - Tranh luận', allContentDFList[1][allContentDFList[1].Category == 'Quan điểm - Tranh luận'])

#print(df20.kwStats())
#print(df20.noOfSub())
#print(df20.noOfArticle())

#export_csv = dfKeyword.to_csv('keywordfreq-QDTL.csv', sep = '\t', encoding = 'utf-8')


