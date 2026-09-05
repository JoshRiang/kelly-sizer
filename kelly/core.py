"""Kelly criterion core math.

The Kelly fraction answers: what fraction of capital should I bet
to maximize the long-run geometric growth rate of my bankroll,
given a probability edge?
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def kelly_fraction(win_prob: float, win_loss_ratio: float) -> float:
    """Full Kelly fraction for binary outcomes.

    Args:
        win_prob: probability of winning (0, 1)
        win_loss_ratio: ratio of win amount to loss amount (b in literature)

    Returns:
        optimal fraction of capital to bet in [0, 1]
    """
    if not 0 < win_prob < 1:
        raise ValueError("win_prob must be in (0, 1)")
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")
    p = win_prob
    q = 1 - p
    b = win_loss_ratio
    f = (p * b - q) / b
    return max(0.0, f)


def fractional_kelly(win_prob: float, win_loss_ratio: float, fraction: float = 0.5) -> float:
    """Apply a fraction of full Kelly (commonly 1/2 for safety)."""
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1]")
    return kelly_fraction(win_prob, win_loss_ratio) * fraction


def kelly_from_edge_vol(edge: float, vol: float) -> float:
    """Kelly for continuous returns with known edge and volatility.

    f* = edge / variance
    where edge = expected return, vol = standard deviation of returns.
    """
    if vol <= 0:
        raise ValueError("vol must be positive")
    if edge <= 0:
        return 0.0
    return edge / (vol ** 2)


def vol_targeted_kelly(
    edge: float,
    vol: float,
    target_vol: float = 0.15,
    leverage_cap: float = 1.0,
) -> float:
    """Kelly fraction scaled to hit a target annualized portfolio vol.

    Useful when individual assets have very different vols.
    Caps leverage so we never bet more than `leverage_cap` of capital.
    """
    if vol <= 0:
        raise ValueError("vol must be positive")
    raw = kelly_from_edge_vol(edge, vol)
    scaled = raw * (target_vol / vol)
    return max(0.0, min(scaled, leverage_cap))


def kelly_matrix(
    edges: pd.Series,
    vols: pd.Series,
    target_vol: float = 0.15,
    cov: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Per-asset Kelly fractions, optionally adjusted for correlation.

    Returns a DataFrame with raw kelly, scaled kelly, and final size.
    If cov is provided, applies a correlation-aware scaling (1/sqrt(avg corr)).
    """
    if not edges.index.equals(vols.index):
        raise ValueError("edges and vols must share index")
    out = pd.DataFrame(index=edges.index)
    out["edge"] = edges
    out["vol"] = vols
    out["raw_kelly"] = edges.combine(vols, lambda e, v: kelly_from_edge_vol(e, v) if v > 0 else 0.0)
    out["vol_targeted"] = out["raw_kelly"] * (target_vol / out["vol"])
    if cov is not None and len(cov) > 1:
        avg_corr = (cov.values - np.eye(len(cov))).sum() / (len(cov) * (len(cov) - 1))
        avg_corr = max(0.0, min(0.99, avg_corr))
        adj = 1.0 / np.sqrt(1.0 + (len(cov) - 1) * avg_corr)
        out["final"] = out["vol_targeted"] * adj
    else:
        out["final"] = out["vol_targeted"]
    out["final"] = out["final"].clip(lower=0.0, upper=1.0)
    return out
