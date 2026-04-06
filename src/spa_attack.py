import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *

def run_spa(load_id=0, sigma=0.05, n_avg=20):
    tag    = f"L{load_id}_s{str(sigma).replace('.','')}"
    traces = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))

    single    = traces[0]
    avg_trace = traces[:n_avg].mean(axis=0)

    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    axes[0].plot(single, color='#185FA5', lw=0.7, alpha=0.8)
    axes[0].set_title(f'Single trace  |  {LOAD_LABELS[load_id]}, sigma={sigma}')
    axes[0].set_ylabel('Power (norm.)')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(avg_trace, color='#A32D2D', lw=1.0)
    for r in range(10):
        axes[1].axvline(r * 50, color='orange', ls='--', lw=0.7, alpha=0.6)
    axes[1].text(4, avg_trace.max() * 0.92, 'AES round boundaries',
                 fontsize=8, color='darkorange')
    axes[1].set_title(f'Average of {n_avg} traces  —  round structure visible')
    axes[1].set_ylabel('Power (norm.)')
    axes[1].set_xlabel('Sample index  (10 MHz)')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, f"spa_{tag}.png")
    plt.savefig(out, dpi=150)
    plt.show()
    print(f"SPA plot saved -> {out}")

if __name__ == "__main__":
    run_spa(0, 0.05)
