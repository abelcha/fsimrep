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
- [uv](https://github.com/astral-sh/uv) for dependency management

### Setup
   ```bash
    git clone https://github.com/abelcha/fsimrep.git
    
    ./fsimrep.py vi3k6i5/flashtext                                                                      ✘ 1 master ⬆
    
    2025-03-05 00:29:22 - INFO - Successfully connected to DuckDB
    2025-03-05 00:29:22 - INFO - Calculating similarities for vi3k6i5/flashtext
    2025-03-05 00:29:22 - INFO - Executing similarity query...
    2025-03-05 00:29:23 - INFO - Processing query results...
    Processing results: 100%|█████████████████████████████████████████████████████████| 50/50 [00:00<00:00, 17153.21it/s]
    2025-03-05 00:29:23 - INFO - Similarity calculation completed in 1.46 seconds
    ╒═══════════════════════════════════════╤════════╤══════╤═══════╤════════════════════════════════════════════════════╕
    │ repo                                  │  Score │ %sim │ stars │ Topics                                             │
    ╞═══════════════════════════════════════╪════════╪══════╪═══════╪════════════════════════════════════════════════════╡
    │ github.com/mattlisiv/newsapi-python   │  0.075 │    5 │    67 │ A Python Client for News API                       │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/drivendataorg/erdantic     │  0.056 │    7 │   124 │ Entity relationship diagrams for Python data model │
    │                                       │        │      │       │ classes like Pydantic                              │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/tvst/st-annotated-text     │  0.055 │    5 │    91 │ A simple component to display annotated text in    │
    │                                       │        │      │       │ Streamlit apps.                                    │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/WojciechMula/pyahocorasick │  0.052 │    5 │    97 │ Python module (C extension and plain python)       │
    │                                       │        │      │       │ implementing Aho-Corasick algorithm                │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/zjunlp/AutoKG              │  0.029 │    5 │   173 │                                                    │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/knowsuchagency/promptic    │  0.027 │    5 │   182 │ 90% of what you need for LLM app development.      │
    │                                       │        │      │       │ Nothing you dont.                                │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/manzt/anywidget            │  0.025 │    6 │   238 │ jupyter widgets made easy                          │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/seatgeek/fuzzywuzzy        │  0.023 │    7 │   303 │                                                    │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/henrikbostrom/crepes       │  0.021 │    5 │   241 │                                                    │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/awolverp/cachebox          │  0.021 │    5 │   240 │ The fastest memoizing and caching Python library   │
    │                                       │        │      │       │ written in Rust.                                   │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/sloria/TextBlob            │  0.02  │    8 │   398 │ Simple, Pythonic, text processing--Sentiment       │
    │                                       │        │      │       │ analysis, part-of-speech tagging, noun phrase      │
    │                                       │        │      │       │ extraction, translation, and more.                 │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │ github.com/mahmoud/boltons            │  0.02  │    5 │   250 │ Like builtins, but boltons. 250+ constructs,       │
    │                                       │        │      │       │ recipes, and snippets which extend (and rely on    │
    │                                       │        │      │       │ nothing but) the Python standard library.  Nothing │
    │                                       │        │      │       │ like Michael Bolton.                               │
    ├───────────────────────────────────────┼────────┼──────┼───────┼────────────────────────────────────────────────────┤
    │