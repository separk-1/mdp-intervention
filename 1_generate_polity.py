import json
from itertools import product
from pathlib import Path

# === Configuration ===
MDP_PATH = "data/tmi_mdp.json"
OUTPUT_PATH = "data/policy_list.json"
MAX_TOTAL_INTERVENTION_COST = 1.5
TERMINAL_STATE = "S5"  # absorbing state

# === Load MDP ===
with open(MDP_PATH, "r") as f:
    mdp = json.load(f)

states = [s for s in mdp["states"] if s != TERMINAL_STATE]
intervention_costs = {
    state: mdp["costs"][state]["intervene"]
    for state in states
}

# === Generate All Policy Combinations ===
valid_policies = []
for actions in product(["no_intervention", "intervene"], repeat=len(states)):
    policy = {state: act for state, act in zip(states, actions)}
    policy[TERMINAL_STATE] = "no_intervention"  # always no intervention on terminal

    total_cost = sum(
        intervention_costs[state] if act == "intervene" else 0.0
        for state, act in policy.items() if state in intervention_costs
    )

    if total_cost <= MAX_TOTAL_INTERVENTION_COST:
        valid_policies.append({
            "policy": policy,
            "total_intervention_cost": total_cost
        })

# === Save Result ===
Path("data").mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(valid_policies, f, indent=2)

print(f"✅ Saved {len(valid_policies)} policies to {OUTPUT_PATH}")
