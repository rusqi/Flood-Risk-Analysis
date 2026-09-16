import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

data = {
    "Bulan": ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
    "2013": [283.3, 136.1, 89.7, 106.2, 131.4, 167.2, 83.8, 40.4, 164.6, 56.6, 149.8, 214.8],
    "2014": [142.5, 87.6, 7, 112, 78, 69.3, 33.1, 133.5, 141.1, 466.5, 510.7, 483.1],
    "2015": [81.6, 20.2, 124, 354.9, 47.9, 43.5, 84, 56.1, 184.5, 220.9, 24.6, 141.4],
    "2016": [325.5, 160, 92.8, 51, 241, 66, 74.8, 357.7, 66.1, 359.5, 487.4, 227.2],
    "2017": [337.9, 108.7, 327.5, 50.6, 167, 29.7, 20.3, 64.8, 194.8, 193.7, 429.6, 473.7],
    "2018": [252.7, 229.6, 76.9, 261.2, 402, 77.1, 81.7, 95.1, 196.6, 307, 578.4, 498.8],
    "2019": [126.9, 99.5, 87.43, 209.8, 75.5, 117.2, 135.8, 40.1, 83.3, 371, 178.5, 99],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame:")
print(df, "\n")

# Check for missing values in the DataFrame
missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values, "\n")

# Identifying outliers for each month
outliers = {}

for month in df["Bulan"]:
    values = df[df["Bulan"] == month].iloc[:, 1:].values.flatten()
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    month_outliers = values[(values < lower_bound) | (values > upper_bound)]
    outliers[month] = month_outliers

print("Outliers for each month:")
for month, outlier_values in outliers.items():
    print(f"{month}: {outlier_values}")

# Normalize the data using Min-Max Scaling
scaler = MinMaxScaler()
numerical_columns = df.columns[1:]
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Display the normalized DataFrame
print("\nNormalized DataFrame:")
print(df)