from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetProfile:
    name: str
    share: float
    currency: str


PROFILES = [
    DatasetProfile("PaySim mobile money", 0.38, "INR"),
    DatasetProfile("IEEE-CIS e-commerce", 0.24, "INR"),
    DatasetProfile("European card", 0.18, "EUR"),
    DatasetProfile("Bank transactions", 0.12, "INR"),
    DatasetProfile("AMLSim network", 0.08, "INR"),
]


def _weighted_sources(rng: np.random.Generator, size: int) -> np.ndarray:
    return rng.choice([profile.name for profile in PROFILES], size=size, p=[p.share for p in PROFILES])


def build_demo_data(seed: int = 42, transactions: int = 4800) -> pd.DataFrame:
    """Create a deterministic multi-source stream with realistic user histories."""
    rng = np.random.default_rng(seed)
    user_count = max(260, transactions // 18)
    users = np.array([f"U{index:04d}" for index in range(1001, 1001 + user_count)])
    user_mean = rng.lognormal(mean=np.log(1200), sigma=0.72, size=user_count)
    user_map = dict(zip(users, user_mean))

    user_ids = rng.choice(users, transactions)
    sources = _weighted_sources(rng, transactions)
    timestamps = pd.Timestamp("2026-09-17 00:00:00") - pd.to_timedelta(
        rng.integers(0, 30 * 24 * 60, transactions), unit="m"
    )
    amounts = np.maximum(40, rng.lognormal(np.log([user_map[user] for user in user_ids]), 0.68))
    locations = rng.choice(["Bhopal", "Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad"], transactions,
                           p=[0.30, 0.19, 0.16, 0.14, 0.12, 0.09])
    devices = rng.choice([f"D-{index:03d}" for index in range(1, 155)], transactions)
    merchants = rng.choice([f"M-{index:03d}" for index in range(1, 95)], transactions)
    methods = rng.choice(["UPI", "Card", "Wallet", "Bank transfer"], transactions, p=[0.48, 0.27, 0.15, 0.10])
    transaction_types = rng.choice(["PAYMENT", "CASH_OUT", "TRANSFER", "PURCHASE", "DEBIT"], transactions)

    frame = pd.DataFrame({
        "transaction_id": [f"TX-{index:06d}" for index in range(1, transactions + 1)],
        "source": sources,
        "user_id": user_ids,
        "amount": amounts.round(2),
        "timestamp": timestamps,
        "merchant_id": merchants,
        "location": locations,
        "device_id": devices,
        "payment_method": methods,
        "transaction_type": transaction_types,
    }).sort_values("timestamp").reset_index(drop=True)

    # Inject a small, inspectable fraud cohort into the stream.
    fraud_count = max(45, transactions // 32)
    fraud_indexes = rng.choice(frame.index.to_numpy(), fraud_count, replace=False)
    frame["is_fraud"] = 0
    frame.loc[fraud_indexes, "is_fraud"] = 1
    cluster_users = rng.choice(users, size=min(4, user_count), replace=False)
    frame.loc[fraud_indexes, "user_id"] = rng.choice(cluster_users, fraud_count)
    frame.loc[fraud_indexes, "amount"] *= rng.uniform(5.5, 16.0, fraud_count)
    frame.loc[fraud_indexes, "amount"] = frame.loc[fraud_indexes, "amount"].round(2)
    frame.loc[fraud_indexes, "location"] = rng.choice(["Delhi", "Mumbai", "Dubai"], fraud_count)
    frame.loc[fraud_indexes, "device_id"] = "D-NEW-NETWORK"
    frame.loc[fraud_indexes, "timestamp"] = pd.Timestamp("2026-09-17 03:12:00") + pd.to_timedelta(
        rng.integers(0, 4 * 60, fraud_count), unit="s"
    )

    frame["hour"] = frame["timestamp"].dt.hour
    frame["user_average"] = frame["user_id"].map(
        frame[frame["is_fraud"] == 0].groupby("user_id")["amount"].median()
    ).fillna(frame["amount"].median()).round(2)
    frame["user_tx_count"] = frame.groupby("user_id")["transaction_id"].transform("count")
    frame["source_currency"] = frame["source"].map({profile.name: profile.currency for profile in PROFILES})
    frame["user_known_devices"] = frame.groupby("user_id")["device_id"].transform("nunique")
    frame["transactions_10m"] = (
        frame.sort_values(["user_id", "timestamp"])
        .groupby("user_id", group_keys=False)
        .apply(_rolling_transaction_count, include_groups=False)
        .reindex(frame.index)
        .fillna(1)
        .astype(int)
    )
    return frame.sort_values("timestamp", ascending=False).reset_index(drop=True)


def _rolling_transaction_count(group: pd.DataFrame) -> pd.Series:
    timestamps = group["timestamp"]
    counts = pd.Series(1, index=pd.DatetimeIndex(timestamps))
    return pd.Series(counts.rolling("10min").sum().to_numpy(), index=group.index)
