import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import pickle
import scipy.stats as stats
from scipy.stats import genextreme, genpareto

file_path = "Data Curah Hujan Harian Cleaned.xlsx" 
data = pd.read_excel(file_path, header=0)
data['Curah Hujan'] = pd.to_numeric(data['Curah Hujan'], errors='coerce')
data['Tanggal'] = pd.to_datetime(data['Tanggal'], errors='coerce')

for i in range(1, 3):
    data[f'Lag-{i}'] = data['Curah Hujan'].shift(i)
data.dropna(subset=[f'Lag-{i}' for i in range(1, 3)], inplace=True)

X = data[[f'Lag-{i}' for i in range(1, 3)]].values
y = data['Curah Hujan'].values

train_ratio = 0.8
train_size = int(len(X) * train_ratio)

X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

class ELM:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.biases = np.random.uniform(-1, 1, (1, hidden_size))
        self.output_weights = np.random.uniform(-1, 1, (hidden_size, output_size))

    def relu_activation(self, x):
        return np.maximum(0, x)

    def train(self, X, y):
        H = self.relu_activation(np.dot(X, self.weights) + self.biases)
        H_pseudo_inv = np.linalg.pinv(H)
        self.output_weights = np.dot(H_pseudo_inv, y)

    def predict(self, X):
        H = self.relu_activation(np.dot(X, self.weights) + self.biases)
        predictions = np.dot(H, self.output_weights)
        return np.maximum(predictions, 0)

best_mae = float('inf')
best_mse = float('inf')

best_hidden_size_mae = None
best_hidden_size_mse = None

best_elm_mae = None
best_elm_mse = None

mae_scores_for_hidden_sizes = []
mse_scores_for_hidden_sizes = []

hidden_sizes = [1, 3, 5, 10, 15, 20, 25, 30]

for hidden_size in hidden_sizes:
    elm = ELM(input_size=X_train.shape[1], hidden_size=hidden_size, output_size=1)
    elm.train(X_train, y_train)
    predictions = elm.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    
    mae_scores_for_hidden_sizes.append(mae)
    mse_scores_for_hidden_sizes.append(mse)
    
    if mae < best_mae:
        best_mae = mae
        best_hidden_size_mae = hidden_size
        best_elm_mae = elm

    if mse < best_mse:
        best_mse = mse
        best_hidden_size_mse = hidden_size
        best_elm_mse = elm

    print(f"Jumlah Neuron pada Hidden Layer: {hidden_size}")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")

print(f"Best MAE: {best_mae} untuk Jumlah Neuron: {best_hidden_size_mae}")
print(f"Best MSE: {best_mse} untuk Jumlah Neuron: {best_hidden_size_mse}")

best_predictions = best_elm_mae.predict(X_test)

plt.figure(figsize=(20, 8))
plt.plot(y_test, color='blue', label='Nilai Aktual')
plt.plot(best_predictions, color='red', label='Nilai Prediksi')
plt.title('Perbandingan Nilai Aktual dan Nilai Prediksi', fontsize=16)
plt.xlabel('Waktu', fontsize=12)
plt.ylabel('Curah Hujan (mm)', fontsize=12)
dates = data['Tanggal'].iloc[-len(y_test):]
years_months = dates.dt.strftime('%b %Y')
plt.xticks(ticks=np.arange(0, len(dates), step=30), labels=years_months[::30], rotation=45, fontsize=10)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print(f"MAE for Best ELM model: {best_mae}")
print(f"MSE for Best ELM model: {best_mse}")

plt.subplot(1, 2, 1)
plt.plot(hidden_sizes, mae_scores_for_hidden_sizes, marker='o', color='blue')
plt.xlabel('Jumlah Neuron pada Lapisan Tersembunyi')
plt.ylabel('Mean Absolute Error (MAE)')
plt.title('Perbandingan MAE untuk Jumlah Neuron yang Berbeda')

plt.subplot(1, 2, 2)
plt.plot(hidden_sizes, mse_scores_for_hidden_sizes, marker='o', color='red')
plt.xlabel('Jumlah Neuron pada Lapisan Tersembunyi')
plt.ylabel('Mean Squared Error (MSE)')
plt.title('Perbandingan MSE untuk Jumlah Neuron yang Berbeda')
plt.tight_layout()
plt.show()

with open('best_elm_model_mae.pkl', 'wb') as file:
    pickle.dump(best_elm_mae, file)

with open('best_elm_model_mse.pkl', 'wb') as file:
    pickle.dump(best_elm_mse, file)

print("Model ELM terbaik telah disimpan.")

data['Bulan'] = data['Tanggal'].dt.to_period('M')
bulan_max = data.groupby('Bulan')['Curah Hujan'].max().reset_index()

monthly_extremes = bulan_max['Curah Hujan'].values
params = stats.genextreme.fit(monthly_extremes)
shape_gev, loc_gev, scale_gev = params

