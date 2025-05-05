import numpy as np
import json
from src.mdp import load_mdp
from src.utils import sample_next_state, get_action_from_policy, log_run_result
from src.config import NUM_RUNS, MAX_STEPS, POLICY


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


if __name__ == "__main__":
    mdp = load_mdp("data/tmi_mdp.json")
    policy_fn = lambda s: get_action_from_policy(s, POLICY)

    sim_results = run_simulation(mdp, policy_fn)
    log_run_result(sim_results, output_path="results/run1_result.json")
    print(f"Completed {NUM_RUNS} simulations. Results saved to results/run1_result.json")
