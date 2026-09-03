# Data & AI Job Market Salary Analysis

An end-to-end data pipeline and analysis project: raw salary data is extracted,
cleaned, loaded into a SQL database, and analyzed with SQL + Python to surface
salary and hiring trends for Data Analyst, Data Scientist, Data Engineer, and
Machine Learning roles.

## Why I built this

I'm graduating with a CS degree and job-hunting for Data Analyst / AI Developer
roles. Instead of a toy dataset, I wanted a project that answers a question I
actually care about: what do these roles pay, which titles are growing, and
where does remote work stand right now. This project is the pipeline I'd want
if I were building the analytics layer for a company's own hiring data.

## Pipeline

```
data/ds_salaries.csv          (raw, 3,755 rows)
        │
        ▼  scripts/etl.py  (extract → clean/transform → load)
        │     - drops exact duplicates (1,171 found)
        │     - maps coded fields to labels (e.g. "SE" → "Senior-level")
        │     - flags Data/AI-relevant job titles
        │     - filters implausible salary outliers
        ▼
db/job_market.db              (SQLite; schema is plain ANSI SQL —
data/cleaned_salaries.csv       swap sqlite3 for psycopg2 to run this
                                 unchanged against real PostgreSQL)
        │
        ▼  sql/queries.sql  (6 analytical queries)
        ▼  scripts/analysis.py  (runs the SQL, generates charts)
        ▼
charts/*.png                  (6 charts)
FINDINGS.md                   (tables behind every chart)
```

## Key findings (2,090 Data/AI-role rows analyzed, 2020–2023)

- **Experience pays**: average salary rises from **$67.2K** (entry) to
  **$98.9K** (mid) to **$152.2K** (senior) to **$188.8K** (executive).
- **The market grew fast**: Data/AI postings in this dataset went from 67
  (2020) to 903 (2023), with average salary climbing from $86.3K to $144.0K
  over the same period.
- **Highest-paying titles**: Principal Data Scientist ($198.2K avg) and
  Machine Learning Software Engineer ($192.4K avg) top the list.
- **Remote work is close to a 3-way split**: 48% fully remote, 45% on-site,
  7% hybrid.
- **Medium-sized companies (50–250 employees) pay the most on average**
  ($138.9K), ahead of large companies ($105.0K) and small companies ($75.9K).
- **Most common titles by volume**: Data Engineer (598), Data Scientist (538),
  and Data Analyst (396) dominate postings.

Full tables behind each finding are in [`FINDINGS.md`](FINDINGS.md).

## Tech stack

Python (pandas), SQL (SQLite, portable to PostgreSQL), matplotlib.

## Running it yourself

```bash
pip install pandas matplotlib tabulate
python scripts/etl.py        # extract, clean, load
python scripts/analysis.py   # run SQL queries, generate charts + findings
```

## Using this in Power BI

`data/cleaned_salaries.csv` is ready to load directly into Power BI Desktop
(Get Data → Text/CSV) to build an interactive dashboard on top of the same
cleaned data used here.

## Dataset

Data Science / AI job salaries, 2020–2023, originally sourced from
[ai-jobs.net](https://ai-jobs.net) salary data (public dataset, ~3,750 rows).

## Possible extensions

- Swap the static CSV for a live job-board API to track postings in real time
- Add year-over-year forecasting for salary trends
- Build the Power BI dashboard on top of `cleaned_salaries.csv`
