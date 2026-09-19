# Flood Risk Analysis & Rainfall Forecasting

A quantitative rainfall and flood-risk analysis for **Aceh Besar, Indonesia**, combining time-series forecasting, Extreme Value Theory, and Value at Risk to analyze extreme rainfall events and estimate potential rainfall risk.

> **Research Project — Undergraduate Thesis, Universitas Syiah Kuala**

---

## Project Overview

Flooding can be strongly influenced by periods of unusually high rainfall. This project investigates historical rainfall patterns in **Aceh Besar** and combines forecasting with extreme-value analysis to better understand potential rainfall risk.

The analysis uses three complementary approaches:

* **Extreme Learning Machine (ELM)** to forecast rainfall using lagged rainfall observations
* **Extreme Value Theory (EVT)** to model unusually high rainfall events
* **Value at Risk (VaR)** to estimate rainfall levels associated with different confidence levels

The goal was not only to predict rainfall, but also to translate extreme rainfall behavior into quantitative risk estimates.

---

## Key Results

### Rainfall Forecasting

The ELM model was evaluated using different hidden-layer sizes:

* **1 neuron** produced the lowest MAE
* **5 neurons** produced the lowest MSE in the repeated evaluation
* Increasing the number of neurons did not consistently improve prediction performance
* The best MAE was approximately **5.83–5.94 mm** across repeated experiments

### Extreme Rainfall Analysis

Extreme rainfall was analyzed using two EVT approaches:

* **GEV (Generalized Extreme Value)** using monthly block maxima
* **GPD (Generalized Pareto Distribution)** using the Peaks Over Threshold approach

The Kolmogorov–Smirnov test produced:

| Distribution | KS p-value |
| ------------ | ---------: |
| GEV          |   **0.79** |
| GPD          |   **0.06** |

A **90 mm threshold** was selected for the GPD analysis based on the Mean Residual Life Plot.

### Value at Risk

Estimated rainfall VaR for the 2025 period:

| Confidence Level |      GEV |       GPD |
| ---------------- | -------: | --------: |
| 90%              | 64.40 mm | 261.04 mm |
| 95%              | 70.22 mm | 263.29 mm |
| 99%              | 78.95 mm | 264.89 mm |

The two approaches provide different perspectives: GEV models monthly maximum rainfall, while GPD focuses specifically on rainfall exceeding the selected extreme threshold.

---

## Research Questions

This project investigates three main questions:

1. How accurately can rainfall in Aceh Besar be forecast using Extreme Learning Machine?
2. How can Extreme Value Theory be used to identify and model extreme rainfall events?
3. What rainfall levels are estimated under different confidence levels using Value at Risk?

---

## Dataset

The analysis uses secondary rainfall data obtained from **BMKG**.

| Attribute    | Description                  |
| ------------ | ---------------------------- |
| Location     | Aceh Besar, Indonesia        |
| Data type    | Daily rainfall               |
| Period       | January 2022 – December 2024 |
| Observations | 1,096 daily observations     |
| Unit         | Millimeters (mm)             |
| Source       | BMKG                         |
| Format       | Excel / CSV                  |

The rainfall data were collected from the Sultan Iskandar Muda Meteorological Station.

---

## Methodology

The overall analytical workflow was:

```text
Daily Rainfall Data
        │
        ▼
Data Preprocessing
        │
        ▼
Lag Feature Creation
        │
        ▼
Train / Test Split
        │
        ▼
Extreme Learning Machine
        │
        ├── MAE
        └── MSE
        │
        ▼
Extreme Rainfall Analysis
        │
        ├── Block Maxima → GEV
        │
        └── Peaks Over Threshold → GPD
        │
        ▼
Kolmogorov–Smirnov Test
        │
        ▼
Value at Risk
        │
        ▼
Rainfall Risk Estimates
```

---

## 1. Data Preparation

The original dataset contains daily rainfall observations.

The preprocessing workflow included:

