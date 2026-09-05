"""Tests for Kelly sizer."""
import pytest
import pandas as pd
import numpy as np
from kelly.core import (
    kelly_fraction,
    fractional_kelly,
    kelly_from_edge_vol,
    vol_targeted_kelly,
    kelly_matrix,
)


def test_kelly_basic():
    # 60% win prob, 2:1 payoff
    f = kelly_fraction(0.6, 2.0)
    # f* = (0.6*2 - 0.4)/2 = 0.4
    assert abs(f - 0.4) < 1e-9


def test_kelly_zero_edge():
    # 50% win prob = no edge -> 0
    f = kelly_fraction(0.5, 2.0)
    assert f == 0.0


def test_kelly_negative_edge_returns_zero():
    # worse than 50/50 -> 0 (no bet)
    f = kelly_fraction(0.3, 1.0)
    assert f == 0.0


def test_fractional_kelly():
    f = fractional_kelly(0.6, 2.0, fraction=0.5)
    assert abs(f - 0.2) < 1e-9


def test_kelly_from_edge_vol():
    # edge 0.05, vol 0.20 -> f = 0.05/0.04 = 1.25 (capped at 1)
    f = kelly_from_edge_vol(0.05, 0.20)
    assert abs(f - 1.25) < 1e-9


def test_vol_targeted():
    f = vol_targeted_kelly(0.10, 0.40, target_vol=0.15, leverage_cap=1.0)
    # raw = 0.10/0.16 = 0.625, scaled = 0.625 * 0.15/0.40 = 0.234
    assert abs(f - 0.234) < 1e-6


def test_kelly_matrix():
    edges = pd.Series({"A": 0.05, "B": 0.10})
    vols = pd.Series({"A": 0.20, "B": 0.30})
    df = kelly_matrix(edges, vols, target_vol=0.15)
    assert "final" in df.columns
    assert (df["final"] <= 1.0).all()
    assert (df["final"] >= 0.0).all()


if __name__ == "__main__":
    test_kelly_basic()
    test_kelly_zero_edge()
    test_kelly_negative_edge_returns_zero()
    test_fractional_kelly()
    test_kelly_from_edge_vol()
    test_vol_targeted()
    test_kelly_matrix()
    print("All tests passed")
