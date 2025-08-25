# ForexFactoryScraper

A web scraper that downloads ForexFactory calendar data and writes it to a CSV.

- Scrapes week-by-week for completeness (no need to click "more").
- Continues from the last row on re-run (incremental).
- Stops automatically when it reaches today (last rows are today's events).
- Post-processes the CSV to remove empty and duplicate rows.

## Requirements

- Google Chrome installed (non-headless required due to Cloudflare)
- Python 3.10+
- pip

## Setup

```sh
# Create and activate a virtual environment (recommended)
python3.10 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

Tip (Apple Silicon/Homebrew Python): `/opt/homebrew/bin/python3.10 -m venv .venv`.

## Run

```sh
python ffs.py
```

What happens when you run it:

- Opens Chrome and scrapes calendar data week-by-week starting from Jan 1, 2007, or from the last date present in `forex_factory_catalog.csv`.
- Writes rows to `forex_factory_catalog.csv` and logs issues to `errors.csv`.
- Automatically deduplicates and removes empty rows after scraping.

## Output files

- `forex_factory_catalog.csv` — cleaned event data
- `errors.csv` — optional log for parsing issues

## Timezone

CSV timestamps are written in Eastern Time (UTC-5/ET with DST when applicable). To change the output timezone, edit the call at the bottom of `ffs.py`:

```python
scrap(gettz('UTC-5'), debug=False)
```

Examples: `gettz('UTC')`, `gettz('America/New_York')`, `gettz('Europe/London')`, etc.

## Quick debug run (optional)

To limit scraping for a quick check, set `debug=True` in the `scrap(...)` call in `ffs.py`.

## Resume or reset

- Resume: run `python ffs.py` again; it continues after the last row in `forex_factory_catalog.csv`.
- Reset: delete `forex_factory_catalog.csv` to start fresh from 2007-01-01.
