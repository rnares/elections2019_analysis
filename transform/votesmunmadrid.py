import pandas as pd
import numpy as np

#load elections data from Madrid
# Load elections data from Madrid
df_madrid = pd.read_csv('votes')

# Filter rows where "Código de Provincia" equals 28 (Madrid)
df_madrid = df_madrid[df_madrid['Código de Provincia'] == 28]

# Transform "Código de Provincia" and "Código de Municipio" to the desired format
df_madrid['Código de Provincia'] = df_madrid['Código de Provincia'].astype(str).str.zfill(2)
df_madrid['Código de Municipio'] = df_madrid['Código de Municipio'].astype(str).str.zfill(3)

# Trim values
df_madrid['Nombre de Municipio'] = df_madrid['Nombre de Municipio'].str.strip()

# Concatenate the two columns with the transformed values
df_madrid['COD_POSTAL'] = df_madrid['Código de Provincia'] + df_madrid['Código de Municipio']
df_madrid.rename(columns={'PSOE                                              ': 'PSOE'}, inplace=True)
df_madrid['%PSOE']=df_madrid['PSOE']/df_madrid['Votos a candidaturas']
df_madrid.rename(columns={'PP                                                ': 'PP'}, inplace=True)
df_madrid['%PP']=np.NaN

# Create a new column "tamano poblacion" based on the condition
df_madrid['size'] = df_madrid['Votos a candidaturas'].apply(lambda x: '<5K' if x < 5000 else '>5K')

# Merge the dataframes based on the common column
#merged_df = df_madrid.merge(MADRID_map, left_on='COD_POSTAL', right_on='CODIGOINE', how='left')
#print(merged_df.head(10))

# Save the transformed DataFrame to a CSV file
df_madrid.to_csv('df_madrid.csv', index=False)  # You can specify index=False to avoid saving the index column

# Print the first 10 rows of the DataFrame
print(df_madrid.head(10))