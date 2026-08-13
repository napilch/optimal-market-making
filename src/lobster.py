import numpy as np, pandas as pd

MSG_COLS = ["time","event","order_id","size","price","direction"]

def load(ticker="AAPL", date="2012-06-21", levels=10, path="data"):
    """Load LOBSTER message and orderbook files, aligned row-for-row."""
    stem = f"{path}/{ticker}_{date}_34200000_57600000"
    msg = pd.read_csv(f"{stem}_message_{levels}.csv", header=None, names=MSG_COLS)
    cols = []
    for i in range(1, levels+1):
        cols += [f"ap{i}", f"av{i}", f"bp{i}", f"bv{i}"]
    book = pd.read_csv(f"{stem}_orderbook_{levels}.csv", header=None, names=cols)
    for c in cols:
        if c.startswith(("ap","bp")):
            book[c] = book[c] / 10000.0
    msg["price"] = msg["price"] / 10000.0
    return msg, book
