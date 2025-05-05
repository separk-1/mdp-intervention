import json
import os
from src.mdp import load_mdp
from src.utils import sample_next_state, get_action_from_policy, log_run_result
from pathlib import Path

# Simulation config
NUM_RUNS = 10000
MAX_STEPS = 10

# File paths
MDP_PATH = "data/tmi_mdp.json"
POLICY_LIST_PATH = "data/policy_list.json"
RESULTS_DIR = "results"

# Load MDP and policy list
mdp = load_mdp(MDP_PATH)
with open(POLICY_LIST_PATH, "r") as f:
    policy_list = json.load(f)

os.makedirs(RESULTS_DIR, exist_ok=True)

# Simulation core
def run_simulation(mdp, policy_fn, num_runs=NUM_RUNS, max_steps=MAX_STEPS):
    results = []
    for run in range(num_runs):
        state = mdp['initial_state']
        total_cost = 0

        for t in range(max_steps):
            action = policy_fn(state)
            cost = mdp['costs'][state][action]
            total_cost += cost

            if state in mdp['terminal_states']:
                break

            state = sample_next_state(state, action, mdp['transitions'])

        results.append({
            'run': run,
            'final_state': state,
            'total_cost': total_cost
        })
    return results

# Run all policies
summary_rows = []
for i, item in enumerate(policy_list):
    policy = item["policy"]
    total_intervention_cost = item["total_intervention_cost"]

    policy_fn = lambda s, p=policy: get_action_from_policy(s, p)
    sim_results = run_simulation(mdp, policy_fn)

    out_file = os.path.join(RESULTS_DIR, f"policy_{i:02d}.json")
    log_run_result(sim_results, output_path=out_file)

    avg_cost = sum(r['total_cost'] for r in sim_results) / NUM_RUNS
    summary_rows.append({
        "policy_id": i,
        "avg_total_cost": avg_cost,
        "intervention_cost": total_intervention_cost,
        "policy": policy
    })

# Save metadata as JSON
metadata_path = os.path.join(RESULTS_DIR, "policy_metadata.json")
with open(metadata_path, "w") as f:
    json.dump([
        {
            "policy_id": row["policy_id"],
            "intervene_states": [k for k, v in row["policy"].items() if v == "intervene"],
            "avg_total_cost": row["avg_total_cost"],
            "intervention_cost": row["intervention_cost"]
        }
        for row in summary_rows
    ], f, indent=2)

print(f"✅ Metadata saved to {metadata_path}")


# Save summary CSV
import pandas as pd
df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv(os.path.join(RESULTS_DIR, "summary.csv"), index=False)

print(f"✅ Completed {len(policy_list)} policies. Results saved to {RESULTS_DIR}")
