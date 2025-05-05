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

## 🤔 Policy Configuration (src/config.py)
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
| S0 | Valve A left open, operator assumes it's closed |
| S1 | Reactor auto-trip |
| S2 | Ambiguous signals emerge; Valve B misread as closed |
| S3 | Cooling water leaking, but operator believes excess water exists |
| S4 | Auto-injection disabled; pump starts vibrating due to low level |
| S5 | Full cooling failure → core damage (terminal) |

### 🔄 Transition Probabilities
Transitions represent how likely an operator is to move to the next misinterpretation without or with intervention.

| From | To | P (no_intervention) | P (intervene) | Notes |
|------|----|----------------------|---------------|-------|
| S0 | S1 | 0.8 | 0.3 | Operator misses initial abnormal state (Valve A open) |
| S1 | S2 | 0.9 | 0.4 | Auto-trip causes signal overload; intervention helps reassess |
| S2 | S3 | 0.95 | 0.5 | Valve B status misjudged unless checked |
| S3 | S4 | 0.9 | 0.4 | Water level misunderstood; corrective cues missed |
| S4 | S5 | 1.0 | 0.8 | Final critical error before meltdown |
| S5 | S5 | 1.0 | 1.0 | Absorbing terminal state (core damage) |

### 💸 Cost Structure
Each state-action pair has an immediate cost, approximating severity of misinterpretation and cost of intervention. These costs act as a proxy for system risk—higher costs imply greater hazard if misjudgment continues unchecked.

| State | Cost (no_intervention) | Cost (intervene) | Rationale |
|-------|-------------------------|------------------|-----------|
| S0 | 0.0 | 0.2 | Initial belief error; minimal consequence if caught early |
| S1 | 0.0 | 0.2 | Auto-trip stage; information overload begins, still easy to intervene |
| S2 | 1.0 | 0.3 | Early misjudgment of cooling issue; intervention begins to matter |
| S3 | 2.0 | 0.5 | Dangerous phase: operator assumes overfill despite leak |
| S4 | 5.0 | 1.0 | Critical signals emerge (pump vibration); late intervention is costly but useful |
| S5 | 20.0 | 15.0 | Core damage or meltdown; huge risk even if intervention is attempted |

> 🔍 **Note on Intervention Costs:**
> 
> Intervention costs increase in later states not only due to higher system risk, but also due to practical challenges in executing corrective actions under crisis:
> - ⚙️ **Complexity**: Later interventions require more invasive and multi-step actions.
> - ⏱️ **Time Pressure**: Decisions must be made rapidly under stress, increasing the cost of coordination.
> - 💡 **Delayed Response Burden**: Reversing damage is harder and more expensive once system degradation has progressed.
> 
> This reflects real-world emergency operations, where early correction is cheaper, but delayed action—even when successful—comes with significant overhead.

---

Contact: seongeunpark@cmu.edu
