#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importiamo le librerie necessarie
import pandas as pd

# Carichiamo il dataset
file_path = 'owid-covid-data.csv'  # Sostituisci con il percorso del file CSV
df = pd.read_csv(file_path)

# Verifichiamo le dimensioni del dataset
print("Dimensioni del dataset:")
print(f"Righe: {df.shape[0]}, Colonne: {df.shape[1]}")

# Verifichiamo i metadati (nomi colonne e tipi di dati)
print("\nMetadati del dataset:")
print(df.info())

# Mostriamo le prime righe del dataset per avere un'idea del contenuto
print("\nPrime righe del dataset:")
print(df.head())

# 1a. Calcoliamo il numero totale di casi per continente
# Filtriamo righe valide e raggruppiamo per continente
continent_cases = df[df['continent'].notnull()].groupby('continent')['new_cases'].sum()

print("\nNumero totale di casi per continente:")
print(continent_cases)

# 1b. Calcoliamo il numero totale di casi mondiali
world_cases = df['new_cases'].sum()

# Calcoliamo la percentuale per ogni continente
percent_cases = (continent_cases / world_cases) * 100

print("\nPercentuale di casi per continente rispetto al totale mondiale:")
print(percent_cases)

# Creiamo un report finale in un file CSV
report = pd.DataFrame({
    'Total Cases': continent_cases,
    'Percentage of World Cases': percent_cases
})
report.to_csv('continent_cases_report.csv', index=True)
print("\nReport salvato come 'continent_cases_report.csv'")


# In[ ]:





# In[2]:


# Rimuoviamo valori nulli e sostituiamo new_cases mancanti con 0
df['new_cases'] = df['new_cases'].fillna(0)

# Calcoliamo il totale mondiale dei nuovi casi
world_cases = df['new_cases'].sum()

# Filtriamo righe valide (continente non nullo) e raggruppiamo per continente
continent_cases = df[df['continent'].notnull()].groupby('continent')['new_cases'].sum()

# Calcoliamo la percentuale rispetto al totale mondiale
percent_cases = (continent_cases / world_cases) * 100

# Verifichiamo la somma delle percentuali
total_percentage = percent_cases.sum()

print("\nNumero totale di casi per continente:")
print(continent_cases)

print("\nPercentuale di casi per continente rispetto al totale mondiale:")
print(percent_cases)

print(f"\nLa somma delle percentuali è: {total_percentage:.2f}%")


# In[3]:


# Calcolo del totale della popolazione per continente
# Filtriamo i dati validi per continente
continent_population = df[df['continent'].notnull()].groupby('continent')['population'].max()

print("\nTotale della popolazione per continente:")
print(continent_population)

# Calcolo del rapporto positivi totali sulla popolazione per continente
# Positivi totali (numero totale di casi confermati)
positives_by_continent = df[df['continent'].notnull()].groupby('continent')['new_cases'].sum()

# Rapporto positivi totali su popolazione
positives_ratio = (positives_by_continent / continent_population) * 100

print("\nRapporto di positivi totali sulla popolazione per continente (in %):")
print(positives_ratio)

# Stampa i totali della popolazione per continenti
print("\nPopolazione totale per continente:")
print(continent_population)

# Creazione di un report combinato
report = pd.DataFrame({
    'Total Cases': positives_by_continent,
    'Total Population': continent_population,
    'Positives Ratio (%)': positives_ratio
})
print("\nReport finale:")
print(report)

# Salvataggio del report come CSV
report.to_csv('continent_population_report.csv', index=True)
print("\nReport salvato come 'continent_population_report.csv'")


# In[4]:


# Troviamo la popolazione totale per continente prendendo il valore massimo per ciascun paese
continent_population = df[df['continent'].notnull()]     .groupby(['continent', 'location'])['population'].max()     .groupby('continent').sum()

# Calcoliamo il totale dei positivi per continente
positives_by_continent = df[df['continent'].notnull()].groupby('continent')['new_cases'].sum()

# Calcoliamo il rapporto positivi/popolazione
positives_ratio = (positives_by_continent / continent_population) * 100

