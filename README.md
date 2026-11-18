# supply-chain-insights

An explainable supply-chain analytics app built on 180,000+ real-world order records.

**The rule this project follows: code computes the numbers, the LLM only explains them.** Every statistic comes from SQL I can test and verify. The language model explains those results in plain English, with an audit trail of exactly what data it was given.

## Key findings so far

Measured on shipped orders only (172,765 order items; canceled orders excluded, see data notes below).

**1. 57.3% of shipped order items were delivered late.**

**2. Shipping mode, not geography, drives lateness.**

| Shipping mode  | Items   | Late rate |
|----------------|---------|-----------|
| First Class    | 26,513  | 100.0%    |
| Second Class   | 33,806  | 79.8%     |
| Same Day       | 9,293   | 47.9%     |
| Standard Class | 103,153 | 39.8%     |

Across the 23 regions, late rates sit between 55% and 59% for almost all of them. The extremes (Central Africa at 60.1%, Canada at 51.6%) are also two of the smallest groups, with under 2,000 items each, so they swing more by chance.

**3. First Class's 100% late rate is a dataset artifact, not a business finding.** Every one of its 26,513 shipped items is scheduled for 1 day and recorded as taking exactly 2.

## Demand forecasting

**Data break:** from October 2017, order items drop about 60%, categories shrink from 24 to as few as 8, and from November every item has quantity 1. That looks like a change in how data was recorded, not real demand, so forecasting uses January 2015 to September 2017 only.

Methods compared with MAPE (lower is better):

| Method          | Single split (6 months) | Rolling backtest (7 windows, 3 months) |
|-----------------|-------------------------|----------------------------------------|
| Moving average  | 5.7%                    | 3.9%                                   |
| Holt-Winters    | 5.4%                    | 4.0%                                   |
| Seasonal naive  | 5.2%                    | 4.2%                                   |
| Naive           | 7.7%                    | 4.3%                                   |

The single split favored seasonal naive, but the rolling backtest puts all four methods within 0.4 points. On this stable series, simple methods are as accurate as Holt-Winters and easier to explain.

## LLM explanations

`/explain/forecast` sends only the computed backtest scores to Claude, with rules: no invented or calculated numbers, and no unsupported recommendations. If the model call fails, the endpoint still returns the facts, with a reason instead of an explanation.

## MCP server

Exposes the stats and forecasts as tools any MCP client can call. All SQL and math live in `core/`; the server only wraps them, so the API and the MCP server always return the same numbers.

| Tool | Returns |
|---|---|
| `late_by_shipping_mode` | Late rate per shipping mode (canceled orders excluded) |
| `late_by_region` | Late rate per order region (canceled orders excluded) |
| `forecast_demand(method, months)` | Next 1–12 months of units using naive, seasonal_naive, moving_average or ets |
| `backtest_results` | Average MAPE per method from a rolling 3-month backtest |

## Forecast approval workflow

A LangGraph workflow in `agents/workflow.py`:

1. **Forecaster:** Claude reads the backtest scores and picks a method with a one-line reason. The forecast numbers are computed by code, not by the model.
2. **Verifier:** rule-based checks in `core/verify.py`, deliberately not a second LLM. It rejects an unknown method, a method more than 0.5 MAPE points worse than the best, or numbers that don't match the forecast function. A rejection goes back to the forecaster with feedback, up to 3 attempts.
3. **Human approval:** the graph pauses until a person approves or rejects.

## Data quality notes

I checked the source data before trusting any number from it:

- **Shipping days are calendar days, not 24-hour periods.** Calculating `shipping_date - order_date` in full days matched the dataset's own column for only 175,862 of 180,519 rows. All 4,657 mismatches were off by exactly one day: orders placed late in the evening and shipped the next morning. After comparing dates without their times, all 180,519 rows matched.
- **The late-delivery flag excludes canceled orders.** 4,423 canceled items took longer than scheduled but are not flagged late. That's why late rates here are measured on shipped orders only.
- **Text values are messy.** One region is stored as `South of  USA`, with two spaces. Filters on text need to match the stored value exactly.
- **Each row is one order item, not one order.** The table uses `order_item_id` as its primary key.
- **Personal data is deliberately left out.** The source includes customer names, emails and passwords (masked). None of these are loaded into the database.

## How it works

```
DataCo CSV → pipeline/clean.py → pipeline/load.py → PostgreSQL → core/ (stats, forecast, verify, explain)
                                                                    ↓
                                                interface/ (FastAPI + MCP server) · agents/ (LangGraph workflow)
```

- `pipeline/`: `clean.py` selects 15 columns, renames them to snake_case and parses dates; `load.py` loads them into Postgres
- `core/`: all logic. `db.py` (connection), `stats.py` (late-rate queries), `forecast.py` (methods and backtest), `verify.py` (proposal checks), `explain.py` (Claude explanations)
- `interface/`: `main.py` (FastAPI) and `mcp_server.py` (MCP tools), both thin wrappers over `core/`
- `agents/`: `workflow.py`, the forecast approval workflow
- `scripts/`: `explore.py`, `db_check.py`, `llm_check.py` (one-off checks)
- `sql/`: `schema.sql` (the `orders` table) and the analysis queries
- `tests/`: pytest suite, run by GitHub Actions on every push and pull request

## Run it yourself

**Requirements:** Python 3.12, PostgreSQL 17

1. **Get the data.** Download `DataCoSupplyChainDataset.csv` from [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5) and put it in a `data/` folder (git-ignored).

2. **Set up Python:**
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root (git-ignored, never committed):
   ```
   PGHOST=localhost
   PGPORT=5432
   PGUSER=postgres
   PGPASSWORD=your-password
   PGDATABASE=supply_chain
   ANTHROPIC_API_KEY=your-key
   ANTHROPIC_MODEL=a-current-claude-model-id
   ```

4. **Create the database and table:**
   ```
   psql -U postgres -c "CREATE DATABASE supply_chain;"
   psql -U postgres -d supply_chain -f sql/schema.sql
   ```

5. **Load and verify:**
   ```
   python -m pipeline.load
   python -m scripts.db_check    # should print 180519
   ```

6. **Start the API:**
   ```
   python -m uvicorn interface.main:app --reload
   ```
   Then open 127.0.0.1:8000/docs to try every endpoint.

7. **Run the MCP server** in the MCP Inspector:
   ```
   mcp dev interface/mcp_server.py
   ```

8. **Run the approval workflow:**
   ```
   python -m agents.workflow
   ```

9. **Run the tests:**
   ```
   python -m pytest
   ```

## Data source

DataCo Smart Supply Chain for Big Data Analysis, by Fabian Constante, Fernando Silva and António Pereira. Published on [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5), DOI: 10.17632/8gx2fvg2k6.5.