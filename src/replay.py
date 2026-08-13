import numpy as np, pandas as pd, sys
sys.path.insert(0, "src")
from lobster import load
from avellaneda import quotes

def prep(ticker="AAPL"):
    """Mid-price series and executed trades from the LOBSTER files."""
    msg, book = load(ticker)
    mid = (book.ap1 + book.bp1) / 2.0
    df = pd.DataFrame({
        "time": msg.time.values,
        "event": msg.event.values,
        "price": msg.price.values,
        "size": msg["size"].values,
        "direction": msg.direction.values,
        "mid": mid.values,
        "ask": book.ap1.values,
        "bid": book.bp1.values,
    })
    return df

def run_replay(df, gamma=0.1, k=1.5, sigma=None, horizon=None, naive_half=None):
    """Quote continuously against real flow. Fill when a trade crosses us."""
    if sigma is None:
        lr = np.diff(np.log(df.mid.values[::100]))
        sigma = lr.std() * np.sqrt(len(df)/100)
    t0, t1 = df.time.iloc[0], df.time.iloc[-1]
    if horizon is None:
        horizon = t1 - t0
    q, cash = 0, 0.0
    fills = []
    for row in df.itertuples():
        if row.event != 4:
            continue
        tau = max((t1 - row.time) / horizon, 1e-6)
        if naive_half is None:
            bid, ask = quotes(row.mid, q, sigma, gamma, k, tau)
        else:
            bid, ask = row.mid - naive_half, row.mid + naive_half
        if row.direction == -1 and row.price <= bid:
            q += 1; cash -= bid
            fills.append((row.time, "buy", bid, row.mid, q))
        elif row.direction == 1 and row.price >= ask:
            q -= 1; cash += ask
            fills.append((row.time, "sell", ask, row.mid, q))
    return cash + q*df.mid.iloc[-1], q, pd.DataFrame(
        fills, columns=["time","side","price","mid","q_after"])

def markouts(df, fills, horizons=(1, 10, 60)):
    """Signed mid-price move after each fill, from the maker's perspective.
    Negative means the price went against us: adverse selection."""
    t = df.time.values
    mid = df.mid.values
    out = {h: [] for h in horizons}
    for f in fills.itertuples():
        j = np.searchsorted(t, f.time)
        sign = 1.0 if f.side == "buy" else -1.0
        for h in horizons:
            j2 = np.searchsorted(t, f.time + h)
            j2 = min(j2, len(mid)-1)
            out[h].append(sign * (mid[j2] - f.mid))
    return {h: np.array(v) for h, v in out.items()}
