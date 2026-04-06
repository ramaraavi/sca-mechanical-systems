import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *
from aes_hw_model import sbox_out

def _sel(pt_byte, k):
    return (sbox_out(pt_byte, k) >> 7) & 1

def dpa_byte(load_id, sigma, byte_idx):
    tag        = f"L{load_id}_s{str(sigma).replace('.','')}"
    traces     = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))
    plaintexts = np.load(os.path.join(TRACES_DIR, f"plaintexts_{tag}.npy"))
    N, T       = traces.shape
    diffs      = np.zeros((256, T), dtype=np.float32)

    for k in range(256):
        bits   = np.array([_sel(int(plaintexts[i, byte_idx]), k) for i in range(N)])
        g1, g0 = traces[bits == 1], traces[bits == 0]
        if len(g1) and len(g0):
            diffs[k] = g1.mean(0) - g0.mean(0)

    peaks     = np.max(np.abs(diffs), axis=1)
    recovered = int(np.argmax(peaks))
    true_byte = AES_KEY[byte_idx]
    ok        = recovered == true_byte
    print(f"  Byte {byte_idx:2d}: recovered=0x{recovered:02X}  "
          f"true=0x{true_byte:02X}  {'CORRECT' if ok else 'WRONG'}")
    return recovered, ok, diffs

def recover_full_key(load_id=0, sigma=0.05, plot_byte=0):
    print(f"\n=== DPA Full Key Recovery  L{load_id}  sigma={sigma} ===")
    recovered, correct = [], 0
    diffs_plot = None
    for b in range(16):
        kb, ok, diffs = dpa_byte(load_id, sigma, b)
        recovered.append(kb)
        if ok: correct += 1
        if b == plot_byte: diffs_plot = diffs

    print(f"Correct: {correct}/16")
    print(f"Recovered : {''.join(f'{b:02x}' for b in recovered)}")
    print(f"True key  : {AES_KEY.hex()}")

    if diffs_plot is not None:
        fig, ax = plt.subplots(figsize=(12, 4))
        for k in range(256):
            col = '#E24B4A' if k == AES_KEY[plot_byte] else '#CCCCCC'
            lw  = 1.5 if k == AES_KEY[plot_byte] else 0.3
            ax.plot(diffs_plot[k], color=col, lw=lw,
                    alpha=1.0 if k == AES_KEY[plot_byte] else 0.4)
        ax.set_title(f'DPA correlation surface  |  byte {plot_byte}'
                     f'  L{load_id} sigma={sigma}  (red = correct key)')
        ax.set_xlabel('Sample index')
        ax.set_ylabel('Difference of means')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        out = os.path.join(PLOTS_DIR, f"dpa_L{load_id}_b{plot_byte}.png")
        plt.savefig(out, dpi=150)
        plt.show()
    return correct

if __name__ == "__main__":
    recover_full_key(0, 0.05)
    recover_full_key(2, 0.15)
