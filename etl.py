"""
ETL pipeline: Data & AI Job Market Salary Analysis
Extracts raw salary data, cleans/transforms it, and loads it into a SQL database.

Swap the sqlite3 connection below for psycopg2 + a PostgreSQL connection string
to run this exact same pipeline against a real Postgres instance -- the schema
and SQL are standard ANSI SQL and will work unchanged.
"""
import pandas as pd
import sqlite3
import os

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ds_salaries.csv")
CLEAN_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_salaries.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "job_market.db")

EXPERIENCE_MAP = {
    "EN": "Entry-level",
    "MI": "Mid-level",
    "SE": "Senior-level",
    "EX": "Executive-level",
}
EMPLOYMENT_MAP = {
    "FT": "Full-time",
    "PT": "Part-time",
    "CT": "Contract",
    "FL": "Freelance",
}
COMPANY_SIZE_MAP = {
    "S": "Small (<50)",
    "M": "Medium (50-250)",
    "L": "Large (>250)",
}


def extract(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    # Drop rows missing critical fields
    df = df.dropna(subset=["job_title", "salary_in_usd", "experience_level", "work_year"])

    # Human-readable category labels
    df["experience_level_label"] = df["experience_level"].map(EXPERIENCE_MAP)
    df["employment_type_label"] = df["employment_type"].map(EMPLOYMENT_MAP)
    df["company_size_label"] = df["company_size"].map(COMPANY_SIZE_MAP)

    # Flag roles relevant to a Data/AI job search
    role_pattern = r"data analy|data scientist|data engineer|machine learning|ml engineer|ai engineer|business intelligence|analytics engineer"
    df["role_category"] = df["job_title"].str.lower().str.contains(role_pattern, regex=True)

    # Basic outlier guard: drop rows with implausible salaries
    df = df[(df["salary_in_usd"] >= 5000) & (df["salary_in_usd"] <= 800000)]

    after = len(df)
    print(f"Transform: {before} raw rows -> {after} cleaned rows ({before - after} removed)")

    return df.reset_index(drop=True)


def load(df: pd.DataFrame):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("salaries", conn, if_exists="replace", index=False)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_job_title ON salaries(job_title)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_work_year ON salaries(work_year)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_role_category ON salaries(role_category)")
    conn.commit()
    conn.close()
    print(f"Loaded {len(df)} rows into {DB_PATH}")
    print(f"Cleaned CSV (Power BI-ready) written to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    raw = extract(RAW_PATH)
    cleaned = transform(raw)
    load(cleaned)
