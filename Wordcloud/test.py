import pickle 
from report import subDf

f = open('data.pickle', 'rb')

df10 = pickle.load(f)
df20 = pickle.load(f)
df30 = pickle.load(f)
df40 = pickle.load(f)
df50 = pickle.load(f)

print(df10.dataFrame)
print(df20.dataFrame)
print(df30.dataFrame)
print(df40.dataFrame)
print(df50.dataFrame)


