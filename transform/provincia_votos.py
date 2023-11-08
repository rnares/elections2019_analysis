import pandas as pd
import numpy as np

#load elections data from Madrid
# Load elections data from Madrid
df_spain = pd.read_csv('../data/votes')

# Filter rows where "Código de Provincia" equals 28 (Madrid)
#df_spain = df_spain[df_spain['Código de Provincia'] == 28]

# Transform "Código de Provincia" and "Código de Municipio" to the desired format
df_spain['Código de Provincia'] = df_spain['Código de Provincia'].astype(str).str.zfill(2)
df_spain['Código de Municipio'] = df_spain['Código de Municipio'].astype(str).str.zfill(3)

# Trim values
df_spain['Nombre de Provincia'] = df_spain['Nombre de Provincia'].str.strip()

# Concatenate the two columns with the transformed values
df_spain['COD_POSTAL'] = df_spain['Código de Provincia'] + df_spain['Código de Municipio']
df_spain.rename(columns={'PSOE                                              ': 'PSOE'}, inplace=True)

df_spain.rename(columns={'PP                                                ': 'PP'}, inplace=True)

df_spain = df_spain.groupby(["Código de Provincia", 'Nombre de Provincia'])[['PSOE','PP', 'Votos a candidaturas']].sum().reset_index()


df_spain['%PSOE']=(df_spain['PSOE']/df_spain['Votos a candidaturas']).apply(lambda x: '{:.2f}'.format(x * 100))
df_spain['%PP']=(df_spain['PP']/df_spain['Votos a candidaturas']).apply(lambda x: '{:.2f}'.format(x * 100))

# Save the transformed DataFrame to a CSV file
df_spain.to_csv('../data/df_spain.csv', index=False)  # You can specify index=False to avoid saving the index column

# Print the first 10 rows of the DataFrame
print(df_spain.head(10))