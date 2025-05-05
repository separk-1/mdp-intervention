# Simulation configuration
NUM_RUNS = 10000
MAX_STEPS = 10

# Example policy: intervene only at S3 and S5
POLICY = {
    "S1": "no_intervention",
    "S2": "no_intervention",
    "S3": "intervene",
    "S4": "no_intervention",
    "S5": "intervene",
    "S6": "no_intervention"  # terminal state
}
