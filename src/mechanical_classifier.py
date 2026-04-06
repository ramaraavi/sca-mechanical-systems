import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from config import *
from scipy import stats
from sklearn.neighbors import NearestCentroid
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

def extract_features(traces):
    N = len(traces)
    feats = np.zeros((N, 20), dtype=np.float32)
    for i, tr in enumerate(traces):
        freqs = np.fft.rfftfreq(500, d=1/SAMPLE_RATE)
        psd   = np.abs(np.fft.rfft(tr))**2
        feats[i, 0]  = tr.mean()
        feats[i, 1]  = tr.var()
        feats[i, 2]  = float(stats.skew(tr))
        feats[i, 3]  = float(stats.kurtosis(tr))
        for fi, (lo, hi) in enumerate([(0,1e3),(1e3,5e3),(5e3,100e3),(100e3,500e3)]):
            m = (freqs >= lo) & (freqs < hi)
            feats[i, 4+fi] = psd[m].mean() if m.any() else 0
        feats[i, 8]  = tr.max() - tr.min()
        feats[i, 9]  = np.percentile(tr, 75) - np.percentile(tr, 25)
        feats[i, 10] = np.sqrt(np.mean(tr**2))
        feats[i, 11] = np.mean(np.abs(np.diff(tr)))
        feats[i, 12:16] = np.percentile(tr, [10, 30, 70, 90])
        for fi, (lo, hi) in enumerate([(0,2e3),(2e3,10e3),(10e3,50e3),(50e3,200e3)]):
            m = (freqs >= lo) & (freqs < hi)
            feats[i, 16+fi] = psd[m].mean() if m.any() else 0
    return feats

def classify_load(sigma=0.05):
    print(f"\n=== Mechanical State Classifier  sigma={sigma} ===")
    X_all, y_all = [], []
    for load_id in [0, 1, 2]:
        tag    = f"L{load_id}_s{str(sigma).replace('.','')}"
        traces = np.load(os.path.join(TRACES_DIR, f"traces_{tag}.npy"))
        X_all.append(extract_features(traces))
        y_all.extend([load_id] * len(traces))

    X, y = np.vstack(X_all), np.array(y_all)
    clf  = NearestCentroid()
    cv   = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    sc   = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
    print(f"5-fold CV accuracy: {sc.mean()*100:.1f}% +/- {sc.std()*100:.1f}%")

    # Train 200 per class, test rest
    tr_idx, te_idx = [], []
    for c in [0, 1, 2]:
        idx = np.where(y == c)[0]
        tr_idx.extend(idx[:200]); te_idx.extend(idx[200:])
    clf.fit(X[tr_idx], y[tr_idx])
    y_pred = clf.predict(X[te_idx])
    print(classification_report(y[te_idx], y_pred,
          target_names=list(LOAD_LABELS.values())))

    cm = confusion_matrix(y[te_idx], y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap='Blues')
    ax.set_xticks([0,1,2]); ax.set_yticks([0,1,2])
    ax.set_xticklabels(list(LOAD_LABELS.values()), rotation=25)
    ax.set_yticklabels(list(LOAD_LABELS.values()))
    for r in range(3):
        for c in range(3):
            ax.text(c, r, str(cm[r,c]), ha='center', va='center',
                    color='white' if cm[r,c] > cm.max()/2 else 'black')
    ax.set_xlabel('Predicted'); ax.set_ylabel('True')
    ax.set_title(f'Load state confusion matrix  sigma={sigma}')
    plt.colorbar(im, ax=ax); plt.tight_layout()
    out = os.path.join(PLOTS_DIR, f"confusion_s{str(sigma).replace('.','')}.png")
    plt.savefig(out, dpi=150); plt.show()
    return sc.mean()

if __name__ == "__main__":
    classify_load(0.05)
    classify_load(0.15)
