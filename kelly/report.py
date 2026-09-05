"""PDF/HTML report generation for Kelly sizing."""
from datetime import datetime
import pandas as pd
from .core import kelly_matrix, fractional_kelly, kelly_from_edge_vol


def generate_report(edges: pd.Series, vols: pd.Series, capital: float = 100_000.0,
                    cov=None, target_vol: float = 0.15) -> str:
    """Generate a Markdown report with sizing recommendations.

    Returns the report as a string (caller decides how to render: print, save .md, or convert to PDF).
    """
    df = kelly_matrix(edges, vols, target_vol=target_vol, cov=cov)
    df["dollar_size"] = (df["final"] * capital).round(2)

    lines = []
    lines.append(f"# Kelly Position Sizing Report")
    lines.append(f"_Generated: {datetime.utcnow().isoformat()}Z_")
    lines.append(f"_Capital: ${capital:,.0f} | Target vol: {target_vol:.0%}_")
    lines.append("")
    lines.append("## Recommended Position Sizes")
    lines.append("")
    lines.append("| Asset | Edge | Vol | Raw Kelly | Vol-Targeted | Final | Dollar Size |")
    lines.append("|-------|------|-----|-----------|--------------|-------|-------------|")
    for asset, row in df.iterrows():
        lines.append(
            f"| {asset} | {row['edge']:.2%} | {row['vol']:.2%} | "
            f"{row['raw_kelly']:.2%} | {row['vol_targeted']:.2%} | "
            f"{row['final']:.2%} | ${row['dollar_size']:,.0f} |"
        )
    lines.append("")
    lines.append("## Methodology")
    lines.append("- Raw Kelly: `f* = edge / variance`")
    lines.append("- Vol-targeted: scaled to hit portfolio vol target")
    if cov is not None:
        lines.append("- Correlation-adjusted: `1/sqrt(1 + (n-1) * avg_corr)`")
    lines.append("- Clipped to [0, 1] (no negative or >100% allocations)")
    lines.append("")
    lines.append("## Caveats")
    lines.append("- Kelly assumes your edge estimate is accurate. Overestimating edge ruins Kelly.")
    lines.append("- Recommended: use 1/2 Kelly in practice to reduce volatility and ruin risk.")
    lines.append("- Edge and vol should be estimated from out-of-sample data, not backtest-in-sample.")
    return "\n".join(lines)
