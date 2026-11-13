# supply-chain-insights

An explainable supply-chain analytics app built on 180,000+ real-world order records.

**The rule this project follows: code computes the numbers, the LLM only explains them.** Every statistic comes from SQL I can test and verify. The language model's job (coming in a later step) is to explain those results in plain English, with an audit trail of exactly what data it was given.

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

## Data quality notes

I checked the source data before trusting any number from it:

- **Shipping days are calendar days, not 24-hour periods.** Calculating `shipping_date - order_date` in full days matched the dataset's own column for only 175,862 of 180,519 rows. All 4,657 mismatches were off by exactly one day: orders placed late in the evening and shipped the next morning. After comparing dates without their times, all 180,519 rows matched.
- **The late-delivery flag excludes canceled orders.** 4,423 canceled items took longer than scheduled but are not flagged late. That's why late rates here are measured on shipped orders only.
- **Text values are messy.** One region is stored as `South of  USA`, with two spaces. Filters on text need to match the stored value exactly.
- **Each row is one order item, not one order.** The table uses `order_item_id` as its primary key.
- **Personal data is deliberately left out.** The source includes customer names, emails and passwords (masked). None of these are loaded into the database.

## How it works

```
DataCo CSV  →  clean.py  →  load.py  →  PostgreSQL  →  sql/stats.sql
              (select,      (load       (orders         (late-rate
               rename,       180,519     table)          analysis)
               parse dates)  rows)
```

- `explore.py`: first look at the raw data (shape, columns, missing values)
- `clean.py`: `get_clean_data()` selects 15 columns, renames them to snake_case and parses dates; running it directly also runs the shipping-days sanity check
- `sql/schema.sql`: the `orders` table definition
- `load.py`: loads the cleaned data into Postgres
- `db_check.py`: confirms the connection and row count
- `sql/stats.sql`: the analysis queries behind the findings above

## Run it yourself

**Requirements:** Python 3.12, PostgreSQL 17

1. **Get the data.** Download `DataCoSupplyChainDataset.csv` from [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5) and put it in a `data/` folder (git-ignored).

2. **Set up Python:**
   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root (git-ignored, never committed):
   ```
   PGHOST=localhost
   PGPORT=5432
   PGUSER=postgres
   PGPASSWORD=your-password
   PGDATABASE=supply_chain
   ```

4. **Create the database and table:**
   ```
   psql -U postgres -c "CREATE DATABASE supply_chain;"
   psql -U postgres -d supply_chain -f sql/schema.sql
   ```

5. **Load and verify:**
   ```
   python load.py
   python db_check.py     # should print 180519
   ``
## Data source

DataCo Smart Supply Chain for Big Data Analysis, by Fabian Constante, Fernando Silva and António Pereira. Published on [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5), DOI: 10.17632/8gx2fvg2k6.5.
