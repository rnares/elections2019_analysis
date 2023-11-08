import pandas as pd

renta_df = pd.read_csv('../data/RentaEspaña.csv')
renta_df = renta_df[(renta_df['Tipo de elemento'] == "municipio")]
renta_df.rename(columns={'sección censal': 'COD_POSTAL'}, inplace=True)

df_wealth = renta_df
print(df_wealth.head(10))

df_wealth = df_wealth.reset_index()


df_votes = pd.read_csv('../data/votes')
df_votes.rename(columns={'Nombre de Municipio': 'Municipio'}, inplace=True)
df_votes['Municipio']=df_votes['Municipio'].str.strip()
df_votes.rename(columns={'PSOE                                              ': 'PSOE'}, inplace=True)
df_votes['%PSOE']=(df_votes['PSOE']/df_votes['Votos a candidaturas']).apply(lambda x: '{:.2f}'.format(x * 100))
df_votes['Nombre de Comunidad'] = df_votes['Nombre de Comunidad'].astype(str)

# Transform "Código de Provincia" and "Código de Municipio" to the desired format
df_votes['Código de Provincia'] = df_votes['Código de Provincia'].astype(str).str.zfill(2)
df_votes['Código de Municipio'] = df_votes['Código de Municipio'].astype(str).str.zfill(3)
# Trim values
#df_votes['Nombre de Municipio'] = df_votes['Nombre de Municipio'].str.strip()
# Concatenate the two columns with the transformed values
df_votes['COD_POSTAL'] = df_votes['Código de Provincia'] + df_votes['Código de Municipio']
df_votes = df_votes[['Votos a candidaturas', 'Nombre de Comunidad', 'PSOE', '%PSOE', 'COD_POSTAL']]

df_votes['COD_POSTAL'] = df_votes['COD_POSTAL'].astype(int)

result = pd.merge(df_wealth, df_votes, on='COD_POSTAL', how='right')
result.to_csv('../data/municipios_spain')

print(result)