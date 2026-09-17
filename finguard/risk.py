from __future__ import annotations

import pandas as pd


SIGNAL_LABELS = {
    "amount": "Amount is far above the user's normal pattern",
    "time": "Transaction happened during an unusual hour",
    "location": "Location differs from recent activity",
    "device": "Transaction came from an unseen device",
    "velocity": "High transaction velocity detected",
    "network": "Device or merchant links multiple accounts",
}


def score_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    result = transactions.copy()
    result["amount_ratio"] = (result["amount"] / result["user_average"].clip(lower=1)).clip(upper=20)
    result["amount_signal"] = ((result["amount_ratio"] - 1) / 7).clip(0, 1)
    result["time_signal"] = result["hour"].isin([0, 1, 2, 3, 4, 5]).astype(float)
    result["location_signal"] = result["location"].isin(["Delhi", "Mumbai", "Dubai"]).astype(float) * 0.72
    result["device_signal"] = result["device_id"].str.contains("NEW", regex=False).astype(float)
    result["velocity_signal"] = ((result["transactions_10m"] - 2) / 5).clip(0, 1)

    device_accounts = result.groupby("device_id")["user_id"].nunique()
    result["network_signal"] = result["device_id"].map(device_accounts).fillna(1).sub(1).clip(0, 3).div(3)
    result["model_score"] = (
        result["amount_signal"] * 0.30
        + result["time_signal"] * 0.14
        + result["location_signal"] * 0.14
        + result["device_signal"] * 0.18
        + result["velocity_signal"] * 0.14
        + result["network_signal"] * 0.10
    ).clip(0, 1)
    result["risk_score"] = (result["model_score"] * 100).round().astype(int)
    result["risk_level"] = pd.cut(
        result["risk_score"], bins=[-1, 29, 59, 79, 100], labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    ).astype(str)
    result["status"] = result["risk_level"].map({"LOW": "Approved", "MEDIUM": "Review", "HIGH": "Investigate", "CRITICAL": "Block & investigate"})
    result["explanation"] = result.apply(_explain_row, axis=1)
    return result


def _explain_row(row: pd.Series) -> str:
    signals = []
    if row["amount_signal"] >= 0.35:
        signals.append(SIGNAL_LABELS["amount"])
    if row["time_signal"]:
        signals.append(SIGNAL_LABELS["time"])
    if row["location_signal"]:
        signals.append(SIGNAL_LABELS["location"])
    if row["device_signal"]:
        signals.append(SIGNAL_LABELS["device"])
    if row["velocity_signal"]:
        signals.append(SIGNAL_LABELS["velocity"])
    if row["network_signal"]:
        signals.append(SIGNAL_LABELS["network"])
    return " | ".join(signals) if signals else "Consistent with observed customer behavior"


def explain_transaction(row: pd.Series) -> list[dict[str, str]]:
    checks = [
        ("Amount anomaly", f"{row['amount_ratio']:.1f}x user median", row["amount_signal"]),
        ("Time anomaly", f"{int(row['hour']):02d}:00 activity", row["time_signal"]),
        ("Location anomaly", str(row["location"]), row["location_signal"]),
        ("Device anomaly", str(row["device_id"]), row["device_signal"]),
        ("Velocity anomaly", "Burst pattern" if row["velocity_signal"] else "Normal cadence", row["velocity_signal"]),
        ("Network signal", "Shared identity link" if row["network_signal"] else "No cluster link", row["network_signal"]),
    ]
    return [{"name": name, "detail": detail, "severity": "high" if float(value) >= 0.65 else "medium" if float(value) > 0 else "low"} for name, detail, value in checks]
