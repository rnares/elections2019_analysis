import pandas as pd
import numpy as np

df_globalmesas = pd.read_csv('../data/globalmesas1')
filtered_df = pd.read_csv('../data/votos_distritos')
renta_df = pd.read_csv('../data/RentaEspaña.csv')

renta_df.rename(columns={'sección censal': 'CUSEC'}, inplace=True)

# Merge the first DataFrame into the second based on "NúmeroDistrito" and "CódigoSección"
# Create a new column by merging "NúmeroDistrito" and "CódigoSección"
#filtered_df['DistritoSección'] = filtered_df.apply(lambda row: f"{row['NúmeroDistrito']}-{row['CódigoSección']}", axis=1)
# Group by "NúmeroDistrito" and "CódigoSección" and aggregate "VotosCandidaturas" with sum
filtered_df = filtered_df.groupby(["CUSEC"])["VotosObtenidos"].sum().reset_index()

merged_df = filtered_df.merge(df_globalmesas, on=['CUSEC'], how="inner")
merged_df = merged_df.merge(renta_df, on=['CUSEC'], how="left")

merged_df['%PSOE']=(merged_df['VotosObtenidos']/merged_df['VotosCandidaturas']).apply(lambda x: '{:.2f}'.format(x * 100))

# Calculate the percentiles
percentile_25 = merged_df['Renta media por hogar'].quantile(0.25)
median = merged_df['Renta media por hogar'].quantile(0.50)  # Median is the same as the 50th percentile
percentile_75 = merged_df['Renta media por hogar'].quantile(0.75)
percentile_95 = merged_df['Renta media por hogar'].quantile(0.95)

print(f"25th Percentile: {percentile_25}")
print(f"Median (50th Percentile): {median}")
print(f"75th Percentile: {percentile_75}")
print(f"95th Percentile: {percentile_95}")


# Define the conditions and create the new columns
merged_df['PSOE_poor'] = merged_df['%PSOE'].where(merged_df['Renta media por hogar'] < percentile_25)
merged_df['PSOE_mid'] = merged_df['%PSOE'].where((merged_df['Renta media por hogar'] >= percentile_25) & (merged_df['Renta media por hogar'] <= percentile_75))
merged_df['PSOE_uppermid'] = merged_df['%PSOE'].where(merged_df['Renta media por hogar'] > percentile_75)
merged_df['PSOE_rich'] = merged_df['%PSOE'].where(merged_df['Renta media por hogar'] > percentile_95)

# Replace NaN values with null if needed
# merged_df['PSOE_poor'].fillna(np.NaN, inplace=True)
# merged_df['PSOE_mid'].fillna(np.NaN, inplace=True)
# merged_df['PSOE_uppermid'].fillna(np.NaN, inplace=True)
# merged_df['PSOE_rich'].fillna(np.NaN, inplace=True)


print(merged_df.head(80))
merged_df.to_csv('../data/votos_mesas')