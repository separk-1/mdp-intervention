import json
import pandas as pd
import os

# File paths
SUMMARY_PATH = "results/summary.csv"
METADATA_PATH = "results/policy_metadata.json"

# Load summary
df_summary = pd.read_csv(SUMMARY_PATH)

# Load metadata
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

# Get baseline (no intervention) average total cost
baseline_cost = df_summary[df_summary["intervention_cost"] == 0]["avg_total_cost"].values[0]

# Add VoI and VoI_per_cost
for p in metadata:
    p["VoI"] = baseline_cost - p["avg_total_cost"]
    p["VoI_per_cost"] = p["VoI"] / p["intervention_cost"] if p["intervention_cost"] > 0 else 0.0

# Save updated metadata
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Updated metadata with VoI and VoI_per_cost.\nSaved to: {METADATA_PATH}")
