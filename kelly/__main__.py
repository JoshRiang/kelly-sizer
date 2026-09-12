
# Maintenance: last reviewed 2026-09-12 (daily improvement cycle)
"""CLI: python -m kelly --edge 0.05 --odds 2.0 --capital 100000"""
import argparse
import sys
import pandas as pd
from kelly import kelly_fraction, fractional_kelly, generate_report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--edge", type=float, help="single-asset edge (probability of win)")
    p.add_argument("--odds", type=float, default=2.0, help="win/loss ratio")
    p.add_argument("--capital", type=float, default=100000.0)
    p.add_argument("--fraction", type=float, default=0.5, help="fraction of full Kelly (default 0.5 = half Kelly)")
    p.add_argument("--out", help="write report to file")
    args = p.parse_args()

    if args.edge is not None:
        full = kelly_fraction(args.edge, args.odds)
        frac = fractional_kelly(args.edge, args.odds, args.fraction)
        size = frac * args.capital
        print(f"Kelly fraction:     {full:.2%}")
        print(f"Fractional ({args.fraction:.0%}): {frac:.2%}")
        print(f"Position size:      ${size:,.2f}")
    else:
        # demo with sample data
        edges = pd.Series({"SPY": 0.05, "AGG": 0.02, "GLD": 0.03, "NVDA": 0.10})
        vols = pd.Series({"SPY": 0.16, "AGG": 0.05, "GLD": 0.15, "NVDA": 0.45})
        report = generate_report(edges, vols, capital=args.capital)
        print(report)
        if args.out:
            with open(args.out, "w") as f:
                f.write(report)
            print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    main()