# Creiamo il report finale
report = pd.DataFrame({
    'Total Cases': positives_by_continent,
    'Total Population': continent_population,
    'Positives Ratio (%)': positives_ratio
})

print("\nReport finale:")
print(report)

# Salviamo il report in un file CSV
report.to_csv('continent_population_report_fixed.csv', index=True)
print("\nReport salvato come 'continent_population_report_fixed.csv'")


# In[5]:


import pandas as pd

# Carica il file JSON
df = pd.read_json('path_to_your_file.json')

# Controlliamo la struttura dei dati
print(df.head())
print(df.columns)

# Se la struttura del JSON è complessa (dati annidati), possiamo "appiattirla"
# df = pd.json_normalize(df)

# Passaggio 1: Creiamo una colonna 'year_month' per raggruppare i dati per mese e anno
df['year_month'] = df['date'].apply(lambda x: x[:7])  # Assuming date is in 'YYYY-MM-DD' format

# Passaggio 2: Raggruppiamo i dati per continente, anno/mese e sommiamo i casi nuovi
continent_cases_monthly = df.groupby(['continent', 'year_month'])['new_cases'].sum().reset_index()

# Passaggio 3: Sommiamo i casi per continente
continent_cases_total = continent_cases_monthly.groupby('continent')['new_cases'].sum()

# Passaggio 4: Popolazione per continente (assumendo che la popolazione sia corretta)
continent_population = df[df['continent'].notnull()]     .groupby('continent')['population'].max()

# Passaggio 5: Calcolare il rapporto dei casi sulla popolazione
positives_ratio = (continent_cases_total / continent_population) * 100

# Passaggio 6: Creiamo il report finale
report = pd.DataFrame({
    'Total Cases': continent_cases_total,
    'Total Population': continent_population,
    'Positives Ratio (%)': positives_ratio
})

# Stampa del report finale
print("\nReport finale:")
print(report)

# Salviamo il report in un file CSV
report.to_csv('continent_population_report_from_json.csv', index=True)
print("\nReport corretto salvato come 'continent_population_report_from_json.csv'")


# In[6]:


import pandas as pd
import requests

# URL del file JSON
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json"

# Scarica il file JSON dal URL
response = requests.get(url)

# Verifica se il download è andato a buon fine
if response.status_code == 200:
    print("Download riuscito!")
    # Carica i dati JSON in un DataFrame pandas
    df = pd.read_json(response.text)

    # Controlliamo la struttura dei dati
    print(df.head())
    print(df.columns)
    
    # Passaggio 1: Creiamo una colonna 'year_month' per raggruppare i dati per mese e anno
    df['year_month'] = df['date'].apply(lambda x: x[:7])  # Assuming date is in 'YYYY-MM-DD' format

    # Passaggio 2: Raggruppiamo i dati per continente, anno/mese e sommiamo i casi nuovi
    continent_cases_monthly = df.groupby(['continent', 'year_month'])['new_cases'].sum().reset_index()

    # Passaggio 3: Sommiamo i casi per continente
    continent_cases_total = continent_cases_monthly.groupby('continent')['new_cases'].sum()

    # Passaggio 4: Popolazione per continente (assumendo che la popolazione sia corretta)
    continent_population = df[df['continent'].notnull()]         .groupby('continent')['population'].max()

    # Passaggio 5: Calcolare il rapporto dei casi sulla popolazione
    positives_ratio = (continent_cases_total / continent_population) * 100

    # Passaggio 6: Creiamo il report finale
    report = pd.DataFrame({
        'Total Cases': continent_cases_total,
        'Total Population': continent_population,
        'Positives Ratio (%)': positives_ratio
    })

    # Stampa del report finale
    print("\nReport finale:")
    print(report)

    # Salviamo il report in un file CSV
    report.to_csv('continent_population_report_from_json.csv', index=True)
    print("\nReport corretto salvato come 'continent_population_report_from_json.csv'")

else:
    print(f"Errore nel download del file. Status code: {response.status_code}")


