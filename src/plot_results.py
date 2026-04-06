import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *

plt.rcParams.update({'font.size': 11, 'axes.linewidth': 0.8,
                     'grid.alpha': 0.3, 'figure.dpi': 150})

def fig1_trace_comparison():
    tag    = f"L0_s005"
    traces = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))
    fig, axes = plt.subplots(1, 2, figsize=(13, 3.5))

    axes[0].plot(traces[0], lw=0.6, color='#185FA5', alpha=0.8)
    axes[0].set_title('(a) Single power trace')
    axes[0].set_xlabel('Sample'); axes[0].set_ylabel('Power (norm.)')
    axes[0].grid(True)

    avg = traces[:20].mean(0)
    axes[1].plot(avg, lw=1.0, color='#A32D2D')
    for r in range(10):
        axes[1].axvline(r*50, color='orange', lw=0.7, ls='--', alpha=0.7)
    axes[1].set_title('(b) Average of 20 traces — AES round boundaries')
    axes[1].set_xlabel('Sample'); axes[1].grid(True)

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "fig1_traces.png")
    plt.savefig(out, dpi=150, bbox_inches='tight'); plt.show()
    print(f"Saved {out}")

def fig2_rho_bar():
    labels = ['L0\ns=0.05','L1\ns=0.05','L2\ns=0.05',
              'L0\ns=0.15','L1\ns=0.15','L2\ns=0.15']
    rho    = [0.91, 0.88, 0.85, 0.73, 0.70, 0.68]
    colors = ['#E24B4A']*3 + ['#EF9F27']*3

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(labels, rho, color=colors, width=0.55, edgecolor='none')
    ax.axhline(0.2, color='black', ls='--', lw=1, label='Attack threshold')
    ax.set_ylabel('Peak Pearson correlation (rho)')
    ax.set_ylim(0, 1.05); ax.legend()
    ax.set_title('CPA peak correlation — load and noise conditions')
    for b, v in zip(bars, rho):
        ax.text(b.get_x()+b.get_width()/2, v+0.02,
                f'{v}', ha='center', fontsize=9)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "fig2_rho_vs_load.png")
    plt.savefig(out, dpi=150, bbox_inches='tight'); plt.show()
    print(f"Saved {out}")

def fig3_countermeasures():
    labels = ['Baseline','Jitter','Noise\ninject','Bool\nmasking','Masking\n+Jitter']
    rho    = [0.91, 0.67, 0.54, 0.18, 0.11]
    colors = ['#E24B4A','#EF9F27','#EF9F27','#1D9E75','#0F6E56']

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(labels, rho, color=colors, width=0.55, edgecolor='none')
    ax.axhline(0.2, color='black', ls='--', lw=1, label='Practical threshold')
    ax.set_ylabel('Peak rho after countermeasure')
    ax.set_ylim(0, 1.05); ax.legend()
    ax.set_title('Countermeasure effectiveness (L0, sigma=0.05)')
    for b, v in zip(bars, rho):
        ax.text(b.get_x()+b.get_width()/2, v+0.02,
                f'{v}', ha='center', fontsize=10)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "fig3_countermeasures.png")
    plt.savefig(out, dpi=150, bbox_inches='tight'); plt.show()
    print(f"Saved {out}")

if __name__ == "__main__":
    fig1_trace_comparison()
    fig2_rho_bar()
    fig3_countermeasures()
    print("All figures done.")
