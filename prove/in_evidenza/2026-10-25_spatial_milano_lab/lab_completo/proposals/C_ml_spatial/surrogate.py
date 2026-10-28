"""4. Neural surrogate test: MLP weight-vector -> candidate scores, vs exact WLC / Monte-Carlo acceptability.
Exact computation is also timed in JavaScript (node) when available, since the browser is the target.
Output: results/surrogate.json. Needs results/access_parcels.csv.gz (access.py)."""
import subprocess, tempfile, time
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.neural_network import MLPRegressor
from common import *

RNG = np.random.default_rng(2)

if __name__ == "__main__":
    A = pd.read_csv(os.path.join(RES, "access_parcels.csv.gz"), dtype={"ref": str})
    D = parcels()[["ref", "gfa_headroom_m2"]]
    C = A[A.soft_site].merge(D, on="ref")
    crit = {"A_jobs": C.A_jobs, "A_school": C.A_school, "A_services": C.A_services, "A_green": C.A_green,
            "metro_close": -C.d_metro, "headroom": C.gfa_headroom_m2}
    X = np.column_stack([pd.Series(v).rank(pct=True) for v in crit.values()]).astype(np.float32)  # rank-normalised 0-1
    n, m = X.shape; K = 100
    w0 = np.full(m, 1 / m)

    def timeit(f, rep=20):
        f(); t = time.perf_counter()
        for _ in range(rep): f()
        return (time.perf_counter() - t) / rep * 1e3

    t_wlc = timeit(lambda: X @ w0)
    W = RNG.dirichlet(np.full(m, 20.0), 1000).astype(np.float32)  # Monte-Carlo around equal weights (concentration 20)

    def acceptability():
        S = X @ W.T                                       # n x 1000
        thr = np.partition(S, n - K, axis=0)[n - K]       # K-th best per draw
        return (S >= thr).mean(1)
    t_mc = timeit(acceptability, rep=3); acc = acceptability()

    # surrogate: w -> scores of a 500-candidate shortlist (top-500 under equal weights)
    sl = np.argsort(-(X @ w0))[:500]; Xs = X[sl]
    Wtr = RNG.dirichlet(np.ones(m), 4000).astype(np.float32); Wte = RNG.dirichlet(np.ones(m), 500).astype(np.float32)
    t0 = time.perf_counter()
    mlp = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=400, early_stopping=True, random_state=0).fit(Wtr, Wtr @ Xs.T)
    t_train = time.perf_counter() - t0
    Yp, Yt = mlp.predict(Wte), Wte @ Xs.T
    rho = [spearmanr(a, b)[0] for a, b in zip(Yp, Yt)]
    top20 = [len(set(np.argsort(-a)[:20]) & set(np.argsort(-b)[:20])) / 20 for a, b in zip(Yp, Yt)]
    one = Wte[:1]
    t_mlp = timeit(lambda: mlp.predict(one), rep=200); t_exact_sl = timeit(lambda: one @ Xs.T, rep=200)

    out = {"n_candidates": n, "n_criteria": m, "criteria": list(crit),
           "numpy_ms": {"wlc_all_candidates": round(t_wlc, 3), "mc1000_acceptability_topK": round(t_mc, 1),
                        "exact_shortlist500": round(t_exact_sl, 4), "mlp_shortlist500": round(t_mlp, 4)},
           "mlp": {"train_s": round(t_train, 1), "spearman_median": round(float(np.median(rho)), 4),
                   "spearman_p5": round(float(np.percentile(rho, 5)), 4), "top20_overlap_mean": round(float(np.mean(top20)), 3),
                   "top20_overlap_p5": round(float(np.percentile(top20, 5)), 3)},
           "acceptability": {"K": K, "candidates_with_P_topK_gt_0.5": int((acc > .5).sum()),
                             "candidates_with_P_topK_gt_0": int((acc > 0).sum())}}
    # exact computation in JS (the browser's language): Float32Array WLC + 1000-draw Monte Carlo
    js = """
const n=%d,m=%d,K=%d,X=new Float32Array(n*m);for(let i=0;i<n*m;i++)X[i]=Math.random();
function wlc(w,s){for(let i=0;i<n;i++){let a=0;for(let j=0;j<m;j++)a+=X[i*m+j]*w[j];s[i]=a;}}
const s=new Float32Array(n),w=new Float32Array(m).fill(1/m),cnt=new Uint16Array(n);
let t=performance.now();for(let r=0;r<100;r++)wlc(w,s);const tw=(performance.now()-t)/100;
t=performance.now();for(let r=0;r<1000;r++){let z=0;for(let j=0;j<m;j++){w[j]=-Math.log(Math.random());z+=w[j];}for(let j=0;j<m;j++)w[j]/=z;
wlc(w,s);const thr=Float32Array.from(s).sort()[n-K];for(let i=0;i<n;i++)if(s[i]>=thr)cnt[i]++;}
console.log(JSON.stringify({wlc_ms:tw,mc1000_ms:performance.now()-t}));""" % (n, m, K)
    try:
        f = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False); f.write(js); f.close()
        out["node_ms"] = json.loads(subprocess.run(["node", f.name], capture_output=True, text=True, timeout=120).stdout)
        os.unlink(f.name)
    except Exception as e:
        out["node_ms"] = f"not measured: {e}"
    save_json(out, "surrogate.json"); log(out)
