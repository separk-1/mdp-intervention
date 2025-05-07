import os
import json
import ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# ===== 0. 파일 경로 설정 =====
SUMMARY_PATH = "results/summary.csv"
METADATA_PATH = "results/policy_metadata.json"
OUTPUT_CSV_PATH = "results/summary_with_voi_extended.csv"
FIGURE_DIR = "figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

# ===== 1. CSV 생성 =====
df_summary = pd.read_csv(SUMMARY_PATH)
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

baseline_cost = df_summary[df_summary["intervention_cost"] == 0]["avg_total_cost"].values[0]

for p in metadata:
    p["VoI"] = baseline_cost - p["avg_total_cost"]
    p["VoI_per_cost"] = p["VoI"] / p["intervention_cost"] if p["intervention_cost"] > 0 else 0.0

df_metadata = pd.DataFrame(metadata)

# success_rate와 policy가 summary에 없을 경우 대비
if "success_rate" in df_summary.columns:
    merge_cols = ["policy_id", "policy", "success_rate"]
else:
    merge_cols = ["policy_id", "policy"]

df_merged = pd.merge(df_metadata, df_summary[merge_cols], on="policy_id")

# 필요한 컬럼만 추림
columns_to_keep = [
    "policy_id", "avg_total_cost", "intervention_cost", "policy", "intervene_states", "VoI", "VoI_per_cost"
]
if "success_rate" in df_summary.columns:
    columns_to_keep.insert(3, "success_rate")

df_merged = df_merged[columns_to_keep]
df_merged.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"✅ '{OUTPUT_CSV_PATH}' 생성 완료")

# ===== 2. 분석 =====
df_merged["intervene_states"] = df_merged["intervene_states"].apply(ast.literal_eval)

# 2-1. 상태별 개입 빈도
all_states = [s for states in df_merged["intervene_states"] for s in states]
state_counts = Counter(all_states)

plt.figure(figsize=(6, 4))
plt.bar(state_counts.keys(), state_counts.values(), color='skyblue')
plt.title("Intervention Frequency per State")
plt.xlabel("State")
plt.ylabel("Number of Policies")
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/intervention_frequency.png", dpi=300)
plt.close()

# 2-2. 성공률 95% 이상에서 개입 빈도
if "success_rate" in df_merged.columns:
    df_high_success = df_merged[df_merged["success_rate"] >= 0.95]
    high_success_states = [s for states in df_high_success["intervene_states"] for s in states]
    high_success_counts = Counter(high_success_states)

    plt.figure(figsize=(6, 4))
    plt.bar(high_success_counts.keys(), high_success_counts.values(), color='green')
    plt.title("Intervention Frequency (Success Rate ≥ 95%)")
    plt.xlabel("State")
    plt.ylabel("High Success Policy Count")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/high_success_intervention.png", dpi=300)
    plt.close()

# 2-3. 정책 군집화
mlb = MultiLabelBinarizer()
intervene_encoded = mlb.fit_transform(df_merged["intervene_states"])
pca = PCA(n_components=2)
intervene_pca = pca.fit_transform(intervene_encoded)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(intervene_encoded)

plt.figure(figsize=(6, 5))
plt.scatter(intervene_pca[:, 0], intervene_pca[:, 1], c=clusters, cmap='Set1', s=50)
plt.title("Policy Clustering (PCA + KMeans)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/policy_clustering.png", dpi=300)
plt.close()

# 2-4. 성공률 vs 개입비용
if "success_rate" in df_merged.columns:
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df_merged, x="intervention_cost", y="success_rate", hue="success_rate", palette="viridis", s=80)
    plt.title("Success Rate vs Intervention Cost")
    plt.xlabel("Intervention Cost")
    plt.ylabel("Success Rate")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/success_vs_cost.png", dpi=300)
    plt.close()

# 2-5. 개입 조합별 성공률 히트맵
if "success_rate" in df_merged.columns:
    heatmap_data = pd.DataFrame(intervene_encoded, columns=mlb.classes_)
    heatmap_data["success_rate"] = df_merged["success_rate"]

    plt.figure(figsize=(8, 5))
    sns.heatmap(
        heatmap_data.groupby(list(mlb.classes_)).mean().reset_index().set_index(list(mlb.classes_)),
        cmap="YlGnBu", annot=False
    )
    plt.title("Success Rate Heatmap by Intervention Pattern")
    plt.tight_layout()
    plt.savefig(f"{FIGURE_DIR}/success_rate_heatmap.png", dpi=300)
    plt.close()

print("✅ 모든 분석 결과가 'figures/' 폴더에 저장되었습니다.")
