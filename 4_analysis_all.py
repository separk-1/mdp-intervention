import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import matplotlib

# Times New Roman 설정
matplotlib.rcParams['font.family'] = 'Times New Roman'

# 경로
SUMMARY_PATH = "results/summary.csv"
METADATA_PATH = "results/policy_metadata.json"
FIGURE_DIR = "figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

# Load
df = pd.read_csv(SUMMARY_PATH)
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

# Total Cost vs Intervention Cost
df_sorted = df.sort_values("avg_total_cost")
plt.figure(figsize=(8, 6))
scatter = sns.scatterplot(
    data=df_sorted,
    x="intervention_cost",
    y="avg_total_cost",
    hue="avg_total_cost",
    palette="viridis",
    s=100,
    edgecolor='black',
    legend=False
)
# Top-N 라벨링
top_n = 5
top_policies = df_sorted.head(top_n)
for _, row in top_policies.iterrows():
    plt.text(row["intervention_cost"], row["avg_total_cost"] + 0.5,
             str(int(row["policy_id"])), fontsize=9,
             ha='center', va='bottom', color='black')

plt.title("Policy Comparison: Total Cost vs Intervention Cost", fontsize=14)
plt.xlabel("Total Intervention Cost", fontsize=12)
plt.ylabel("Average Total Cost (Simulation Outcome)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/policy_cost_tradeoff.png", dpi=300)
plt.close()

# VoI 계산
df_sorted = df_sorted.reset_index(drop=True)
baseline_cost = df_sorted[df_sorted["intervention_cost"] == 0]["avg_total_cost"].values[0]
df_sorted["VoI"] = baseline_cost - df_sorted["avg_total_cost"]
df_sorted["VoI_per_cost"] = df_sorted.apply(
    lambda row: row["VoI"] / row["intervention_cost"] if row["intervention_cost"] > 0 else 0,
    axis=1
)
df_sorted.to_csv(os.path.join(FIGURE_DIR, "summary_with_voi.csv"), index=False)

# Heatmap
state_list = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5']
voi_matrix = pd.DataFrame([{
    'policy_id': p['policy_id'],
    **{s: p['VoI'] if s in p['intervene_states'] else 0 for s in state_list}
} for p in metadata]).set_index('policy_id')

plt.figure(figsize=(10, 6))
sns.heatmap(voi_matrix, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={"label": "VoI"})
plt.title("VoI per State per Policy", fontsize=14)
plt.xlabel("Intervention State", fontsize=12)
plt.ylabel("Policy ID", fontsize=12)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/voi_heatmap.png", dpi=300)
plt.close()

# Pareto Front
plt.figure(figsize=(8, 6))
sc = plt.scatter(
    df_sorted["intervention_cost"],
    df_sorted["VoI"],
    c=df_sorted["VoI_per_cost"],
    cmap="plasma",
    s=100,
    edgecolors='k'
)
plt.colorbar(sc, label="VoI per Cost")

# Top-N 라벨링 (Pareto)
top_pareto = df_sorted.sort_values("VoI_per_cost", ascending=False).head(top_n)
for _, row in top_pareto.iterrows():
    plt.text(row["intervention_cost"], row["VoI"] + 0.5,
             str(int(row["policy_id"])), fontsize=9,
             ha='center', va='bottom', color='black')

plt.title("Pareto Front: Intervention Cost vs VoI", fontsize=14)
plt.xlabel("Intervention Cost", fontsize=12)
plt.ylabel("VoI (Risk Reduction)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pareto_voi_front.png", dpi=300)
plt.close()
# --- Top 5 (by avg_total_cost)
print("\n🔹 Top 5 Policies by Lowest Average Total Cost:")
print(top_policies[["policy_id", "avg_total_cost", "intervention_cost"]])

# --- Top 5 (by VoI_per_cost)
print("\n🔸 Top 5 Policies by Highest VoI per Cost:")
print(top_pareto[["policy_id", "VoI", "intervention_cost", "VoI_per_cost"]])
