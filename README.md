# Web Scraping with AgentQL and Playwright

This project demonstrates web scraping using AgentQL and Playwright in Python.

## Prerequisites

- Python 3.12 or higher
- Poetry (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd webscraping
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Install Playwright browsers:
```bash
poetry run playwright install
```

## Usage

Run the scraping script:
```bash
poetry run python main.py
```

To Run the tests:
```bash
poetry run pytest
```

## Project Structure

- `main.py`: Main scraping script
- `pyproject.toml`: Poetry project configuration and dependencies
- `README.md`: Project documentation (this file)

## Dependencies

- agentql: Web scraping framework
- playwright: Browser automation tool
