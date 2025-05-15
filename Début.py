import pandas as pd

pd.options.display.max_rows = 9999

df = pd.read_csv('data.csv', sep=';')

df.drop(columns=['Lien vers les mesures en direct', 'Mesures d’amélioration mises en place ou prévues','air','actions'],inplace=True)
df.drop_duplicates(inplace=True)
df.dropna(how='all',inplace=True)
#print(df.info())

Metro=df[df["Nom de la ligne"].str.contains("Métro", case=False, na=False)]
Train=Metro.head(int(0.7*len(Metro)+1))
Test=Metro.tail(int(0.3*len(Metro)))
#print(Metro.to_string())
#print(Train.info())
#print(Test.info())

#Metro.to_csv("stations_metro2.csv", index=False, encoding='utf-8-sig',sep=';')
#Train.to_csv("stations_metro2.csv", index=False, encoding='utf-8-sig',sep=';')
#Test.to_csv("stations_metro2.csv", index=False, encoding='utf-8-sig',sep=';')

#Question 2
numeric_df = df.select_dtypes(include=['number'])
print(numeric_df.columns)
print(numeric_df.describe())

correlations = numeric_df.corr()
print(correlations)
