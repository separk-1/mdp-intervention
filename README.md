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

## 🧐 Policy Configuration (src/config.py)
You can modify the `POLICY` dictionary to control which states trigger interventions.

Example:
```python
POLICY = {
    "S0": "no_intervention",
    "S1": "no_intervention",
    "S2": "intervene",
    "S3": "no_intervention",
    "S4": "intervene",
    "S5": "no_intervention"  # terminal state
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

## ⚙️ Model Design Rationale
The MDP model (`data/tmi_mdp.json`) is inspired by the key decision stages observed in the 1979 Three Mile Island accident. Each state represents a point of operator judgment, and transitions reflect the likelihood of advancing (or repeating) based on the operator's understanding and whether intervention occurred.

### 🔁 States and Meanings
| State | Description |
|-------|-------------|
| S0 | 	Valve A left open, operator assumes it's closed |
| S1 | Reactor auto-trip; ambiguous signals emerge |
| S2 | Valve B is stuck open but misjudged as closed |
| S3 | Cooling water leaking, but operator believes excess water exists |
| S4 | Auto-injection disabled; pump starts vibrating due to low level |
| S5 | Full cooling failure → core damage (terminal) |

### 🔄 Transition Probabilities
Transitions represent how likely an operator is to move to the next misinterpretation without or with intervention.

| From | To | P (no_intervention) | P (intervene) | Notes |
|------|----|----------------------|---------------|-------|
| S0 | S1 | 0.8 | 0.3 | Without intervention, misjudgment persists (80%) |
| S1 | S2 | 0.9 | 0.4 | High forward progression without reassessment |
| S2 | S3 | 0.95 | 0.5 | Nearly always misinterpreted without help |
| S3 | S4 | 0.9 | 0.4 | Assumes system is overfilled, fails to reassess |
| S4 | S5 | 1.0 | 0.8 | If not stopped, full failure guaranteed |
| S5 | S5 | 1.0 | 1.0 | Absorbing terminal state |

### 💸 Cost Structure
Each state-action pair has an immediate cost, approximating severity of misinterpretation and cost of intervention.

| State | Cost (no_intervention) | Cost (intervene) | Rationale |
|-------|-------------------------|------------------|-----------|
| S0 | 0.0 | 0.2 | Very early, cheap to correct |
| S1 | 0.0 | 0.2 | Still relatively safe to intervene |
| S2 | 1.0 | 0.3 | Moderate cost to catch cooling loss early |
| S3 | 2.0 | 0.5 | Getting worse, water level dropping |
| S4 | 5.0 | 1.0 | Onset of critical state (vibration) |
| S5 | 20.0 | 15.0 | Fuel damage, severe penalty |

All values are scaled arbitrarily to reflect cost gradients and encourage early intervention while still penalizing late-stage misjudgment.

---

Contact: seongeunpark@cmu.edu
