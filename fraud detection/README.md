# FinGuard

FinGuard is a research prototype for explainable financial fraud investigation. It combines a multi-source transaction stream, customer behavior signals, anomaly scoring, and shared-identity graph pivots in a Streamlit operations dashboard.

## Run it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit.

## Included data sources

The generator creates a deterministic, inspectable dataset with PaySim-style mobile-money records, IEEE-CIS-style e-commerce records, European card records, bank transaction records, and AMLSim-style network records. The records are synthetic and source labels describe the scenario shape; they are not downloaded copies of those datasets.

The demo includes 4,800 transactions, user-level medians, timestamps, locations, devices, merchants, payment methods, transaction types, injected fraud cases, behavioral 10-minute velocity features, and a deliberately shared fraud-device cluster for network investigation. Replace `build_demo_data()` with licensed/public data ingestion when moving beyond the prototype.

## Risk model

The risk score is a transparent prototype composite of amount, time, location, device, velocity, and network signals. Velocity is calculated from the customer's observed transactions in a rolling 10-minute window; it does not use the synthetic fraud label. It is designed for dashboard demonstration and is not a production banking control. Production work would require calibrated models, temporal validation, feature stores, data governance, model monitoring, access controls, and a reviewed alert policy.

## Project shape

- `app.py`: Streamlit command center, investigation view, and identity network view
- `finguard/data.py`: reproducible multi-source data generator
- `finguard/risk.py`: explainable signal and risk scoring
- `finguard/graph.py`: shared-device identity graph helpers
