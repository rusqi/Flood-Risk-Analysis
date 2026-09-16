import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

# Load the Excel file
file_path = '/mnt/data/Data Curah Hujan Harian 2022-2024 Cleaned.xlsx'

# Load the sheet, skipping the first 6 rows that contain metadata
df_cleaned = pd.read_excel(file_path, sheet_name='Data Harian - Table', skiprows=6)

# Clean the DataFrame by renaming columns and focusing on relevant columns
df_cleaned.columns = ['Tanggal', 'Curah Hujan (mm)', 'Unused', 'Metadata']
df_cleaned = df_cleaned[['Tanggal', 'Curah Hujan (mm)']]

# Convert the 'Tanggal' column to datetime
df_cleaned['Tanggal'] = pd.to_datetime(df_cleaned['Tanggal'], errors='coerce')

# Remove rows with invalid dates or missing rainfall data
df_cleaned = df_cleaned.dropna(subset=['Tanggal', 'Curah Hujan (mm)'])

# Extract the month and year from the 'Tanggal' column
df_cleaned['Bulan'] = df_cleaned['Tanggal'].dt.month
df_cleaned['Tahun'] = df_cleaned['Tanggal'].dt.year

# Aggregate the data to get monthly rainfall totals
monthly_rainfall = df_cleaned.groupby(['Tahun', 'Bulan'])['Curah Hujan (mm)'].sum().reset_index()

# Display the first few rows of the aggregated data
print(monthly_rainfall.head())