* Converting rainfall values to numeric format
* Converting dates into datetime format
* Identifying missing observations
* Handling missing values
* Creating lagged rainfall features
* Preparing the dataset for time-series forecasting

Two lag features were used:

* `Lag-1`
* `Lag-2`

These features represent rainfall observations from the previous two time periods.

---

## 2. Rainfall Forecasting with Extreme Learning Machine

### Model

The forecasting model uses an **Extreme Learning Machine**, a single-hidden-layer neural network approach in which the hidden-layer weights and biases are randomly initialized and the output weights are calculated using the Moore–Penrose pseudoinverse.

The model uses:

```text
Lag-1 ─┐
       ├──► Hidden Layer ───► Rainfall Prediction
Lag-2 ─┘
```

A ReLU activation function was used in the hidden layer.

### Model Evaluation

The model was tested using multiple hidden-layer configurations:

```text
1
3
5
10
15
20
25
30
```

Performance was evaluated using:

* **Mean Absolute Error (MAE)**
* **Mean Squared Error (MSE)**

### Initial Evaluation

| Hidden Neurons |        MSE |      MAE |
| -------------: | ---------: | -------: |
|              1 |     276.01 | **5.92** |
|              3 | **225.50** |     5.46 |
|              5 | **225.50** |     5.88 |
|             10 |     226.72 |     6.91 |
|             15 |     227.41 |     7.13 |
|             20 |     237.61 |     7.21 |
|             25 |     242.86 |     7.29 |
|             30 |     235.81 |     7.20 |

Repeated experiments were subsequently performed to evaluate the stability of the results.

The repeated evaluation showed that:

* **1 neuron** consistently produced the lowest MAE
* **5 neurons** produced the lowest MSE
* Increasing model complexity did not consistently improve performance

This illustrates an important modeling consideration: a larger neural network is not necessarily a better model for a small time-series dataset.

---

## 3. Extreme Value Theory

After forecasting rainfall, the analysis focused on the behavior of extreme rainfall observations.

Two EVT approaches were used.

### Generalized Extreme Value — GEV

The **Block Maxima** approach was used to extract the maximum rainfall value from each month.

These monthly maxima were then modeled using a Generalized Extreme Value distribution.

Estimated GEV parameters:

* Shape: **−0.24**
* Location: **43.32**
* Scale: **27.93**

The Kolmogorov–Smirnov test produced a p-value of:

**0.79**

---

### Generalized Pareto Distribution — GPD

The second approach used **Peaks Over Threshold (POT)**.

A Mean Residual Life Plot was used to investigate potential thresholds. The analysis identified the **80–90 mm range** as a candidate region, with **90 mm** selected as the working threshold.

Rainfall observations above this threshold were treated as extreme events.

Estimated GPD parameters:

* Shape: **−1.46**
* Location / Threshold: **90 mm**
* Scale: **293.67**

The Kolmogorov–Smirnov test produced a p-value of:

**0.06**

Since this is slightly above the 0.05 significance level used in the research, the fitted GPD was considered compatible with the observed extreme values under the study's testing framework.

---

## 4. Value at Risk

The final stage translated the extreme-value models into quantitative rainfall risk estimates.

VaR was calculated at:

* **90% confidence**
* **95% confidence**
* **99% confidence**

### GEV vs GPD

| Confidence |      GEV |       GPD |
| ---------- | -------: | --------: |
| 90%        | 64.40 mm | 261.04 mm |
| 95%        | 70.22 mm | 263.29 mm |
| 99%        | 78.95 mm | 264.89 mm |

The difference between the two estimates reflects their different purposes.

**GEV** works with block maxima and provides an estimate based on the maximum rainfall observed within each monthly block.

**GPD** focuses specifically on exceedances above the 90 mm threshold and therefore captures the upper tail of the rainfall distribution.

The GPD estimates are substantially higher because the analysis specifically targets the more extreme portion of the rainfall distribution.

---

## Key Findings

### 1. Model complexity did not guarantee better forecasting performance