print(f"GEV Parameters - Shape: {shape_gev}, Location: {loc_gev}, Scale: {scale_gev}")
ks_stat, ks_p_value = stats.kstest(monthly_extremes, 'genextreme', args=params)
print(f"Kolmogorov-Smirnov Test Statistic: {ks_stat}, P-value: {ks_p_value}")

for month, month_data in bulan_max.groupby('Bulan')['Curah Hujan']:
    params_month = stats.genextreme.fit(month_data)
    shape_month, loc_month, scale_month = params_month

    ks_stat_month, ks_p_value_month = stats.kstest(month_data, 'genextreme', args=params_month)
    print(f"Bulan {month} - GEV KS Test - Statistic: {ks_stat_month}, P-value: {ks_p_value_month}")

plt.figure(figsize=(10, 6))
plt.hist(monthly_extremes, bins=10, density=True, alpha=0.6, color='g', label='Data Ekstrem')
plt.title('Distribusi GEV dan Data Ekstrem Curah Hujan')
plt.xlabel('Curah Hujan (mm)')
plt.ylabel('Frekuensi Relatif / Kepadatan Probabilitas')
plt.text(151, 0.0122, f'Shape: {shape_gev:.2f}\nLocation: {loc_gev:.2f}\nScale: {scale_gev:.2f}', fontsize=10)
plt.legend()
plt.grid(True)
plt.show()

def calculate_residual_life(threshold, data):
    exceedances = data[data > threshold]

    if len(exceedances) > 0:
        residual_life = np.mean(exceedances - threshold)
    else:
        residual_life = np.nan
    return residual_life

thresholds = np.linspace(min(monthly_extremes), max(monthly_extremes), 100)
residual_life_values = [calculate_residual_life(threshold, monthly_extremes) for threshold in thresholds]

plt.figure(figsize=(10, 6))
plt.plot(thresholds, residual_life_values, label="Mean Residual Life", color='blue')

thresholds_lines = [40, 50, 90, 100]
for threshold in thresholds_lines:
    plt.axvline(x=threshold, color='red', linestyle='--', linewidth=1)
plt.axvline(x=threshold, color='red', linestyle='--', linewidth=1, label='Kandidat Thresholds')
plt.title('Mean Residual Life Plot', fontsize=16)
plt.xlabel('Curah Hujan (mm)', fontsize=12)
plt.ylabel('Mean Excess', fontsize=12)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.show()

threshold = 100
extreme_values = monthly_extremes[monthly_extremes > threshold]
print(f"Jumlah nilai ekstrem (lebih besar dari threshold {threshold} mm): {len(extreme_values)}")

params_gpd = stats.genpareto.fit(extreme_values)
shape_gpd, loc_gpd, scale_gpd = params_gpd

print(f"GPD Parameters - Shape: {shape_gpd}, Location: {loc_gpd}, Scale: {scale_gpd}")
ks_stat_gpd, ks_p_value_gpd = stats.kstest(extreme_values, 'genpareto', args=params_gpd)
print(f"Kolmogorov-Smirnov Test GPD - Statistic: {ks_stat_gpd}, P-value: {ks_p_value_gpd}")

params_extreme = stats.genextreme.fit(extreme_values)
shape_extreme, loc_extreme, scale_extreme = params_extreme

for value in extreme_values:
    ks_stat, ks_p_value = stats.kstest([value], 'genextreme', args=params_extreme)
    print(f"Nilai ekstrem: {value} mm - KS Test - Statistic: {ks_stat}, P-value: {ks_p_value}")


plt.figure(figsize=(10, 6))

plt.hist(extreme_values, bins=10, density=True, alpha=0.6, color='g', label='Data Ekstrem')

plt.title('Distribusi GPD dan Data Ekstrem Curah Hujan')
plt.xlabel('Curah Hujan (mm)')
plt.ylabel('Frekuensi Relatif / Kepadatan Probabilitas')
plt.text(182, 0.0312, f'Shape: {shape_gpd:.2f}\nLocation: {loc_gpd:.2f}\nScale: {scale_gpd:.2f}', fontsize=10)
plt.legend()
plt.grid(True)
plt.show()

def calculate_var(p, shape, loc, scale):
    var = loc + scale * ((-np.log(1 - p)) ** shape - 1) / shape
    return var

confidence_levels = [0.90, 0.95, 0.99]

var_values_gev = []
for p in confidence_levels:
    var_gev = calculate_var(p, shape_gev, loc_gev, scale_gev)
    var_values_gev.append(var_gev)
    print(f"VaR pada {int(p*100)}% kepercayaan dengan GEV: {var_gev}")

var_values_gpd = []
for p in confidence_levels:
    var_gpd = calculate_var(p, shape_gpd, loc_gpd, scale_gpd) 
    var_values_gpd.append(var_gpd)
    print(f"VaR pada {int(p*100)}% kepercayaan dengan GPD: {var_gpd}")