# In[7]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Mostriamo le prime righe per confermare che il file è stato caricato correttamente
print(df.head())

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Raggruppa per continente e anno e somma la popolazione
continent_population_yearly = df.groupby(['continent', 'year'])['population'].max().reset_index()

# Somma totale della popolazione per continente
continent_population_total = continent_population_yearly.groupby('continent')['population'].sum()

# Somma globale della popolazione
total_population = continent_population_total.sum()

# Mostriamo il risultato
print("\nPopolazione totale per anno e continente:")
print(continent_population_yearly)

print("\nPopolazione totale per continente:")
print(continent_population_total)

print("\nPopolazione totale globale:")
print(total_population)


# In[8]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Mostriamo le prime righe per confermare che il file è stato caricato correttamente
print(df.head())

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Raggruppa per continente e anno e somma la popolazione
continent_population_yearly = df.groupby(['continent', 'year'])['population'].sum().reset_index()

# Mostriamo il risultato: popolazione totale per continente e anno
print("\nTotale popolazione per continente e anno:")
print(continent_population_yearly)


# In[9]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Rimuovi eventuali duplicati considerando solo la combinazione di 'continent' e 'year' 
df_unique = df.drop_duplicates(subset=['continent', 'year'])

# Raggruppa per continente e anno e somma i casi totali
continent_cases_yearly = df_unique.groupby(['continent', 'year'])['total_cases'].sum().reset_index()

# Mostriamo il risultato: totale dei casi per continente e anno
print("\nTotale casi per continente e anno:")
print(continent_cases_yearly)


# In[ ]:





# In[10]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Filtra il dataset per includere solo i dati relativi a 'OWID_EUR' (Europa)
df_europe = df[df['continent'] == 'Europe']

# Raggruppa i dati per anno e somma i nuovi casi
total_new_cases_per_year = df_europe.groupby('year')['new_cases'].sum().reset_index()

# Mostriamo il risultato
print("\nSomma del totale dei nuovi casi per anno (identificatore 'OWID_EUR'):")
print(total_new_cases_per_year)


# In[11]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Filtra il dataset per includere solo i dati relativi al continente 'Europe'
df_europe = df[df['continent'] == 'Europe']

# Raggruppa i dati per anno e somma i nuovi casi
total_new_cases_per_year_europe = df_europe.groupby('year')['new_cases'].sum().reset_index()

# Mostriamo il risultato
print("\nSomma del totale dei nuovi casi per anno (identificatore 'Europe'):")
print(total_new_cases_per_year_europe)


# In[ ]:





# In[12]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Lista dei continenti OWID
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Dati per ogni continente
result = []

# Itera per ogni continente
for continent in continents:
    # Filtra il dataset per il continente corrente
    df_continent = df[df['continent'] == continent]
    
    # Raggruppa i dati per anno e somma i nuovi casi e la popolazione
    grouped_data = df_continent.groupby('year').agg(
        total_new_cases=('new_cases', 'sum'),
        total_population=('population', 'max')  # Supponiamo che la popolazione per il continente non cambi durante l'anno
    ).reset_index()
    
    # Calcola il rapporto tra nuovi casi e popolazione
    grouped_data['cases_ratio'] = (grouped_data['total_new_cases'] / grouped_data['total_population']) * 100
    
    # Aggiungi il continente come colonna
    grouped_data['continent'] = continent
    
    # Aggiungi i risultati alla lista
    result.append(grouped_data)

