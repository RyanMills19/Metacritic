import pandas as pd

cols = ['ID', 'img', 'title']

df = pd.read_csv(r'C:\Users\Ryan\metacritic\comments_metacritic_en.csv')
df.loc[:,cols] = df.loc[:,cols].ffill()
df = df.dropna()
df = df.drop_duplicates()
df.to_csv('output.csv',index=False)