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

# Create output directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Summary statistics
print("--- Summary Statistics ---")
print(df["total_cost"].describe())
print("\nFinal State Distribution:")
print(df["final_state"].value_counts())

# Plot distribution of total cost
plt.figure(figsize=(8, 5))
sns.histplot(df["total_cost"], bins=30, kde=True)
plt.title("Distribution of Total Cost over Simulations")
plt.xlabel("Total Cost")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/total_cost_distribution.png", dpi=300)
plt.close()

# Final state pie chart
plt.figure(figsize=(6, 6))
df["final_state"].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Final State Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("figures/final_state_pie.png", dpi=300)
plt.close()
