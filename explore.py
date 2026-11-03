import pandas as pd

df= pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin-1")

print(df.shape)
print(df.columns)
print(df.head())
print(df.isnull().sum())