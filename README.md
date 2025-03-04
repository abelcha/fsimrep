# fsimrep: Repository Similarity Analyzer

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-altair%20|%20duckdb%20|%20pandas%20|%20tqdm%20|%20tabulate-orange.svg)

fsimrep is a command-line tool designed to find and analyze similar GitHub repositories based on common stargazers. It leverages DuckDB for efficient querying of star event data, calculates Jaccard similarity scores, and provides detailed output including repository descriptions and topics.

## Features
- **Similarity Calculation**: Computes Jaccard similarity based on overlapping stargazers between repositories.
- **Efficient Querying**: Uses DuckDB for fast, optimized SQL queries on large datasets.
- **Detailed Output**: Displays similarity scores, common users, total stars, topics, and descriptions.
- **Progress Tracking**: Includes progress bars via `tqdm` for long-running operations.
- **Customizable**: Adjustable parameters for minimum stars, common users, and result limits.

## Installation

### Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management (optional but recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/abelcha/fsimrep.git
   cd fsimrep