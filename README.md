# Kelly Criterion Sizing Calculator

Position sizing based on Kelly criterion with fractional Kelly and vol targeting.

Answers: what fraction of capital should I bet to maximize long-run geometric growth, given a probability edge? Implements full/fractional binary Kelly, continuous `edge / variance` Kelly, vol-targeted Kelly scaled to a target annualized portfolio vol, and a correlation-adjusted Kelly matrix across multiple assets. CLI prints per-asset sizes and dollar amounts; `generate_report` emits a Markdown report (print, save .md, or convert to PDF). Captured formulas: `f* = (p*b − q) / b` for binary outcomes; `f* = edge / vol²` for continuous returns; correlation adjustment `1 / sqrt(1 + (n−1)·avg_corr)`.

```bash
git clone https://github.com/JoshRiang/kelly-sizer.git
cd kelly-sizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
# Single binary bet: 60% win prob, 2:1 payoff, half Kelly, $100k capital
python -m kelly --edge 0.6 --odds 2.0 --capital 100000 --fraction 0.5

# Multi-asset demo (SPY, AGG, GLD, NVDA) with vol targeting at 15%
python -m kelly --capital 100000 --out report.md
```

```python
from kelly import kelly_fraction, fractional_kelly, kelly_from_edge_vol, vol_targeted_kelly, kelly_matrix, generate_report
import pandas as pd

# Binary Kelly: 60% win rate, 2:1 payoff -> f* = 0.40 (40% of capital)
f = kelly_fraction(0.6, 2.0)        # 0.4
half = fractional_kelly(0.6, 2.0, 0.5)  # 0.2

# Continuous Kelly: edge 5%, vol 20% -> f = 0.05 / 0.04 = 1.25 (125% leveraged)
f = kelly_from_edge_vol(0.05, 0.20)

# Vol-targeted: scale to 15% portfolio vol, cap leverage at 1.0x
f = vol_targeted_kelly(edge=0.10, vol=0.40, target_vol=0.15, leverage_cap=1.0)

# Multi-asset matrix with correlation adjustment
edges = pd.Series({'SPY': 0.05, 'AGG': 0.02, 'GLD': 0.03, 'NVDA': 0.10})
vols  = pd.Series({'SPY': 0.16, 'AGG': 0.05, 'GLD': 0.15, 'NVDA': 0.45})
df = kelly_matrix(edges, vols, target_vol=0.15)
print(df[['raw_kelly', 'vol_targeted', 'final']])

# Markdown report with dollar sizes
report = generate_report(edges, vols, capital=100_000, target_vol=0.15)
print(report)
```

Project structure:

```
kelly-sizer/
├── kelly/
│   ├── __init__.py     # exports: kelly_fraction, fractional_kelly, vol_targeted_kelly, kelly_from_edge_vol, kelly_matrix, generate_report
│   ├── core.py         # kelly math: binary, fractional, edge/vol, vol-targeted, correlation matrix
│   ├── report.py       # generate_report: Markdown sizing report with methodology + caveats
│   └── __main__.py     # CLI: --edge --odds --capital --fraction --out
├── tests/test_kelly.py # synthetic unit tests: basic Kelly, zero edge, fractional, edge/vol, vol-targeted, matrix clipping
├── requirements.txt    # pandas, numpy
├── LICENSE
└── README.md
```

Testing:

```bash
pytest -v
```

License: MIT — see [LICENSE](LICENSE).

Author: Joshua Riangkamang — [github.com/JoshRiang](https://github.com/JoshRiang)
