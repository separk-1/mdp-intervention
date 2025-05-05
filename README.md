# MDP-INTERVENTION: TMI-Inspired Decision Flow Simulation

This repository simulates how decision errors propagate in a high-risk system like a nuclear power plant, using the Three Mile Island (TMI) accident as a case study. It models the flow of human judgment as a Markov Decision Process (MDP) and quantifies the effect of interventions on system risk using Monte Carlo simulations.

---

## 🔧 Project Structure
```
MDP-INTERVENTION/
├── data/               # MDP model JSON files
│   └── tmi_mdp.json
├── results/            # Output of simulation runs
│   └── run1_result.json
├── src/                # Core simulation source code
│   ├── mdp.py          # MDP loader
│   ├── utils.py        # Helpers for transition, policy, logging
│   └── config.py       # Simulation configs and policies
├── figures/            # Saved plots from analysis (auto-generated)
├──  simulate.py        # Main simulation runner
├── analysis.py         # Visualization and post-analysis script
├── requirements.txt    # Python package requirements
└── README.md
```

---

## ▶️ How to Run
### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run simulation
```bash
python src/simulate.py
```
- Outputs will be saved to `results/run1_result.json`

### 3. Analyze results (generate plots)
```bash
python analysis.py
```
- Images will be saved in the `figures/` directory

---

## 🧠 Policy Configuration (src/config.py)
You can modify the `POLICY` dictionary to control which states trigger interventions.

Example:
```python
POLICY = {
    "S1": "no_intervention",
    "S2": "no_intervention",
    "S3": "intervene",
    "S4": "no_intervention",
    "S5": "intervene",
    "S6": "no_intervention"  # terminal state
}
```

---

## 📊 Purpose and Use Cases
This simulation framework supports:
- Modeling error propagation in decision sequences
- Evaluating the impact of interventions
- Quantifying Value of Information (VoI) for risk mitigation

It is suitable for applications in nuclear safety analysis, accident investigation, and human-reliability modeling.

---

Contact: seongeunpark@cmu.edu
