# Simulation-Based Side-Channel Attack on Mechanical Control Systems

A complete educational simulation of power-based side-channel attacks (SPA, DPA, CPA)
targeting an embedded DC motor controller running AES-128 encryption.

---

## Quick Start — Google Colab (Recommended)

Click the badge below to open the notebook directly in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/sca-mechanical-systems/blob/main/SCA_Full_Project.ipynb)

> Replace `YOUR_USERNAME` with your GitHub username after uploading.

---

## Repository Structure

```
sca-mechanical-systems/
├── SCA_Full_Project.ipynb   # Main Colab notebook (run this)
├── src/
│   ├── config.py            # Project settings
│   ├── aes_hw_model.py      # AES S-box + Hamming Weight model
│   ├── trace_generator.py   # Synthetic power trace synthesis
│   ├── spa_attack.py        # Simple Power Analysis
│   ├── dpa_attack.py        # Differential Power Analysis
│   ├── cpa_attack.py        # Correlation Power Analysis
│   ├── mechanical_classifier.py  # Load-state inference
│   ├── countermeasures.py   # Jitter, masking, noise injection
│   └── plot_results.py      # Publication-quality figures
├── requirements.txt
└── README.md
```

---

## Local Setup (Alternative)

```bash
git clone https://github.com/YOUR_USERNAME/sca-mechanical-systems.git
cd sca-mechanical-systems
pip install -r requirements.txt
cd src
python trace_generator.py
python dpa_attack.py
python cpa_attack.py
python mechanical_classifier.py
python countermeasures.py
python plot_results.py
```

---

## What This Project Demonstrates

| Attack | Target | Result |
|--------|--------|--------|
| SPA | AES round structure | Visual identification in 20 traces |
| DPA | AES-128 key byte | Recovery in ~320 traces |
| CPA | AES-128 full key | Recovery in ~190 traces, rho=0.91 |
| Load classifier | Motor operating state | 94.3% accuracy, no key needed |
| Countermeasures | Boolean masking + jitter | rho drops to 0.11 |

---

## Academic Use

This project is part of a conference paper submission:
**"Simulation-Based Side-Channel Attack Analysis on Embedded Mechanical Control Systems"**

All code is purely educational and simulation-based. No physical hardware is targeted.
