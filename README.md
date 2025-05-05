# MDP-INTERVENTION: TMI-Inspired Decision Flow Simulation

This repository simulates how decision errors propagate in a high-risk system like a nuclear power plant, using the Three Mile Island (TMI) accident as a case study. It models the flow of human judgment as a Markov Decision Process (MDP) and quantifies the effect of interventions on system risk using Monte Carlo simulations.

---

## 🔧 Project Structure
```
MDP-INTERVENTION/
├── data/                  # MDP model JSON and generated policy list
│   ├── tmi_mdp.json       # MDP states, transitions, costs
│   └── policy_list.json   # All policies and intervention costs
├── results/               # Output of simulation runs
│   ├── policy_XX.json     # Result of individual policy simulations
│   ├── summary.csv        # Summary table with total cost and VoI
│   ├── top5_policies.csv      # Cost-optimal policies
│   ├── top_voi_per_cost.csv  # VoI-efficiency optimal policies
│   └── summary_with_voi.csv  # Full policy summary with VoI fields
├── src/                   # Core simulation source code
│   ├── mdp.py             # MDP loader
│   ├── utils.py           # Helpers for transition, policy, logging
│   ├── config.py          # General constants (e.g. run count)
│   └── generate_policies.py # Exhaustive policy generator by cost
├── 1_generate_policies.py    # Run this to create full policy set
├── 2_simulate_all.py         # Run this to simulate every policy
├── 3_add_voi_to_metadata.py  # Annotate metadata with VoI
├── 4_analysis_all.py         # Analyze policies and visualize results
├── figures/                  # Saved plots (auto-generated)
├── requirements.txt          # Python package requirements
└── README.md
```

---

## ▶️ How to Run
### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate policies
```bash
python 1_generate_policies.py
```
- Produces `data/policy_list.json` with all possible intervention policies and their costs.

### 3. Run simulations on all policies
```bash
python 2_simulate_all.py
```
- Saves each result to `results/policy_XX.json`
- Also saves summary statistics to `results/summary.csv`

### 4. Add VoI to metadata
```bash
python 3_add_voi_to_metadata.py
```
- Calculates Value of Information (VoI) for each policy
- Updates the metadata with VoI, VoI per cost, and intervention states

### 5. Analyze results (VoI, Pareto, Heatmap)
```bash
python 4_analysis_all.py
```
- Generates plots and saves them to `figures/`
- Includes:
  - 📈 Total cost vs intervention cost
  - 🔥 VoI heatmap by state
  - 💠 Pareto front for VoI/cost tradeoff

---

## 🎯 Objective
This framework helps answer:
- Which operator states are most impactful to intervene?
- How does total cost vary across intervention strategies?
- What is the Value of Information (VoI) for each intervention?
- What are cost-effective and risk-effective intervention policies?

It is designed for nuclear safety studies, accident response simulation, and human reliability modeling.

---

## ⚙️ MDP Model Design

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
Transitions reflect how likely the operator is to progress to the next state (i.e., next misjudgment) depending on whether intervention occurred.

| From | To | P (no_intervention) | P (intervene) | Notes |
|------|----|----------------------|---------------|-------|
| S0 | S1 | 0.8 | 0.1 | Operator misses initial abnormal state (Valve A open) |
| S1 | S2 | 0.9 | 0.3 | Auto-trip causes signal overload; intervention helps reassess |
| S2 | S3 | 0.95 | 0.8 | Valve B stuck open physically; intervention has limited effect |
| S3 | S4 | 0.9 | 0.5 | Water level misunderstood due to poor training; harder to fix |
| S4 | S5 | 1.0 | 0.6 | Final critical error before meltdown; fast action can help |
| S5 | S5 | 1.0 | 1.0 | Absorbing terminal state (core damage) |

### 💸 Cost Structure
Each state-action pair has a cost. Higher cost = higher system risk or difficulty of intervention.

| State | Cost (no_intervention) | Cost (intervene) | Rationale |
|-------|-------------------------|------------------|-----------|
| S0 | 0.0 | 0.1 | Early misjudgment; easy to correct |
| S1 | 0.0 | 0.5 | Requires more resources to verify and interpret signals |
| S2 | 1.0 | 0.2 | Re-checking valve B is low-cost, but impact is limited |
| S3 | 2.0 | 1.0 | Training mismatch; intervention is expensive but important |
| S4 | 5.0 | 0.5 | Pump vibration is urgent; intervention is effective and cheap |
| S5 | 20.0 | 15.0 | Catastrophic failure; intervention is possible but costly |

> 📌 **Note**: Total cost = (intervention cost) + (simulated consequence cost)

> 🔍 **Why later interventions cost more?**
> - 🔁 Later states represent crisis moments where mistakes compound
> - ⚙️ Actions require more time, coordination, or system override
> - 🧠 Human factors like stress and ambiguity make decision harder
> - ⏱️ Correcting deep errors comes with a higher price tag

---

## 📈 Analysis Output
Running `4_analysis_all.py` provides:
- 🔹 **Cost-efficiency ranking**: which policies reduce risk with least intervention
- 🔸 **VoI per state**: visualized as a heatmap
- 💠 **Pareto frontier**: visualize tradeoff between cost and VoI
- 📊 **Policy-wise intervention breakdown**: where each policy intervenes

> 📁 Output saved to `figures/`
> 📄 Top policies saved to CSVs: `summary_with_voi.csv`, `top5_policies.csv`, `top_voi_per_cost.csv`

---

Contact: seongeunpark@cmu.edu