import numpy as np

def reservation_price(s, q, sigma, gamma, tau):
    """Price at which the maker is indifferent to holding inventory q.
    tau = time remaining. Long inventory pushes this below the mid."""
    return s - q*gamma*(sigma**2)*tau

def optimal_spread(sigma, gamma, k, tau):
    """Total bid-ask spread the maker should quote."""
    return gamma*(sigma**2)*tau + (2/gamma)*np.log(1 + gamma/k)

def quotes(s, q, sigma, gamma, k, tau):
    """Bid and ask, centred on the reservation price."""
    r = reservation_price(s, q, sigma, gamma, tau)
    half = optimal_spread(sigma, gamma, k, tau) / 2
    return r - half, r + half
