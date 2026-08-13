import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, sys
sys.path.insert(0, "src")
from simulate import run
from avellaneda import reservation_price, quotes

def fig_inventory():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for s in range(6):
        ax[0].plot(run("as", seed=s)[2], lw=1, alpha=.8)
        ax[1].plot(run("naive", seed=s)[2], lw=1, alpha=.8)
    for a, t in zip(ax, ["Avellaneda-Stoikov", "naive symmetric"]):
        a.axhline(0, color="black", lw=.6)
        a.set_ylim(-16, 16); a.set_xlabel("step"); a.set_ylabel("inventory")
        a.set_title(t, loc="left", fontsize=10)
    fig.tight_layout(); fig.savefig("figures/fig1_inventory.png", dpi=150)
    print("saved fig1")

def fig_pnl():
    a = np.array([run("as", seed=i)[0] for i in range(3000)])
    n = np.array([run("naive", seed=i)[0] for i in range(3000)])
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.hist(n, bins=70, alpha=.5, density=True, label="naive", color="tab:red")
    ax.hist(a, bins=70, alpha=.5, density=True, label="A-S", color="tab:blue")
    ax.axvline(n.mean(), color="tab:red", ls="--", lw=1)
    ax.axvline(a.mean(), color="tab:blue", ls="--", lw=1)
    ax.set_xlabel("terminal PnL")
    ax.set_ylabel("density")
    ax.set_title("Lower mean, half the variance", loc="left", fontsize=10)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig("figures/fig2_pnl.png", dpi=150)
    print("saved fig2")

def fig_skew():
    from avellaneda import optimal_spread
    s, sigma, gamma, k = 100.0, 2.0, 0.1, 1.5
    qs = np.arange(-20, 21)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for tau, st in [(1.0, "-"), (0.5, "--"), (0.1, ":")]:
        r = [reservation_price(s, q, sigma, gamma, tau) for q in qs]
        ax[0].plot(qs, np.array(r) - s, st, label=f"tau={tau}")
    ax[0].axhline(0, color="black", lw=.6)
    ax[0].set_xlabel("inventory q")
    ax[0].set_ylabel("reservation price - mid")
    ax[0].set_title("Skew is linear in inventory", loc="left", fontsize=10)
    ax[0].legend(frameon=False, fontsize=8)
    taus = np.linspace(0.01, 1, 200)
    for g, st in [(0.05, "-"), (0.1, "--"), (0.3, ":")]:
        ax[1].plot(taus, [optimal_spread(sigma, g, k, t) for t in taus], st,
                   label=f"gamma={g}")
    ax[1].set_xlabel("time remaining")
    ax[1].set_ylabel("optimal spread")
    ax[1].set_title("Spread widens with risk aversion", loc="left", fontsize=10)
    ax[1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig("figures/fig3_skew.png", dpi=150)
    print("saved fig3")