Increasing the number of hidden neurons did not consistently reduce forecasting error.

The repeated experiments showed that the simplest configuration produced the lowest MAE, while a slightly larger configuration produced the lowest MSE.

### 2. Extreme rainfall requires a different analytical perspective

Standard forecasting metrics alone do not fully describe rare extreme events.

EVT provides a framework for specifically studying the upper tail of the rainfall distribution.

### 3. GEV and GPD answer different questions

The two distributions are complementary:

* **GEV:** monthly block maxima
* **GPD:** observations exceeding an extreme threshold

Using both provides a broader view of extreme rainfall behavior.

### 4. Risk estimates increase with confidence level

For both GEV and GPD, the estimated VaR increased as the confidence level moved from 90% to 99%.

This provides a quantitative way to examine increasingly severe rainfall scenarios.

---

## Limitations

Several limitations should be considered when interpreting the results:

* The dataset covers approximately three years of rainfall observations.
* The forecasting model uses only two lagged rainfall features.
* Additional meteorological variables such as temperature, humidity, and wind were not included.
* ELM performance can be affected by random initialization.
* The EVT estimates depend on the selected modeling approach and threshold.
* VaR estimates describe rainfall extremes and should not be interpreted as a complete hydrological flood model.

The original research therefore recommends expanding the time period, incorporating additional meteorological variables, and comparing ELM with other time-series models such as RNN or LSTM.

---

## Tools & Technologies

* **Python 3.13.1**
* **Pandas**
* **NumPy**
* **SciPy**
* **Scikit-learn**
* **Matplotlib**
* **Excel**
* **Visual Studio Code**

### Statistical / Machine Learning Methods

* Time-series analysis
* Data preprocessing
* Lag features
* Extreme Learning Machine
* ReLU activation
* Mean Absolute Error
* Mean Squared Error
* Extreme Value Theory
* Generalized Extreme Value
* Generalized Pareto Distribution
* Block Maxima
* Peaks Over Threshold
* Mean Residual Life
* Maximum Likelihood Estimation
* Kolmogorov–Smirnov test
* Value at Risk

---

## Repository Structure

```text
Flood-Risk-Analysis/
│
├── data/
│   └── rainfall datasets
│
├── notebooks/
│   └── analysis notebooks
│
├── src/
│   └── Python analysis scripts
│
├── assets/
│   ├── rainfall_distribution.png
│   ├── actual_vs_predicted.png
│   ├── elm_error_comparison.png
│   ├── gev_distribution.png
│   ├── mean_residual_life.png
│   └── gpd_distribution.png
│
├── README.md
└── requirements.txt
```

*Update this structure to match the actual repository files.*

---

## Research Context

This project was developed as my undergraduate thesis in the **Bachelor of Mathematics program at Universitas Syiah Kuala**.

**Research title:**

> *Estimation of Flood Risk Level Using Extreme Learning Machine and Extreme Value Theory (Case Study: Aceh Besar Regency)*

The research was completed in 2025.

---

## What I Learned

This project strengthened my ability to work through a complete quantitative analysis workflow:

* Preparing real-world time-series data
* Handling missing observations
* Engineering lag features
* Building and evaluating a machine learning model
* Comparing model configurations
* Analyzing extreme observations statistically
* Selecting a threshold for tail analysis
* Fitting probability distributions
* Validating statistical assumptions
* Translating statistical outputs into risk estimates
* Communicating quantitative findings in a practical context

More importantly, the project taught me that **model performance should be evaluated against the analytical objective**, rather than assuming that greater model complexity automatically produces better results.

---

## Reference

Muhammad Rusqi Ash Shiddieqy.
*Estimation of Flood Risk Level Using Extreme Learning Machine and Extreme Value Theory (Case Study: Aceh Besar Regency).*
Bachelor's Thesis, Department of Mathematics, Faculty of Mathematics and Natural Sciences, Universitas Syiah Kuala, 2025.
