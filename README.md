# Project 2: Kelly Criterion Sizing Calculator

Position sizing based on Kelly criterion. Given an edge estimate, computes the optimal bet size, with fractional Kelly and volatility targeting for risk control.

## Why this exists
Position sizing is more important than entry signals. Most traders either bet too much (and blow up) or too little (and waste their edge). Kelly gives the mathematically optimal fraction, and fractional Kelly + vol targeting make it safe in practice.

## Features
- Full Kelly, fractional Kelly (1/2, 1/4), volatility-targeted
- Multi-asset Kelly matrix with correlation adjustment
- Output: per-position size in dollars or shares
- CLI + PDF report

## Quick start
```bash
pip install -r requirements.txt
python -m kelly --edge 0.05 --odds 2.0 --capital 100000
```

## Math
Kelly fraction: `f* = (p * b - q) / b`
where p = win prob, q = 1-p, b = win/loss ratio.
For continuous outcomes with known edge and vol: `f* = edge / variance`.

## License
MIT
