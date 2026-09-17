# 🏦 FinGuard — Financial Fraud Intelligence Platform

> **A multi-source fraud detection and investigation platform that combines machine learning, behavioral analytics, anomaly detection, and graph-based analysis to identify suspicious financial activity.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)](https://www.postgresql.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io/)

---

## 🚨 Problem Statement

Financial platforms process millions of transactions every day. Detecting fraudulent activity is challenging because:

* Fraud represents only a small fraction of transactions.
* Fraud patterns continuously change.
* Genuine users can have unusual transactions.
* Rule-based systems can generate large numbers of false alerts.
* Fraud may involve multiple accounts, devices, merchants, and transactions.

**FinGuard** addresses this problem by combining transaction-level machine learning with behavioral analysis, anomaly detection, and relationship-based investigation.

---

# 🎯 Project Objective

FinGuard aims to answer four important questions:

1. **Is this transaction suspicious?**
2. **Why is it suspicious?**
3. **Is this behavior unusual for the customer?**
4. **Is the transaction connected to a larger suspicious network?**

Instead of producing only:

```text
Fraud = 1
```

FinGuard generates an explainable risk assessment:

```text
Risk Score: 91/100
Risk Level: CRITICAL

Reasons:
✓ Transaction amount significantly exceeds normal behavior
✓ Unknown device detected
✓ Unusual transaction time
✓ High transaction velocity
✓ Connected to a suspicious account cluster
```

---

# ✨ Key Features

### 🔍 1. Transaction Fraud Detection

Machine learning models analyze transaction characteristics and estimate fraud probability.

Supported models include:

* Logistic Regression
* Random Forest
* XGBoost
* LightGBM

---

### 🧠 2. Behavioral Profiling

FinGuard learns a customer's historical transaction behavior.

It analyzes:

* Average transaction amount
* Transaction frequency
* Typical transaction time
* Common locations
* Known devices
* Merchant categories
* Transaction velocity

Example:

```text
Normal User Behavior
────────────────────────────
Average Amount: ₹1,250
Typical Time: 08:00–22:00
Known Location: Bhopal
Known Devices: 2

Current Transaction
────────────────────────────
Amount: ₹75,000
Time: 03:14 AM
Location: Mumbai
Device: Unknown

→ High Behavioral Anomaly
```

---

### 🚨 3. Anomaly Detection

FinGuard detects unusual transactions even when they don't exactly match previously known fraud patterns.

Algorithms:

* Isolation Forest
* DBSCAN
* Autoencoder-based detection

---

### 🔗 4. Fraud Network Detection

Fraud can involve multiple connected entities.

FinGuard creates relationships between:

```text
Customer
   ↓
Account
   ↓
Device
   ↓
Merchant
   ↓
Transaction
   ↓
Other Account
```

Graph analysis can identify suspicious clusters such as:

```text
Account A ─── Device X ─── Account B
     │                         │
     └──── Merchant Y ─────────┘
                │
            Account C
```

This allows investigators to look beyond individual transactions.

---

### 📊 5. Explainable AI

FinGuard doesn't simply predict fraud.

It explains the important factors contributing to the prediction using techniques such as **SHAP**.

Example:

```text
Transaction Risk: 92%

Major contributing factors:

Amount deviation        +31%
New device               +24%
Transaction velocity     +18%
Unusual location         +11%
Night-time activity       +8%
```

---

### ⚡ 6. Real-Time Transaction Simulation

Transactions can be streamed into the system:

```text
10:31:02   ₹450       LOW
10:31:05   ₹820       LOW
10:31:17   ₹1,200     LOW
10:31:28   ₹75,000    🔴 HIGH
```

The system calculates a risk score and generates an alert.

---

### 📈 7. Fraud Analytics Dashboard

The dashboard provides:

* Total transactions
* Fraudulent transactions
* Suspicious transactions
* Amount at risk
* Fraud trends
* Fraud by transaction type
* Fraud by location
* Fraud by merchant
* Risk distribution
* Suspicious account networks

---

# 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │   Transaction Data  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Data Ingestion    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Data Cleaning & ETL │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Feature Engineering │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       ┌───────────┐ ┌─────────────┐ ┌────────────┐
       │ ML Model  │ │  Anomaly    │ │ Behavioral │
       │           │ │  Detection  │ │  Analysis  │
       └─────┬─────┘ └──────┬──────┘ └──────┬─────┘
             │              │               │
             └──────────────┼───────────────┘
                            ▼
                  ┌──────────────────┐
                  │   Risk Engine    │
                  └────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          ┌─────────────┐     ┌──────────────┐
          │ Fraud Alert │     │ Investigation│
          └─────────────┘     │   Dashboard  │
                              └──────────────┘
```

---

# 📚 Datasets

FinGuard is designed as a **multi-source fraud analytics platform**.

### 1. PaySim

A large synthetic mobile-money transaction dataset containing approximately **6.3 million transactions**.

Useful for:

* Mobile payment fraud
* Transfer fraud
* Cash-out fraud
* Transaction behavior analysis

---

### 2. IEEE-CIS Fraud Detection

A large e-commerce transaction dataset with transaction, identity, device, and other anonymized features.

Useful for:

* Online payment fraud
* Device-based analysis
* Identity-related patterns

---

### 3. Credit Card Fraud Detection

A widely used European credit-card transaction dataset containing **284,807 transactions**.

Useful for:

* Credit-card fraud classification
* Imbalanced classification
* Model benchmarking

---

### 4. IBM AMLSim

Synthetic financial transaction networks designed for anti-money-laundering research.

Useful for:

* Account networks
* Suspicious transaction chains
* Money-laundering patterns
* Graph analytics

---

## 🧩 Data Strategy

The datasets are **not blindly merged into one CSV** because they represent different domains and schemas.

Instead:

```text
PaySim ─────────────┐
IEEE-CIS ───────────┤
Credit Card ────────┤
AMLSim ─────────────┘
          ↓
   Source Adapters
          ↓
 Common Analytical Layer
          ↓
 ┌────────┴─────────┐
 ↓                  ↓
ML Models       Investigation
```

This allows each dataset to retain its original characteristics while supporting common analytical features.

---

# 🧪 Machine Learning Pipeline

```text
Raw Data
   ↓
Missing Value Treatment
   ↓
Duplicate Detection
   ↓
Categorical Encoding
   ↓
Feature Engineering
   ↓
Class Imbalance Handling
   ↓
Train / Validation / Test Split
   ↓
Model Training
   ↓
Hyperparameter Tuning
   ↓
Model Evaluation
   ↓
Explainability
```

---

# ⚙️ Feature Engineering

Example features include:

```text
amount
transaction_frequency
average_amount
amount_deviation
transactions_last_1h
transactions_last_24h
new_device
new_location
night_transaction
merchant_frequency
account_age
time_since_previous_transaction
```

Behavioral features are calculated relative to individual customer history where the required information is available.

---

# 📐 Risk Scoring

FinGuard combines multiple signals:

```text
                 ML Fraud Score
                        +
              Behavioral Score
                        +
               Anomaly Score
                        +
                Network Risk
                        ↓
                 Risk Engine
                        ↓
                  Risk Score
```

Example:

```text
ML Score:          0.84
Behavior Score:    0.91
Anomaly Score:     0.76
Network Score:     0.88
────────────────────────────
Final Risk:        0.86
```

The final score is a **prototype decision-support metric**, not a real banking risk threshold.

---

# 📊 Evaluation Metrics

Because fraud datasets are often highly imbalanced, accuracy alone is not sufficient.

FinGuard evaluates:

* Precision
* Recall
* F1 Score
* PR-AUC
* ROC-AUC
* False Positive Rate
* False Negative Rate
* Confusion Matrix

Special attention is given to the trade-off between detecting fraud and incorrectly flagging legitimate transactions.

---

# 🖥️ Dashboard

### Overview

```text
┌─────────────────────────────────────────┐
│             FINGUARD                    │
├────────────┬────────────┬───────────────┤
│ 8.4M       │ 24.8K      │ ₹18.4L        │
│ Transactions│ Suspicious │ Amount at Risk│
├────────────┴────────────┴───────────────┤
│                                         │
│          Fraud Trend                    │
│       ╱╲      ╱╲                        │
│  ╱╲  ╱  ╲____╱  ╲                       │
│                                         │
├─────────────────────────────────────────┤
│ Risk Distribution                       │
│ 🟢 Low      🟡 Medium    🔴 Critical    │
└─────────────────────────────────────────┘
```

---

# 🔎 Investigation Workflow

```text
Suspicious Transaction
          ↓
       Alert
          ↓
   Transaction Details
          ↓
   Customer History
          ↓
   Behavioral Analysis
          ↓
   Connected Entities
          ↓
   Graph Investigation
          ↓
   Explainable Risk Report
```

---

# 🛠️ Technology Stack

### Programming

* Python
* SQL

### Data Engineering

* Pandas
* NumPy
* PySpark
* Parquet

### Machine Learning

* Scikit-learn
* XGBoost
* LightGBM

### Anomaly Detection

* Isolation Forest
* DBSCAN

### Graph Analytics

* NetworkX

### Explainable AI

* SHAP

### Backend

* FastAPI

### Database

* PostgreSQL

### Visualization

* Plotly
* Streamlit

### Deployment

* Docker
* Streamlit Cloud
* Render / Railway

---

# 📁 Project Structure

```text
FinGuard/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── transactions.py
│   │   ├── fraud.py
│   │   └── investigation.py
│   │
│   ├── services/
│   │   ├── risk_engine.py
│   │   ├── behavior.py
│   │   ├── anomaly.py
│   │   ├── graph_analysis.py
│   │   └── explanation.py
│   │
│   └── database/
│       ├── connection.py
│       └── models.py
│
├── ml/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   └── explain.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── parquet/
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │   ├── overview.py
│   │   ├── transactions.py
│   │   ├── alerts.py
│   │   └── networks.py
│   └── components/
│
├── notebooks/
│   ├── eda.ipynb
│   ├── feature_engineering.ipynb
│   └── model_experiments.ipynb
│
├── tests/
│
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

---

# 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FinGuard.git

cd FinGuard
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Configuration

Create a PostgreSQL database and configure environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/finguard
```

Additional API keys or configuration values should be stored in `.env` and excluded from Git.

---

# ▶️ Running the Project

### Start FastAPI

```bash
uvicorn backend.main:app --reload
```

### Start Streamlit

```bash
streamlit run dashboard/app.py
```

Open the dashboard locally and begin analyzing transactions.

---

# 🔌 Example API

### Analyze Transaction

```http
POST /api/v1/fraud/predict
```

Example request:

```json
{
  "customer_id": "C10291",
  "amount": 78500,
  "transaction_type": "TRANSFER",
  "device_id": "D9281",
  "location": "Mumbai"
}
```

Example response:

```json
{
  "risk_score": 91,
  "risk_level": "CRITICAL",
  "fraud_probability": 0.91,
  "reasons": [
    "Unusual transaction amount",
    "New device",
    "Unusual location",
    "High transaction velocity"
  ]
}
```

---

# 🔐 Security & Responsible Use

FinGuard is an **educational/research prototype**.

It does not represent a production banking fraud-detection system.

Real-world financial systems require:

* Secure authentication
* Encryption
* Access control
* Regulatory compliance
* Data privacy
* Model governance
* Continuous monitoring
* Human review
* Robust fraud-labeling processes

No real customer financial information should be used in this project.

---

# 🔮 Future Improvements

* Real-time Kafka transaction streaming
* Apache Spark distributed processing
* Graph Neural Networks
* Advanced AML detection
* Automated case management
* Model drift detection
* Real-time model monitoring
* SHAP-based investigation reports
* Cloud deployment
* Role-based investigator access
* Feedback loop from fraud investigators

---

# 📌 Current Status

**Project Status:** 🚧 In Development

### Planned milestones

* [x] Project architecture
* [ ] Dataset ingestion
* [ ] Data preprocessing
* [ ] Exploratory analysis
* [ ] Feature engineering
* [ ] Baseline ML model
* [ ] Anomaly detection
* [ ] Behavioral profiling
* [ ] Risk engine
* [ ] FastAPI backend
* [ ] PostgreSQL integration
* [ ] Fraud dashboard
* [ ] Graph investigation
* [ ] Explainable AI
* [ ] Dockerization
* [ ] Deployment

---

# 👩‍💻 Author

**Bhumika Sen**

B.Tech Computer Science Engineering
Bhopal, India

### Skills Demonstrated

`Python` `SQL` `Data Analytics` `Machine Learning` `FastAPI` `PostgreSQL` `PySpark` `NLP/AI` `Graph Analytics` `Data Visualization`

---

## ⭐ Why FinGuard?

FinGuard goes beyond traditional fraud classification by combining:

**Machine Learning + Behavioral Analytics + Anomaly Detection + Graph Analytics + Explainable AI + Data Engineering**

> **Detect the transaction. Understand the behavior. Investigate the network.**
