import json
import random

def sample_next_state(current_state, action, transition_dict):
    transitions = transition_dict[current_state][action]
    next_states = list(transitions.keys())
    probabilities = list(transitions.values())
    return random.choices(next_states, probabilities)[0]

def get_action_from_policy(state, policy):
    if state in policy:
        return policy[state]
    return "no_intervention"  # default fallback

def log_run_result(results, output_path):
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
