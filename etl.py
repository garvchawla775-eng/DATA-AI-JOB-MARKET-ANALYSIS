"""ETL pipeline for the Data & AI Job Market Salary Analysis project."""

from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
RAW_PATH = BASE_DIR / "ds_salaries.csv"
CLEAN_CSV_PATH = BASE_DIR / "cleaned_salaries.csv"
DB_PATH = BASE_DIR / "job_market.db"

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

ROLE_PATTERN = (
    r"data analy|data scientist|data engineer|machine learning|ml engineer|"
    r"ai engineer|business intelligence|analytics engineer"
)


def extract(path: Path) -> pd.DataFrame:
    """Read the raw salary dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset and add human-readable analytical fields."""
    before = len(df)
    cleaned = df.drop_duplicates().copy()

    cleaned = cleaned.dropna(
        subset=["job_title", "salary_in_usd", "experience_level", "work_year"]
    ).copy()

    cleaned["experience_level_label"] = cleaned["experience_level"].map(EXPERIENCE_MAP)
    cleaned["employment_type_label"] = cleaned["employment_type"].map(EMPLOYMENT_MAP)
    cleaned["company_size_label"] = cleaned["company_size"].map(COMPANY_SIZE_MAP)

    cleaned["role_category"] = (
        cleaned["job_title"]
        .astype(str)
        .str.lower()
        .str.contains(ROLE_PATTERN, regex=True, na=False)
    )

    cleaned = cleaned[
        cleaned["salary_in_usd"].between(5_000, 800_000, inclusive="both")
    ].copy()

    after = len(cleaned)
    print(
        f"Transform: {before} raw rows -> {after} cleaned rows "
        f"({before - after} removed)"
    )
    return cleaned.reset_index(drop=True)


def load(df: pd.DataFrame) -> None:
    """Write the cleaned CSV and refresh the local SQLite database."""
    df.to_csv(CLEAN_CSV_PATH, index=False)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("salaries", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_job_title ON salaries(job_title)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_work_year ON salaries(work_year)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_role_category ON salaries(role_category)"
        )

    print(f"Loaded {len(df)} rows into {DB_PATH}")
    print(f"Cleaned CSV written to {CLEAN_CSV_PATH}")


def main() -> None:
    raw = extract(RAW_PATH)
    cleaned = transform(raw)
    load(cleaned)


if __name__ == "__main__":
    main()
