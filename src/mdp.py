import json

def load_mdp(json_path):
    with open(json_path, 'r') as f:
        mdp = json.load(f)
    return mdp
