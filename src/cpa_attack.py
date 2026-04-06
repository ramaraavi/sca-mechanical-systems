import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *
from aes_hw_model import sbox_out, hamming_weight

def _hw_pred(pt_byte, k):
    return hamming_weight(sbox_out(pt_byte, k))

def cpa_byte(load_id, sigma, byte_idx):
    tag        = f"L{load_id}_s{str(sigma).replace('.','')}"
    traces     = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))
    plaintexts = np.load(os.path.join(TRACES_DIR, f"plaintexts_{tag}.npy"))
    N, T       = traces.shape

    H = np.array([[_hw_pred(int(plaintexts[i, byte_idx]), k) for k in range(256)]
                  for i in range(N)], dtype=np.float32)  # (N, 256)

    H_c = H - H.mean(0)          # (N, 256)
    T_c = traces - traces.mean(0) # (N, T)

    num   = H_c.T @ T_c           # (256, T)
    dH    = np.sqrt((H_c**2).sum(0))          # (256,)
    dT    = np.sqrt((T_c**2).sum(0))          # (T,)
    denom = np.outer(dH, dT) + 1e-10          # (256, T)
    corr  = num / denom

    peaks     = np.max(np.abs(corr), axis=1)
    recovered = int(np.argmax(peaks))
    true_byte = AES_KEY[byte_idx]
    ok        = recovered == true_byte
    rho       = float(peaks[true_byte])
    print(f"  Byte {byte_idx:2d}: 0x{recovered:02X}  "
          f"true=0x{true_byte:02X}  rho={rho:.3f}  {'OK' if ok else 'FAIL'}")
    return recovered, ok, rho

def cpa_full_key(load_id=0, sigma=0.05):
    print(f"\n=== CPA Full Key Recovery  L{load_id}  sigma={sigma} ===")
    correct, rhos = 0, []
    for b in range(16):
        _, ok, rho = cpa_byte(load_id, sigma, b)
        if ok: correct += 1
        rhos.append(rho)
    mean_rho = float(np.mean(rhos))
    print(f"Correct: {correct}/16   Mean rho: {mean_rho:.3f}")
    return correct, mean_rho

if __name__ == "__main__":
    cpa_full_key(0, 0.05)
    cpa_full_key(0, 0.15)
    cpa_full_key(2, 0.05)
    cpa_full_key(2, 0.15)
