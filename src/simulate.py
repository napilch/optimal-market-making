import numpy as np, sys
sys.path.insert(0, "src")
from avellaneda import quotes

def run(strategy, T=1.0, n=200, sigma=2.0, gamma=0.1, k=1.5, A=140.0,
        s0=100.0, seed=0, fixed_half=0.85):
    """One session. strategy: 'as' or 'naive'. Returns (pnl, max|q|, path)."""
    rng = np.random.default_rng(seed)
    dt = T/n
    s, q, cash = s0, 0, 0.0
    qs = []
    for i in range(n):
        tau = T - i*dt
        if strategy == "as":
            bid, ask = quotes(s, q, sigma, gamma, k, tau)
        else:
            bid, ask = s - fixed_half, s + fixed_half
        db, da = s - bid, ask - s
        pb = 1 - np.exp(-A*np.exp(-k*db)*dt)
        pa = 1 - np.exp(-A*np.exp(-k*da)*dt)
        if rng.random() < pb:
            q += 1; cash -= bid
        if rng.random() < pa:
            q -= 1; cash += ask
        qs.append(q)
        s += sigma*np.sqrt(dt)*rng.standard_normal()
    return cash + q*s, max(abs(np.array(qs))), qs
