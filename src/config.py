import os

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
TRACES_DIR  = os.path.join(BASE_DIR, "..", "traces")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
PLOTS_DIR   = os.path.join(BASE_DIR, "..", "plots")

for d in [TRACES_DIR, RESULTS_DIR, PLOTS_DIR]:
    os.makedirs(d, exist_ok=True)

SAMPLE_RATE  = 10_000_000
N_TRACES     = 5000
AES_KEY      = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
NOISE_LEVELS = [0.05, 0.15]
LOAD_LABELS  = {0: "No load", 1: "50% load", 2: "Full load"}

ALPHA = 0.30
BETA  = 0.12
GAMMA = 0.08
