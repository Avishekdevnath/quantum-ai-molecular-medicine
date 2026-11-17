#!/usr/bin/env python3
"""
PRISMA-2020 systematic review meta-analysis.

Evaluates empirical distributions across n = 71 curated quantum computing 
investigations in molecular medicine:
- Taxonomy breakdown (VQA, QML, Docking, Open Dynamics)
- Physical hardware vs emulation platforms
- Chemical accuracy rates across molecular active spaces
- Latency scaling (QPU wall-clock vs classical CPU/GPU baselines)
"""

import os
import csv
import numpy as np

def load_master_dataset():
    """Load curated PRISMA database (n=71) from local data directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "data", "master_prisma_n71_benchmarks.csv"),
        os.path.join(script_dir, "..", "data", "master_prisma_n71_benchmarks.csv"),
        os.path.join(script_dir, "master_prisma_n71_benchmarks.csv"),
        os.path.abspath("data/master_prisma_n71_benchmarks.csv")
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader), path
    raise FileNotFoundError("Could not find master_prisma_n71_benchmarks.csv in data paths.")

def run_meta_analysis():
    records, data_path = load_master_dataset()
    n_total = len(records)
    print(f"Loaded {n_total} curated studies from: {data_path}\n")

    # 1. Algorithmic Pillar Breakdown
    pillar_counts = {}
    for r in records:
        p = r["Pillar"]
        pillar_counts[p] = pillar_counts.get(p, 0) + 1

    print("--- 1. Algorithmic Taxonomy Distribution ---")
    for pillar, count in sorted(pillar_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / n_total) * 100.0
        print(f"  {pillar:35s}: {count:2d} ({pct:5.1f}%)")

    # 2. Execution Mode (Physical QPU vs Classical Simulation)
    exec_counts = {}
    for r in records:
        mode = r["Execution_Mode"]
        exec_counts[mode] = exec_counts.get(mode, 0) + 1

    print("\n--- 2. Execution Mode Breakdown ---")
    for mode, count in exec_counts.items():
        pct = (count / n_total) * 100.0
        print(f"  {mode:35s}: {count:2d} ({pct:5.1f}%)")

    # 3. Hardware Modality
    hw_categories = {
        "Superconducting / Transmon": 0,
        "Trapped-Ion": 0,
        "Quantum Annealer": 0,
        "Classical Emulator": 0,
        "Neutral Atom / Other": 0
    }
    for r in records:
        hw = r["Hardware_Platform"]
        if any(k in hw for k in ["IBM", "Google", "Rigetti", "Transmon", "Superconducting"]):
            hw_categories["Superconducting / Transmon"] += 1
        elif any(k in hw for k in ["Quantinuum", "IonQ", "Trapped-Ion"]):
            hw_categories["Trapped-Ion"] += 1
        elif "D-Wave" in hw:
            hw_categories["Quantum Annealer"] += 1
        elif any(k in hw for k in ["Emulator", "Sim", "Aer", "Statevector"]):
            hw_categories["Classical Emulator"] += 1
        else:
            hw_categories["Neutral Atom / Other"] += 1

    print("\n--- 3. Hardware Modality Breakdown ---")
    for cat, count in hw_categories.items():
        pct = (count / n_total) * 100.0
        print(f"  {cat:35s}: {count:2d} ({pct:5.1f}%)")

    # 4. Chemical Accuracy Success Rate (Delta E <= 1.0 kcal/mol)
    vqa_records = [r for r in records if r["Pillar"] == "Variational Quantum Algorithms"]
    small_hydrides_phys = [r for r in vqa_records if r["Target_Class"] == "Small Hydride / Diatomic" and r["Execution_Mode"] == "Physical QPU"]
    small_acc = sum(1 for r in small_hydrides_phys if r["Chemical_Accuracy_Achieved"] == "Yes")
    small_total = len(small_hydrides_phys)

    complex_vqa = [r for r in vqa_records if r["Target_Class"] in ["Oligopeptide / Drug Fragment", "Metalloenzyme Core"]]
    complex_acc = sum(1 for r in complex_vqa if r["Chemical_Accuracy_Achieved"] == "Yes")
    complex_total = len(complex_vqa)

    print("\n--- 4. Chemical Accuracy Analysis (Delta E <= 1 kcal/mol) ---")
    print(f"  Small hydrides on physical QPUs    : {small_acc}/{small_total} ({small_acc/small_total*100.0:.1f}%)")
    print(f"  Drug fragments / Metalloenzymes    : {complex_acc}/{complex_total} ({complex_acc/complex_total*100.0:.1f}%)")

    # 5. Wall-Clock Latency Comparison (T_QPU / T_Classical)
    slowdown_ratios = [float(r["Slowdown_Ratio_QPU_to_Class"]) for r in records if r["Execution_Mode"] == "Physical QPU" and r["Pillar"] in ["Variational Quantum Algorithms", "Quantum Machine Learning"]]
    
    print("\n--- 5. Wall-Clock Latency Ratio (QPU / Classical) ---")
    print(f"  Benchmark comparisons (n)          : {len(slowdown_ratios)}")
    print(f"  Median slowdown                    : {np.median(slowdown_ratios):.1f}x")
    print(f"  Geometric mean                     : {np.exp(np.mean(np.log(slowdown_ratios))):.1f}x")
    print(f"  Min / Max range                    : {np.min(slowdown_ratios):.1f}x - {np.max(slowdown_ratios):.1f}x")

    # 6. Combinatorial Docking (Quantum Annealing vs Classical Solvers)
    anneal_records = [r for r in records if r["Pillar"] == "Combinatorial Docking" and "D-Wave" in r["Hardware_Platform"]]
    print("\n--- 6. Combinatorial Docking Benchmarks (D-Wave vs Classical) ---")
    for r in anneal_records[:4]:
        q_time = float(r['Quantum_WallClock_Seconds'])
        c_time = float(r['Classical_WallClock_Seconds'])
        print(f"  {r['Target_System']:30s} | QPU: {q_time:5.1f}s | Classical: {c_time:5.1f}s | Scores: Q={r['Quantum_Value']}, C={r['Classical_Value']}")

    return {
        "n_total": n_total,
        "pillar_counts": pillar_counts,
        "vqa_small_hydrides_acc_pct": small_acc / small_total * 100.0,
        "vqa_complex_acc_pct": complex_acc / complex_total * 100.0,
        "median_slowdown": float(np.median(slowdown_ratios))
    }

if __name__ == "__main__":
    run_meta_analysis()
