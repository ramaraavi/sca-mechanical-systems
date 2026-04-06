import numpy as np
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *
from aes_hw_model import hw_array, sbox_out, hamming_weight

rng = np.random.default_rng(seed=42)

def _synthetic_ia(load_id: int, n_samples: int = 500) -> np.ndarray:
    """Synthetic armature current when MATLAB output is unavailable."""
    t = np.linspace(0, 0.005, n_samples)
    base = [0.5, 1.2, 2.1][load_id]
    return (base + 0.08 * np.sin(2 * np.pi * 2000 * t)
                 + 0.03 * np.sin(2 * np.pi * 4000 * t)).astype(np.float32)

def generate_traces(load_id: int, sigma: float, n_traces: int = N_TRACES):
    ia_path = os.path.join(TRACES_DIR, f"ia_L{load_id}.csv")
    if os.path.exists(ia_path):
        import pandas as pd
        ia = pd.read_csv(ia_path, header=None).values.flatten().astype(np.float32)[:500]
    else:
        ia = _synthetic_ia(load_id)

    traces     = np.zeros((n_traces, 500), dtype=np.float32)
    plaintexts = rng.integers(0, 256, size=(n_traces, 16), dtype=np.uint8)
    key        = np.frombuffer(AES_KEY, dtype=np.uint8)

    for i in range(n_traces):
        pt   = plaintexts[i]
        D    = np.zeros(500, dtype=np.uint8)
        D_xp = np.zeros(500, dtype=np.uint8)
        for r in range(10):
            for b in range(16):
                idx = r * 50 + b * 3
                if idx < 500:
                    D[idx]    = sbox_out(int(pt[b]), int(key[b]))
                    D_xp[idx] = D[idx] ^ (D[idx - 1] if idx > 0 else 0)

        hw      = hw_array(D)
        hw_xor  = hw_array(D_xp)
        noise   = rng.normal(0, sigma, 500).astype(np.float32)
        traces[i] = ALPHA * hw + BETA * hw_xor + GAMMA * ia + noise

    tag    = f"L{load_id}_s{str(sigma).replace('.','')}"
    np.save(os.path.join(TRACES_DIR, f"traces_{tag}.npy"),     traces)
    np.save(os.path.join(TRACES_DIR, f"plaintexts_{tag}.npy"), plaintexts)
    print(f"  [OK] {n_traces} traces saved  (L{load_id}, sigma={sigma})")
    return traces, plaintexts

if __name__ == "__main__":
    print("Generating power traces...")
    for load in [0, 1, 2]:
        for sigma in NOISE_LEVELS:
            generate_traces(load, sigma)
    print("Done.")
