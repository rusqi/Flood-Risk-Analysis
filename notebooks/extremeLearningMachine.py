import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from hpelm import ELM

# Load the data
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

# Convert to DataFrame
df = pd.DataFrame(data)

# Transpose the data for easier handling
df = df.set_index('Bulan').T

# Prepare features and target
X = []
y = []

# We will use the past 3 months to predict the next month's rainfall
look_back = 3

for i in range(look_back, len(df)):
    X.append(df.iloc[i - look_back:i].values.flatten())
    y.append(df.iloc[i].values.flatten())

X = np.array(X)
y = np.array(y)

# Split the data into training and testing sets
split_ratio = 0.8
split_index = int(split_ratio * len(X))

X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Normalize the data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_train = scaler_X.fit_transform(X_train)
X_test = scaler_X.transform(X_test)

y_train = scaler_y.fit_transform(y_train)
y_test = scaler_y.transform(y_test)

# Train the ELM model
hidden_neurons = 50  # Number of hidden neurons
activation_function = 'sigm'  # Activation function (e.g., 'sigm' for sigmoid)

model = ELM(X_train.shape[1], y_train.shape[1])
model.add_neurons(hidden_neurons, activation_function)

# Train the model
model.train(X_train, y_train)

# Evaluate the model
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Inverse transform predictions and true values to original scale
y_train_inv = scaler_y.inverse_transform(y_train)
y_pred_train_inv = scaler_y.inverse_transform(y_pred_train)
y_test_inv = scaler_y.inverse_transform(y_test)
y_pred_test_inv = scaler_y.inverse_transform(y_pred_test)

# Calculate Mean Absolute Percentage Error (MAPE)
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape_train = mean_absolute_percentage_error(y_train_inv, y_pred_train_inv)
mape_test = mean_absolute_percentage_error(y_test_inv, y_pred_test_inv)

print(f'Training MAPE: {mape_train:.2f}%')
print(f'Testing MAPE: {mape_test:.2f}%')

# Plotting the results
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))

# Plot the training results
plt.subplot(2, 1, 1)
plt.plot(y_train_inv.flatten(), label='Actual')
plt.plot(y_pred_train_inv.flatten(), label='Predicted')
plt.title('Training Results')
plt.xlabel('Samples')
plt.ylabel('Rainfall (mm)')
plt.legend()

# Plot the testing results
plt.subplot(2, 1, 2)
plt.plot(y_test_inv.flatten(), label='Actual')
plt.plot(y_pred_test_inv.flatten(), label='Predicted')
plt.title('Testing Results')
plt.xlabel('Samples')
plt.ylabel('Rainfall (mm)')
plt.legend()

plt.tight_layout()
plt.show()