# Combina tutti i risultati in un DataFrame finale
final_result = pd.concat(result)

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(final_result[['continent', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[13]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Filtra i dati per i continenti che hanno codici ISO che iniziano con 'OWID'
continents = df[df['iso_code'].str.startswith('OWID')]

# Raggruppa i dati per continente e anno e somma i nuovi casi
grouped = continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Prendi solo il primo valore di popolazione per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno
grouped['cases_ratio'] = (grouped['total_new_cases'] / grouped['total_population']) * 100

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[ ]:





# In[14]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno
grouped['cases_ratio'] = (grouped['total_new_cases'] / grouped['total_population']) * 100

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[15]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno, moltiplicato per 100
grouped['cases_ratio'] = (grouped['total_new_cases'] / grouped['total_population']) * 100

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[16]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno, moltiplicato per 100
grouped['cases_ratio'] = (grouped['total_new_cases'] / grouped['total_population']) * 100

# Formatta i numeri con separatore delle migliaia (virgola)
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}")
grouped['total_population'] = grouped['total_population'].apply(lambda x: f"{x:,.0f}")
grouped['cases_ratio'] = grouped['cases_ratio'].apply(lambda x: f"{x:,.2f}")

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[17]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno, moltiplicato per 100
grouped['cases_ratio'] = (grouped['total_new_cases'] / grouped['total_population']) * 100

# Formatta i numeri con punto come separatore delle migliaia e virgola come separatore decimale
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['total_population'] = grouped['total_population'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['cases_ratio'] = grouped['cases_ratio'].apply(lambda x: f"{x:,.2f}".replace(',', '.'))

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[18]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno senza moltiplicare per 100
grouped['cases_ratio'] = grouped['total_new_cases'] / grouped['total_population']

# Formatta i numeri con punto come separatore delle migliaia e virgola come separatore decimale
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['total_population'] = grouped['total_population'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['cases_ratio'] = grouped['cases_ratio'].apply(lambda x: f"{x:,.5f}".replace(',', '.'))

# Mostriamo il risultato
print("\nSomma dei nuovi casi per anno e rapporto con la popolazione per continente:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio']])


# In[19]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno senza moltiplicare per 100
grouped['cases_ratio'] = grouped['total_new_cases'] / grouped['total_population']

# Verifica la somma del cases ratio per anno
sum_cases_ratio = grouped.groupby('year')['cases_ratio'].sum().reset_index()

# Formatta i numeri con punto come separatore delle migliaia e virgola come separatore decimale
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['total_population'] = grouped['total_population'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['cases_ratio'] = grouped['cases_ratio'].apply(lambda x: f"{x:,.5f}".replace(',', '.'))

# Mostriamo il risultato delle somme per ogni anno
print("\nSomma del cases ratio per ogni anno:")
print(sum_cases_ratio)


# In[20]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno
grouped['cases_ratio'] = grouped['total_new_cases'] / grouped['total_population']

# Calcola il totale dei new cases per anno (somma dei nuovi casi su tutti i continenti)
total_new_cases_per_year = grouped.groupby('year')['total_new_cases'].sum().reset_index()
total_new_cases_per_year.rename(columns={'total_new_cases': 'total_new_cases_all_years'}, inplace=True)

# Uniamo il totale dei new cases per anno ai dati raggruppati per continente
grouped = pd.merge(grouped, total_new_cases_per_year, on='year')

# Aggiungiamo una colonna con il rapporto tra il totale dei new cases per anno e continente e il totale dei new cases per anno
grouped['new_cases_ratio_per_year'] = grouped['total_new_cases'] / grouped['total_new_cases_all_years']

# Verifica che la somma della colonna 'new_cases_ratio_per_year' per ogni anno sia pari a 1
sum_new_cases_ratio = grouped.groupby('year')['new_cases_ratio_per_year'].sum().reset_index()

# Formatta i numeri con punto come separatore delle migliaia e virgola come separatore decimale
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['total_population'] = grouped['total_population'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['cases_ratio'] = grouped['cases_ratio'].apply(lambda x: f"{x:,.5f}".replace(',', '.'))
grouped['new_cases_ratio_per_year'] = grouped['new_cases_ratio_per_year'].apply(lambda x: f"{x:,.5f}".replace(',', '.'))

# Mostriamo il risultato delle somme per ogni anno
print("\nSomma del new_cases_ratio_per_year per ogni anno:")
print(sum_new_cases_ratio)

# Mostriamo il dataframe aggiornato
print("\nDati aggiornati con la colonna new_cases_ratio_per_year:")
print(grouped[['iso_code', 'year', 'total_new_cases', 'total_population', 'cases_ratio', 'new_cases_ratio_per_year']])


# In[21]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Definiamo i continenti da considerare
continents = ['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE']

# Filtra i dati per i continenti definiti
df_continents = df[df['iso_code'].isin(continents)]

# Raggruppa i dati per continente e anno, somma i nuovi casi
grouped = df_continents.groupby(['iso_code', 'year']).agg(
    total_new_cases=('new_cases', 'sum'),
    total_population=('population', 'first')  # Popolazione del continente per anno
).reset_index()

# Calcola il rapporto tra nuovi casi e popolazione per ogni continente e anno
grouped['cases_ratio'] = grouped['total_new_cases'] / grouped['total_population']

# Calcola il totale dei new cases per anno (somma dei nuovi casi su tutti i continenti)
total_new_cases_per_year = grouped.groupby('year')['total_new_cases'].sum().reset_index()
total_new_cases_per_year.rename(columns={'total_new_cases': 'total_new_cases_all_years'}, inplace=True)

# Uniamo il totale dei new cases per anno ai dati raggruppati per continente
grouped = pd.merge(grouped, total_new_cases_per_year, on='year')

# Aggiungiamo una colonna con il rapporto tra il totale dei new cases per anno e continente e il totale dei new cases per anno
grouped['new_cases_ratio_per_year'] = grouped['total_new_cases'] / grouped['total_new_cases_all_years']

# Rimuovi le colonne 'total_population' e 'cases_ratio'
grouped.drop(columns=['total_population', 'cases_ratio'], inplace=True)

# Verifica che la somma della colonna 'new_cases_ratio_per_year' per ogni anno sia pari a 1
sum_new_cases_ratio = grouped.groupby('year')['new_cases_ratio_per_year'].sum().reset_index()

# Formatta i numeri con punto come separatore delle migliaia e virgola come separatore decimale
grouped['total_new_cases'] = grouped['total_new_cases'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
grouped['new_cases_ratio_per_year'] = grouped['new_cases_ratio_per_year'].apply(lambda x: f"{x:,.5f}".replace(',', '.'))

# Mostriamo il risultato delle somme per ogni anno
print("\nSomma del new_cases_ratio_per_year per ogni anno:")
print(sum_new_cases_ratio)

# Mostriamo il dataframe aggiornato senza le colonne 'total_population' e 'cases_ratio'
print("\nDati aggiornati con la colonna new_cases_ratio_per_year (senza 'total_population' e 'cases_ratio'):")
print(grouped[['iso_code', 'year', 'total_new_cases', 'new_cases_ratio_per_year']])


# In[22]:


import pandas as pd
import matplotlib.pyplot as plt

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Aggiungi una colonna 'year' per estrarre l'anno dalla data
df['year'] = df['date'].dt.year

# Filtra i dati per l'Italia
df_italy = df[df['location'] == 'Italy']

# Raggruppa per anno e somma i total cases
grouped_italy = df_italy.groupby('year').agg(
    total_cases=('total_cases', 'max')  # Utilizza max per ottenere il totale accumulato dei casi per anno
).reset_index()

# Visualizza il totale dei casi per anno
print(grouped_italy)

# Crea il grafico dell'evoluzione dei casi totali per anno
plt.figure(figsize=(10, 6))
plt.plot(grouped_italy['year'], grouped_italy['total_cases'], marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.title('Evoluzione dei casi totali di COVID-19 in Italia (per anno)', fontsize=14)
plt.xlabel('Anno', fontsize=12)
plt.ylabel('Totale casi accumulati', fontsize=12)
plt.grid(True)
plt.show()


# In[23]:


import pandas as pd
import matplotlib.pyplot as plt

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per l'Italia e per il 2022
df_italy_2022 = df[(df['location'] == 'Italy') & (df['date'].dt.year == 2022)]

# 1. Grafico dell'evoluzione dei casi totali (total_cases) per l'anno 2022
plt.figure(figsize=(10, 6))
plt.plot(df_italy_2022['date'], df_italy_2022['total_cases'], marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
plt.title('Evoluzione dei casi totali di COVID-19 in Italia (2022)', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Totale casi accumulati', fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# 2. Grafico del numero di nuovi casi (new_cases) per l'anno 2022, rimuovendo valori 0 e NaN
df_italy_2022_new_cases = df_italy_2022[(df_italy_2022['new_cases'] > 0) & (~df_italy_2022['new_cases'].isna())]

plt.figure(figsize=(10, 6))
plt.plot(df_italy_2022_new_cases['date'], df_italy_2022_new_cases['new_cases'], marker='o', color='r', linestyle='-', linewidth=2, markersize=5)
plt.title('Nuovi casi di COVID-19 in Italia (2022) (senza valori 0)', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Nuovi casi', fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()


# In[24]:


import pandas as pd
import matplotlib.pyplot as plt

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset direttamente dal URL
df = pd.read_csv(url)

# Assicurati che la colonna 'date' sia nel formato corretto
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per l'Italia e per il 2022
df_italy_2022 = df[(df['location'] == 'Italy') & (df['date'].dt.year == 2022)]

# 1. Grafico dell'evoluzione dei casi totali (total_cases) per l'anno 2022
plt.figure(figsize=(10, 6))
plt.plot(df_italy_2022['date'], df_italy_2022['total_cases'], marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
plt.title('Evoluzione dei casi totali di COVID-19 in Italia (2022)', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Totale casi accumulati', fontsize=12)

# Annotiamo i punti di picco
max_cases = df_italy_2022['total_cases'].max()
max_case_date = df_italy_2022[df_italy_2022['total_cases'] == max_cases]['date'].iloc[0]
plt.annotate(f'{max_cases:,}', 
             (max_case_date, max_cases),
             textcoords="offset points", 
             xytext=(0, 10), 
             ha='center', 
             fontsize=10, 
             color='red', 
             weight='bold')

# Impediamo la notazione scientifica
plt.ticklabel_format(style='plain', axis='y')

plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# 2. Grafico del numero di nuovi casi (new_cases) per l'anno 2022, rimuovendo valori 0 e NaN
df_italy_2022_new_cases = df_italy_2022[(df_italy_2022['new_cases'] > 0) & (~df_italy_2022['new_cases'].isna())]

plt.figure(figsize=(10, 6))
plt.plot(df_italy_2022_new_cases['date'], df_italy_2022_new_cases['new_cases'], marker='o', color='r', linestyle='-', linewidth=2, markersize=5)
plt.title('Nuovi casi di COVID-19 in Italia (2022) (senza valori 0)', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Nuovi casi', fontsize=12)

# Annotiamo i punti di picco
max_new_cases = df_italy_2022_new_cases['new_cases'].max()
max_new_case_date = df_italy_2022_new_cases[df_italy_2022_new_cases['new_cases'] == max_new_cases]['date'].iloc[0]
plt.annotate(f'{max_new_cases:,}', 
             (max_new_case_date, max_new_cases),
             textcoords="offset points", 
             xytext=(0, 10), 
             ha='center', 
             fontsize=10, 
             color='green', 
             weight='bold')

# Impediamo la notazione scientifica
plt.ticklabel_format(style='plain', axis='y')

plt.grid(True)
plt.xticks(rotation=45)
plt.show()


# In[25]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset
df = pd.read_csv(url)

# Assicuriamoci che la colonna 'date' sia in formato datetime
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per Italia, Germania e Francia dal maggio 2022 ad aprile 2023
countries = ['Italy', 'Germany', 'France']
df_filtered = df[(df['location'].isin(countries)) & 
                 (df['date'] >= '2022-05-01') & 
                 (df['date'] <= '2023-04-30')]

# Boxplot per il numero di pazienti in terapia intensiva (ICU) 
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_filtered, x='location', y='icu_patients')

# Titoli e etichette
plt.title('Differenza nel numero di pazienti in Terapia Intensiva (ICU) tra Italia, Germania e Francia (Maggio 2022 - Aprile 2023)', fontsize=14)
plt.xlabel('Nazione', fontsize=12)
plt.ylabel('Numero di pazienti in terapia intensiva (ICU)', fontsize=12)

# Mostra il grafico
plt.show()


# In[26]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset
df = pd.read_csv(url)

# Assicuriamoci che la colonna 'date' sia in formato datetime
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per Italia, Germania, Francia e Spagna per il 2023
countries = ['Italy', 'Germany', 'France', 'Spain']
df_filtered_2023 = df[(df['location'].isin(countries)) & (df['date'].dt.year == 2023)]

# Somma dei pazienti ospedalizzati (hosp_patients) per ogni paese
hospitalized_sum = df_filtered_2023.groupby('location')['hosp_patients'].sum()

# Controlliamo i valori nulli nella colonna 'hosp_patients'
null_values = df_filtered_2023[df_filtered_2023['hosp_patients'].isnull()]

# Stampa della somma dei pazienti ospedalizzati per nazione
print("Somma dei pazienti ospedalizzati per nazione nel 2023:")
print(hospitalized_sum)

# Controlliamo quanti valori nulli ci sono e se è possibile gestirli
print(f"\nValori nulli nei pazienti ospedalizzati (hosp_patients):\n{null_values[['location', 'date', 'hosp_patients']]}")


# In[27]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset
df = pd.read_csv(url)

# Assicuriamoci che la colonna 'date' sia in formato datetime
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per Italia, Germania, Francia e Spagna per il 2023
countries = ['Italy', 'Germany', 'France', 'Spain']
df_filtered_2023 = df[(df['location'].isin(countries)) & (df['date'].dt.year == 2023)]

# Controlliamo i valori nulli nella colonna 'hosp_patients'
null_values = df_filtered_2023[df_filtered_2023['hosp_patients'].isnull()]

# Visualizziamo il numero di valori nulli per ciascuna nazione
null_count = null_values['location'].value_counts()

# Stampa dei valori nulli per nazione e delle statistiche
print(f"Numero di valori nulli nella colonna 'hosp_patients' per ciascuna nazione nel 2023:\n{null_count}")

# Mostriamo alcune righe con valori nulli per esaminare meglio la situazione
print("\nEsempio di righe con valori nulli per 'hosp_patients':")
print(null_values[['location', 'date', 'hosp_patients']].head())


# In[28]:


import pandas as pd

# URL del file CSV
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Carichiamo il dataset
df = pd.read_csv(url)

# Assicuriamoci che la colonna 'date' sia in formato datetime
df['date'] = pd.to_datetime(df['date'])

# Filtriamo i dati per Italia, Germania, Francia e Spagna per il 2023
countries = ['Italy', 'Germany', 'France', 'Spain']
df_filtered_2023 = df[(df['location'].isin(countries)) & (df['date'].dt.year == 2023)]

# Controlliamo i valori nulli nella colonna 'hosp_patients'
null_values = df_filtered_2023[df_filtered_2023['hosp_patients'].isnull()]

# Visualizziamo il numero di valori nulli per ciascuna nazione
null_count = null_values['location'].value_counts()

# Numero totale di righe per ciascuna nazione
total_count = df_filtered_2023['location'].value_counts()

# Calcolare la percentuale di valori nulli rispetto al numero totale di righe
null_percentage = (null_count / total_count) * 100

# Stampa del numero di valori nulli e del numero totale di righe per nazione
print(f"Numero di valori nulli nella colonna 'hosp_patients' per ciascuna nazione nel 2023:")
print(null_count)

print(f"\nNumero totale di righe per ciascuna nazione nel 2023:")
print(total_count)

# Calcolare la percentuale di dati nulli
print(f"\nPercentuale di valori nulli rispetto al totale delle righe per ciascuna nazione:")
print(null_percentage)

# Mostriamo alcune righe con valori nulli per esaminare meglio la situazione
print("\nEsempio di righe con valori nulli per 'hosp_patients':")
print(null_values[['location', 'date', 'hosp_patients']].head())


# In[ ]:




