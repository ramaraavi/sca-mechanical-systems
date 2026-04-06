import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *
from aes_hw_model import sbox_out, hamming_weight

rng = np.random.default_rng(seed=0)

def timing_jitter(traces, max_jitter=5):
    out = np.zeros_like(traces)
    for i in range(len(traces)):
        out[i] = np.roll(traces[i], int(rng.integers(0, max_jitter+1)))
    return out

def noise_injection(traces, extra_sigma=0.16):
    return traces + rng.normal(0, extra_sigma, traces.shape).astype(np.float32)

def boolean_masking(traces, plaintexts):
    masked = traces.copy()
    for i in range(len(traces)):
        mask = rng.integers(0, 256, 16, dtype=np.uint8)
        for r in range(10):
            for b in range(16):
                idx = r*50 + b*3
                if idx < traces.shape[1]:
                    raw_hw    = hamming_weight(sbox_out(int(plaintexts[i,b]),
                                                        int(AES_KEY[b])))
                    masked_hw = hamming_weight(raw_hw ^ int(mask[b]))
                    masked[i, idx] += ALPHA * (masked_hw - raw_hw)
    return masked

def peak_rho(traces, plaintexts, byte_idx=0):
    from cpa_attack import _hw_pred
    N, T  = traces.shape
    true_k = AES_KEY[byte_idx]
    H  = np.array([_hw_pred(int(plaintexts[i, byte_idx]), true_k)
                   for i in range(N)], dtype=np.float32)
    Hc = H - H.mean()
    Tc = traces - traces.mean(0)
    num  = Hc @ Tc
    den  = np.sqrt((Hc**2).sum()) * np.sqrt((Tc**2).sum(0)) + 1e-10
    return float(np.max(np.abs(num / den)))

def compare_countermeasures(load_id=0, sigma=0.05):
    tag        = f"L{load_id}_s{str(sigma).replace('.','')}"
    traces     = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))
    plaintexts = np.load(os.path.join(TRACES_DIR, f"plaintexts_{tag}.npy"))

    configs = {
        "Baseline"       : traces,
        "Jitter"         : timing_jitter(traces),
        "Noise inject"   : noise_injection(traces),
        "Bool masking"   : boolean_masking(traces, plaintexts),
        "Masking+Jitter" : timing_jitter(boolean_masking(traces, plaintexts)),
    }

    print(f"\n=== Countermeasure Comparison  L{load_id}  sigma={sigma} ===")
    rhos = {}
    for name, t in configs.items():
        r = peak_rho(t, plaintexts)
        rhos[name] = r
        print(f"  {name:20s}  rho = {r:.3f}")

    fig, ax = plt.subplots(figsize=(8, 4))
    cols  = ['#E24B4A','#EF9F27','#EF9F27','#1D9E75','#0F6E56']
    bars  = ax.bar(list(rhos.keys()), list(rhos.values()),
                   color=cols, edgecolor='none', width=0.55)
    ax.axhline(0.2, color='black', ls='--', lw=1.0, label='Practical threshold')
    ax.set_ylabel('Peak Pearson correlation (rho)')
    ax.set_ylim(0, 1.05)
    ax.set_title(f'Countermeasure effectiveness  L{load_id}  sigma={sigma}')
    ax.legend()
    for bar, v in zip(bars, rhos.values()):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.02,
                f'{v:.2f}', ha='center', fontsize=10)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, f"countermeasures_L{load_id}.png")
    plt.savefig(out, dpi=150); plt.show()
    return rhos

if __name__ == "__main__":
    compare_countermeasures(0, 0.05)
