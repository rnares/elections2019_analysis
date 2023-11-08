import pandas as pd

# Define the column positions and widths
colspecs = [
    (0, 2),   # Tipo de elección
    (2, 6),   # Año del proceso electoral
    (6, 8),   # Mes del proceso electoral
    (8, 9),   # Número de vuelta
    (9, 11),  # Código de la Comunidad Autónoma
    (11, 22), #CUSEC
    # (11, 13), # Código I.N.E. de la provincia
    # (13, 16), # Código I.N.E. del municipio
    # (16, 18), # Número de distrito municipal
    # (18, 22), # Código de la sección
    (22, 23), # Código de la mesa
    (23, 29), # Código de la candidatura
    (29, 36)  # Votos obtenidos
]

# Define the column names
column_names = [
    "TipoElección",
    "AñoProceso",
    "MesProceso",
    "NúmeroVuelta",
    "CódigoComunidad",
    "CUSEC",
    # "CódigoProvincia",
    # "CódigoMunicipio",
    # "NúmeroDistrito",
    # "CódigoSección",
    "CódigoMesa",
    "CódigoCandidatura",
    "VotosObtenidos"
]

# Read the DAT file using read_fwf
file_path = "10021911.DAT"  # Replace with your actual file path
df = pd.read_fwf(file_path, colspecs=colspecs, names=column_names)

# Filter the records based on the mapped values
filtered_df = df[(df["CódigoCandidatura"] == 94) & (df["CódigoComunidad"] == 12)]
filtered_df.to_csv('votos_distritos')

# Display the DataFrame
print(filtered_df.head(50))


# df_globalmesas = pd.read_csv('globalmesas')

# # Merge the first DataFrame into the second based on "NúmeroDistrito" and "CódigoSección"
# # Create a new column by merging "NúmeroDistrito" and "CódigoSección"
# filtered_df['DistritoSección'] = filtered_df.apply(lambda row: f"{row['NúmeroDistrito']}-{row['CódigoSección']}", axis=1)
# # Group by "NúmeroDistrito" and "CódigoSección" and aggregate "VotosCandidaturas" with sum
# filtered_df = filtered_df.groupby(["DistritoSección","CódigoMunicipio"])["VotosObtenidos"].sum().reset_index()

# merged_df = filtered_df.merge(df_globalmesas, on=['DistritoSección',"CódigoMunicipio"], how="inner")
# merged_df['%PSOE']=merged_df['VotosObtenidos']/merged_df['VotosCandidaturas']

# print(merged_df.head(50))

# filtered_df.to_csv('acensoMAD')
