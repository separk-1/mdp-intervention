import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load simulation result
with open("./results/run1_result.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Create output directory
os.makedirs("figures", exist_ok=True)

# --- Summary statistics ---
print("--- Summary Statistics ---")
print(df["total_cost"].describe())
print("\nFinal State Distribution:")
print(df["final_state"].value_counts())

# --- 1. Total cost distribution ---
plt.figure(figsize=(8, 5))
sns.histplot(df["total_cost"], bins=30, kde=True)
plt.title("Distribution of Total Cost over Simulations")
plt.xlabel("Total Cost")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/total_cost_distribution.png", dpi=300)
plt.close()

# --- 2. Final state pie chart ---
plt.figure(figsize=(6, 6))
df["final_state"].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Final State Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("figures/final_state_pie.png", dpi=300)
plt.close()

# --- 3. Cost by intervention strategy ---
if "intervention" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="intervention", y="total_cost")
    plt.title("Total Cost by Intervention Strategy")
    plt.xlabel("Intervention")
    plt.ylabel("Total Cost")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("figures/total_cost_by_intervention.png", dpi=300)
    plt.close()

# --- 4. Phase-level cost heatmap ---
if "cost_by_phase" in df.columns:
    cost_df = df["cost_by_phase"].apply(pd.Series)
    cost_mean = cost_df.mean().sort_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=cost_mean.index, y=cost_mean.values)
    plt.title("Average Cost by Phase")
    plt.xlabel("Phase")
    plt.ylabel("Mean Cost")
    plt.tight_layout()
    plt.savefig("figures/avg_cost_by_phase.png", dpi=300)
    plt.close()

# --- 5. Risk reduction heatmap ---
if "risk_reduction_by_phase" in df.columns:
    risk_df = df["risk_reduction_by_phase"].apply(pd.Series)
    risk_mean = risk_df.mean().sort_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=risk_mean.index, y=risk_mean.values)
    plt.title("Average Risk Reduction by Phase")
    plt.xlabel("Phase")
    plt.ylabel("Mean Risk Reduction")
    plt.tight_layout()
    plt.savefig("figures/avg_risk_reduction_by_phase.png", dpi=300)
    plt.close()

# --- 6. Value of Information (VoI) Distribution ---
if "VoI" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["VoI"], bins=30, kde=True)
    plt.title("Distribution of Value of Information (VoI)")
    plt.xlabel("VoI")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("figures/voi_distribution.png", dpi=300)
    plt.close()

# --- 7. VoI by intervention point ---
if "VoI_by_intervention" in df.columns:
    voi_df = df["VoI_by_intervention"].apply(pd.Series)
    voi_mean = voi_df.mean().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=voi_mean.index, y=voi_mean.values)
    plt.title("Average VoI by Intervention Point")
    plt.xlabel("Intervention Point")
    plt.ylabel("Mean VoI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("figures/avg_voi_by_intervention_point.png", dpi=300)
    plt.close()

# --- 8. Trajectory length distribution ---
if "trajectory" in df.columns:
    df["trajectory_length"] = df["trajectory"].apply(len)
    plt.figure(figsize=(8, 5))
    sns.histplot(df["trajectory_length"], bins=30)
    plt.title("Trajectory Length Distribution")
    plt.xlabel("Number of States")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("figures/trajectory_length_distribution.png", dpi=300)
    plt.close()
