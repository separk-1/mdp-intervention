# MDP-INTERVENTION: TMI-Inspired Decision Flow Simulation

This repository simulates how judgment errors propagate in a high-risk system, using the Three Mile Island (TMI) accident as a case study. It models human decision-making as a Markov Decision Process (MDP), simulates intervention strategies, and quantifies their risk reduction using Value of Information (VoI).

---

## 📁 Project Structure

```
MDP-INTERVENTION/
├── data/                        # MDP model and intervention policy data
├── results/                     # Simulation outputs and analysis results
├── src/                         # Core simulation code
├── 1_generate_policies.py       # Policy generator
├── 2_simulate_all.py            # Batch simulator
├── 3_add_voi_to_metadata.py     # Annotates VoI
├── 4_analysis_all.py            # Visualization and metrics
├── figures/                     # Saved output plots
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate all intervention policies
```bash
python 1_generate_policies.py
```

### 3. Simulate all policies
```bash
python 2_simulate_all.py
```

### 4. Add VoI calculations
```bash
python 3_add_voi_to_metadata.py
```

### 5. Analyze and visualize results
```bash
python 4_analysis_all.py
```

---

## 🧠 Model Assumptions

- Judgment flow is predefined based on accident reports and domain expertise.
- Cognitive propagation: earlier misjudgments can influence later decisions.
- The system is fully observable (as in a standard MDP).

> ⚠️ Future work will shift to POMDPs for modeling belief uncertainty and perceptual ambiguity.

---

## ⚙️ MDP Model Summary

Each decision point is a state. An intervention can be applied or skipped.

### MDP Elements:
- **States**: S₀ to S₅ (representing operator judgments)
- **Actions**: {`no_intervention`, `intervene`}
- **Transitions**: probabilistic, conditioned on action
- **Cost**: based on both intervention burden and system consequence
- **Policy**: A mapping of each state to an action

---

## 🔄 Transition & Cost Table

| State | Description | Intervene | Cost | P(Fail) | P(Success) | P(Stag.) |
|-------|-------------|-----------|------|---------|------------|----------|
| S0 | Valve A open; operator thinks closed | No | 0.0 | 0.63 | 0.27 | 0.10 |
|     |                                               | Yes | 0.1 | 0.09 | 0.81 | 0.10 |
| S1 | Reactor auto-trip                              | No | 0.0 | 0.70 | 0.20 | 0.10 |
|     |                                               | Yes | 0.5 | 0.20 | 0.70 | 0.10 |
| S2 | Valve B misjudged as closed                    | No | 1.0 | 0.765 | 0.135 | 0.10 |
|     |                                               | Yes | 0.2 | 0.675 | 0.225 | 0.10 |
| S3 | Coolant leak misunderstood                     | No | 2.0 | 0.81 | 0.09 | 0.10 |
|     |                                               | Yes | 1.0 | 0.45 | 0.45 | 0.10 |
| S4 | Pump vibration misjudged, disabled             | No | 5.0 | 0.85 | 0.05 | 0.10 |
|     |                                               | Yes | 0.5 | 0.90 | 0.50 | 0.10 |
| S5 | Cooling fails; core damage (terminal)          | No | 20.0 | 0.95 | 0.70 | 0.10 |
|     |                                               | Yes | 15.0 | 1.00 | 0.00 | 0.00 |

> Non-intervention has zero immediate cost, but hidden future risks.

---

## 📈 Simulation Methodology

- 64 policies ($2^6$) simulated using Monte Carlo (10,000 runs each)
- VoI = Risk reduction relative to baseline policy (no intervention)
- VoI per Cost = VoI normalized by total intervention cost
- Policies with cost ≤ 1.5 are prioritized for realism

---

## 🔍 Key Findings

- Best risk reduction (77%) achieved by Policy #21 (moderate cost)
- Highest efficiency by Policy #12 (VoI/Cost = 156.5) with only S0 intervention
- Targeted early-stage interventions (S0--S2) are most effective

---

## 📊 Visualizations

- **Risk vs Cost scatter**: darker = lower risk
- **VoI heatmap**: highlights high-value intervention states
- **Efficiency Pareto plot**: identifies cost-effective policies

All saved to `/figures/` upon running `4_analysis_all.py`.

---

## 🚧 Limitations & Future Work

- MDP assumes known operator state; VoI here reflects value of correction.
- In reality, operators work under uncertainty.
- Upcoming extension: **POMDP formulation** to model hidden states and belief dynamics.
- VoI will then represent the benefit of resolving uncertainty, not just fixing known misjudgments.

---

## 📬 Contact

**Seongeun Park**  
📧 seongeup@andrew.cmu.edu  
🔗 [GitHub Repository](https://github.com/separk-1/mdp-intervention)