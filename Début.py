import pandas as pd

pd.options.display.max_rows = 9999

df = pd.read_csv('DATA\data.csv', sep=';')

df.drop(columns=['Lien vers les mesures en direct', 'Mesures d’amélioration mises en place ou prévues','air','actions'],inplace=True)
df.drop_duplicates(inplace=True)
df.dropna(how='all',inplace=True)
print(df.info())


#Question 3 – Filtrage métro
Metro = df[df["Nom de la ligne"].str.contains("Métro", case=False, na=False)]

# Filtrage des lignes sans info pollution
Metro = Metro[~Metro['niveau_pollution'].isin(['pas de données', 'station aérienne'])]

Train=Metro.head(int(0.7*len(Metro)+1)) #70 % de l'info de data.csv
Test=Metro.tail(int(0.3*len(Metro)))  #30%restant
print(Metro.to_string())
print(Train.info())
print(Test.info())

Metro.to_csv("stations_metro2.csv", index=False, encoding='utf-8-sig',sep=';')
Train.to_csv("train.csv", index=False, encoding='utf-8-sig',sep=';')
Test.to_csv("test.csv", index=False, encoding='utf-8-sig',sep=';')

#Question 2
numeric_df = df.select_dtypes(include=['number'])
print(numeric_df.columns)
print(numeric_df.describe())

correlations = numeric_df.corr()
print(correlations)
