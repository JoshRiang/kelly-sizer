# Kelly Criterion Sizing Calculator

<p align="left">
  <img src="https://img.shields.io/badge/Risk%20Management-blue?style=flat-square" alt="topic"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license"/>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" alt="python"/>
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="status"/>
</p>

Position sizing based on Kelly criterion with fractional Kelly and vol targeting.

## Overview

This project is part of a curated portfolio of quantitative finance and software engineering work. It is designed to be:

- **Self-contained** — runs out of the box with `pip install -r requirements.txt`
- **Well-tested** — unit tests cover the core logic
- **Documented** — clear API, type hints, and examples
- **Production-ready patterns** — error handling, logging, CLI

**Stack:** Python 3.10+ | pandas | numpy

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Installation

```bash
git clone https://github.com/JoshRiang/kelly-sizer.git
cd kelly-sizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

```bash
# Run the CLI
python -m <module> --help

# Run the example
python examples/run_example.py
```

## Usage

See the [Examples](#examples) section below and the inline docstrings.

```python
from kelly_sizer import core_function

result = core_function(input_data)
print(result)
```

## Architecture

```
kelly-sizer/
├── src/                  # Core package
├── tests/                # Unit tests
├── examples/             # Usage examples
├── docs/                 # Additional documentation
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── requirements.txt
```

## Testing

```bash
pytest -v
```

Tests use synthetic data to ensure deterministic results without external dependencies.

## Roadmap

- [ ] Additional metrics and visualizations
- [ ] Integration with live data sources
- [ ] Performance optimization for large datasets
- [ ] Extended documentation and tutorials

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Joshua Riangkamang** — [github.com/JoshRiang](https://github.com/JoshRiang)

---

<p align="center">
  Built as part of a quantitative finance and software engineering portfolio.
</p>
