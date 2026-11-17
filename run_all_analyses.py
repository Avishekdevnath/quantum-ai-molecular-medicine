#!/usr/bin/env python3
"""
Pipeline runner for computational analysis and benchmarks.

Executes:
1. PRISMA meta-analysis (1_prisma_meta_analysis.py)
2. Zero-noise extrapolation and barren plateau evaluation (2_noise_and_zne_solver.py)
3. Surface-code resource estimator (3_ftqc_resource_estimator.py)
"""

import sys
import os
import subprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    scripts = [
        ("PRISMA Meta-Analysis", "1_prisma_meta_analysis.py"),
        ("ZNE and Barren Plateau Scaling", "2_noise_and_zne_solver.py"),
        ("FTQC Resource Estimation", "3_ftqc_resource_estimator.py")
    ]

    print("Running analysis modules...\n")
    for name, filename in scripts:
        print(f"=== {name} ({filename}) ===")
        ret = subprocess.run([sys.executable, filename])
        if ret.returncode != 0:
            print(f"Error in {filename}")
            sys.exit(ret.returncode)
        print()

    print("All modules completed successfully.")

if __name__ == "__main__":
    main()
