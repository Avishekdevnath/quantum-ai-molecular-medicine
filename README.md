# Quantum Artificial Intelligence in Molecular Medicine

Benchmark datasets and analysis scripts for:
> **Quantum Artificial Intelligence in Molecular Medicine: End-to-End Foundations, Empirical Benchmarks, and Fault-Tolerant Horizons**  
> *Nature Computational Science* (Review Article)  
> **Authors:** Prof. Dr. Hafiz Mohammad Hasan Babu & Avishek Devnath  
> Department of Computer Science and Engineering, University of Dhaka, Dhaka 1000, Bangladesh

---

## Overview

This repository provides reproducible computational analysis scripts and empirical benchmark datasets supporting the systematic review on quantum artificial intelligence (QAI) in molecular medicine.

### Directory Structure

```
.
├── data/
│   ├── master_prisma_n71_benchmarks.csv           # Master PRISMA-2020 dataset (n=71 studies)
│   ├── figure3_noise_and_zne.csv                  # Physical QPU unitary folding noise measurements
│   ├── table_s1_empirical_chemistry_benchmarks.csv# Ground/excited state electronic structure data
│   ├── table_s2_qml_docking_benchmarks.csv        # QML, docking, and multi-omics benchmarks
│   ├── table_s3_surface_code_scaling.csv          # Surface code distance and threshold scaling
│   ├── table_s4_ftqc_molecular_targets.csv        # Fault-tolerant resource budgets for complex active spaces
│   └── table_s5_technology_roadmap.csv           # 10-year hardware milestone projections
├── 1_prisma_meta_analysis.py                      # PRISMA statistical meta-analysis
├── 2_noise_and_zne_solver.py                      # Zero-noise extrapolation & barren plateau scaling
├── 3_ftqc_resource_estimator.py                   # Surface code physical resource estimator
├── run_all_analyses.py                            # Pipeline runner
├── requirements.txt                               # Minimal Python dependencies
└── LICENSE                                        # MIT License
```

---

## Installation & Requirements

- Python $\ge$ 3.8
- `numpy`
- `scipy`

Install dependencies via:

```bash
pip install -r requirements.txt
```

---

## Reproducing the Analysis

To execute all modules sequentially:

```bash
python run_all_analyses.py
```

Or execute individual analysis modules:

```bash
# 1. PRISMA 2020 Systematic Review Meta-Analysis
python 1_prisma_meta_analysis.py

# 2. Zero-Noise Extrapolation (ZNE) and Barren Plateau Scaling
python 2_noise_and_zne_solver.py

# 3. Fault-Tolerant Surface Code Resource Estimator
python 3_ftqc_resource_estimator.py
```

---

## Data Description

- **`master_prisma_n71_benchmarks.csv`**: Contains 71 curated empirical investigations evaluated across 18 operational dimensions (algorithmic pillar, target molecule, active space, execution platform, accuracy, and wall-clock latencies).
- **`figure3_noise_and_zne.csv`**: Unitary gate folding noise data ($\lambda \in [1, 5]$) measured on IBM Heron for the LiH ground state along with Full CI benchmarks.
- **`table_s4_ftqc_molecular_targets.csv`**: Fault-tolerant resource requirements (logical qubits, T-gate counts, code distances, physical qubits, and runtime) for FeMoco, Cytochrome P450, Penicillin, and Caffeine.

---

## License

Code is licensed under the [MIT License](LICENSE).  
Datasets are licensed under the Creative Commons Attribution 4.0 International License ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
