import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

SUMMARY_PATH = "results/summary.csv"
METADATA_PATH = "results/policy_metadata.json"
FIGURE_DIR = "figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

# Load summary and metadata
df = pd.read_csv(SUMMARY_PATH)
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

# --- Policy 비교: 개입 비용 vs 시뮬레이션 결과 ---
df_sorted = df.sort_values("avg_total_cost")
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df_sorted,
    x="intervention_cost",
    y="avg_total_cost",
    hue="avg_total_cost",
    palette="viridis",
    s=100,
    edgecolor='black'
)
plt.title("Policy Comparison: Total Cost vs Intervention Cost")
plt.xlabel("Total Intervention Cost")
plt.ylabel("Average Total Cost (Simulation Outcome)")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/policy_cost_tradeoff.png", dpi=300)
plt.close()

# 상위 5개 정책 출력 및 저장
top5 = df_sorted.head(5)
print("🔍 Top 5 Cost-Effective Policies:")
print(top5[["policy_id", "avg_total_cost", "intervention_cost"]])
top5.to_csv(f"{FIGURE_DIR}/top5_policies.csv", index=False)

# --- VoI 계산 ---
df_sorted = df.sort_values("avg_total_cost").reset_index(drop=True)
baseline_cost = df_sorted[df_sorted["intervention_cost"] == 0]["avg_total_cost"].values[0]
df_sorted["VoI"] = baseline_cost - df_sorted["avg_total_cost"]
df_sorted["VoI_per_cost"] = df_sorted.apply(
    lambda row: row["VoI"] / row["intervention_cost"] if row["intervention_cost"] > 0 else 0,
    axis=1
)
df_sorted_top = df_sorted.sort_values("VoI_per_cost", ascending=False).head(10)
df_sorted_top.to_csv(f"{FIGURE_DIR}/top_voi_per_cost.csv", index=False)

print("\n🔍 Top 5 VoI/Cost Policies:")
print(df_sorted_top[["policy_id", "avg_total_cost", "intervention_cost", "VoI", "VoI_per_cost"]])
df_sorted.to_csv(os.path.join(FIGURE_DIR, "summary_with_voi.csv"), index=False)

# --- 🔎 Policy 개입 위치 확인 ---
print("\n📌 Intervention States per Policy:")
for p in metadata:
    print(f"Policy {p['policy_id']:>3}: {sorted(p['intervene_states'])}")

# --- 🔥 VoI Heatmap per State ---
state_list = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5']
voi_matrix = pd.DataFrame([
    {**{'policy_id': p['policy_id']},
     **{s: p['VoI'] if s in p['intervene_states'] else 0 for s in state_list}}
    for p in metadata
]).set_index('policy_id')

plt.figure(figsize=(10, 6))
sns.heatmap(voi_matrix, annot=True, cmap="YlGnBu", cbar_kws={"label": "VoI"})
plt.title("VoI per State per Policy")
plt.xlabel("Intervention State")
plt.ylabel("Policy ID")
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/voi_heatmap.png", dpi=300)
plt.close()

# --- 📈 Pareto Front (Cost vs VoI) ---
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
plt.title("Pareto Front: Intervention Cost vs VoI")
plt.xlabel("Intervention Cost")
plt.ylabel("VoI (Risk Reduction)")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pareto_voi_front.png", dpi=300)
plt.close()

print(f"✅ All plots and files saved to {FIGURE_DIR}/")
