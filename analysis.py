"""Generate charts and findings for the Data & AI Job Market analysis."""

from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "job_market.db"
SQL_PATH = BASE_DIR / "queries.sql"
CHARTS_DIR = BASE_DIR / "charts"
FINDINGS_PATH = BASE_DIR / "FINDINGS.md"

CHARTS_DIR.mkdir(exist_ok=True)

NAVY = "#1F3864"
ACCENT = "#4472C4"
GRAY = "#8497B0"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#333333",
    "text.color": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "font.size": 11,
})


def load_queries(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    raw = path.read_text(encoding="utf-8")
    return [part.strip() for part in raw.split(";") if part.strip()]


def run_query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)


def usd_fmt(ax, axis: str = "y") -> None:
    formatter = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Run `python etl.py` first."
        )

    queries = load_queries(SQL_PATH)
    if len(queries) < 6:
        raise ValueError("Expected at least 6 SQL queries in queries.sql")

    findings = [
        "# Findings — Data & AI Job Market Salary Analysis\n",
        "*Generated automatically from `queries.sql` against the cleaned dataset.*\n",
    ]

    with sqlite3.connect(DB_PATH) as conn:
        df1 = run_query(conn, queries[0])
        fig, ax = plt.subplots(figsize=(7, 4.2))
        order = ["Entry-level", "Mid-level", "Senior-level", "Executive-level"]
        df1["experience_level"] = pd.Categorical(
            df1["experience_level"], categories=order, ordered=True
        )
        df1 = df1.sort_values("experience_level")
        ax.bar(df1["experience_level"], df1["avg_salary_usd"], color=ACCENT)
        ax.set_title("Average Salary by Experience Level (Data/AI Roles)", fontweight="bold", color=NAVY)
        ax.set_ylabel("Average Salary (USD)")
        usd_fmt(ax)
        for i, value in enumerate(df1["avg_salary_usd"]):
            ax.text(i, value + 2000, f"${value:,.0f}", ha="center", fontsize=9)
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "01_avg_salary_by_experience.png", dpi=150)
        plt.close()
        findings += ["## 1. Average salary by experience level\n", df1.to_markdown(index=False) + "\n"]

        df2 = run_query(conn, queries[1])
        fig, ax1 = plt.subplots(figsize=(7, 4.2))
        ax1.bar(df2["work_year"].astype(str), df2["postings"], color=GRAY)
        ax1.set_ylabel("Postings (n)")
        ax2 = ax1.twinx()
        ax2.plot(df2["work_year"].astype(str), df2["avg_salary_usd"], color=NAVY, marker="o", linewidth=2)
        ax2.set_ylabel("Average Salary (USD)")
        usd_fmt(ax2)
        ax1.set_title("Data/AI Job Postings & Avg Salary by Year", fontweight="bold", color=NAVY)
        fig.tight_layout()
        plt.savefig(CHARTS_DIR / "02_yearly_trend.png", dpi=150)
        plt.close()
        findings += ["## 2. Year-over-year trend\n", df2.to_markdown(index=False) + "\n"]

        df3 = run_query(conn, queries[2])
        fig, ax = plt.subplots(figsize=(8.5, 4.8))
        df3_sorted = df3.sort_values("avg_salary_usd")
        ax.barh(df3_sorted["job_title"], df3_sorted["avg_salary_usd"], color=ACCENT)
        ax.set_title("Top 10 Highest-Paying Data/AI Titles\n(min. 5 postings)", fontweight="bold", color=NAVY)
        ax.set_xlabel("Average Salary (USD)")
        ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
        usd_fmt(ax, axis="x")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "03_top_paying_titles.png", dpi=150)
        plt.close()
        findings += ["## 3. Top 10 highest-paying titles (min. 5 postings)\n", df3.to_markdown(index=False) + "\n"]

        df4 = run_query(conn, queries[3])
        fig, ax = plt.subplots(figsize=(5.5, 4.2))
        colors = [NAVY, ACCENT, GRAY]
        _, _, autotexts = ax.pie(
            df4["n"], labels=df4["remote_type"], autopct="%1.0f%%", colors=colors,
            textprops={"color": "#333333"}
        )
        for text in autotexts:
            text.set_color("white")
            text.set_fontweight("bold")
        ax.set_title("Remote-Work Split (Data/AI Roles)", fontweight="bold", color=NAVY)
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "04_remote_split.png", dpi=150)
        plt.close()
        findings += ["## 4. Remote-work distribution\n", df4.to_markdown(index=False) + "\n"]

        df5 = run_query(conn, queries[4])
        fig, ax = plt.subplots(figsize=(6, 4.2))
        ax.bar(df5["company_size"], df5["avg_salary_usd"], color=ACCENT)
        ax.set_title("Average Salary by Company Size (Data/AI Roles)", fontweight="bold", color=NAVY)
        ax.set_ylabel("Average Salary (USD)")
        usd_fmt(ax)
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "05_salary_by_company_size.png", dpi=150)
        plt.close()
        findings += ["## 5. Average salary by company size\n", df5.to_markdown(index=False) + "\n"]

        df6 = run_query(conn, queries[5])
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        df6_sorted = df6.sort_values("postings")
        ax.barh(df6_sorted["job_title"], df6_sorted["postings"], color=NAVY)
        ax.set_title("Most Common Data/AI Job Titles by Volume", fontweight="bold", color=NAVY)
        ax.set_xlabel("Postings (n)")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "06_most_common_titles.png", dpi=150)
        plt.close()
        findings += ["## 6. Most common titles by posting volume\n", df6.to_markdown(index=False) + "\n"]

    FINDINGS_PATH.write_text("\n".join(findings), encoding="utf-8")

    print("Charts written to:", CHARTS_DIR)
    print("Findings written to:", FINDINGS_PATH)


if __name__ == "__main__":
    main()
