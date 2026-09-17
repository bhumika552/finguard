from __future__ import annotations

import networkx as nx
import pandas as pd


def build_identity_graph(transactions: pd.DataFrame, selected_user: str | None = None) -> nx.Graph:
    graph = nx.Graph()
    subset = transactions if selected_user is None else transactions[transactions["user_id"] == selected_user]
    for row in subset.itertuples(index=False):
        user = f"user:{row.user_id}"
        device = f"device:{row.device_id}"
        merchant = f"merchant:{row.merchant_id}"
        graph.add_node(user, kind="user", label=row.user_id)
        graph.add_node(device, kind="device", label=row.device_id)
        graph.add_node(merchant, kind="merchant", label=row.merchant_id)
        graph.add_edge(user, device, relation="uses")
        graph.add_edge(user, merchant, relation="pays")
    return graph


def shared_identity_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    summary = transactions.groupby("device_id").agg(
        accounts=("user_id", "nunique"),
        transactions=("transaction_id", "count"),
        suspicious=("risk_score", lambda values: int((values >= 60).sum())),
    ).reset_index()
    return summary[summary["accounts"] > 1].sort_values(["suspicious", "accounts"], ascending=False)


def graph_plot_data(graph: nx.Graph) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return stable node and edge tables for a Plotly identity graph."""
    positions = nx.spring_layout(graph, seed=7, k=1.2)
    nodes = pd.DataFrame([
        {
            "node": node,
            "label": attrs["label"],
            "type": attrs["kind"],
            "x": positions[node][0],
            "y": positions[node][1],
        }
        for node, attrs in graph.nodes(data=True)
    ])
    edges = pd.DataFrame([
        {
            "x": [positions[source][0], positions[target][0], None],
            "y": [positions[source][1], positions[target][1], None],
        }
        for source, target in graph.edges()
    ])
    return nodes, edges
