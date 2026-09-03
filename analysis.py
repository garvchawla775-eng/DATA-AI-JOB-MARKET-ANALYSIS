"""
Runs the analytical SQL queries against the cleaned database and generates
chart images summarizing Data/AI job market salary trends.
"""
import sqlite3
import os
import re
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BASE = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE, "..", "db", "job_market.db")
SQL_PATH = os.path.join(BASE, "..", "sql", "queries.sql")
CHARTS_DIR = os.path.join(BASE, "..", "charts")
FINDINGS_PATH = os.path.join(BASE, "..", "FINDINGS.md")

os.makedirs(CHARTS_DIR, exist_ok=True)

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


def load_queries(path):
    with open(path) as f:
        raw = f.read()
    # split on ';' but keep queries with their leading comment
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    return parts


def run_query(conn, sql):
    return pd.read_sql_query(sql, conn)


def usd_fmt(ax, axis="y"):
    formatter = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def main():
    conn = sqlite3.connect(DB_PATH)
    queries = load_queries(SQL_PATH)
    findings = ["# Findings — Data & AI Job Market Salary Analysis\n",
                "*Generated automatically from `sql/queries.sql` against the cleaned dataset.*\n"]

    # ---- Query 1: avg salary by experience level ----
    df1 = run_query(conn, queries[0])
    fig, ax = plt.subplots(figsize=(7, 4.2))
    order = ["Entry-level", "Mid-level", "Senior-level", "Executive-level"]
    df1["experience_level"] = pd.Categorical(df1["experience_level"], categories=order, ordered=True)
    df1 = df1.sort_values("experience_level")
    ax.bar(df1["experience_level"], df1["avg_salary_usd"], color=ACCENT)
    ax.set_title("Average Salary by Experience Level (Data/AI Roles)", fontweight="bold", color=NAVY)
    ax.set_ylabel("Average Salary (USD)")
    usd_fmt(ax)
    for i, v in enumerate(df1["avg_salary_usd"]):
        ax.text(i, v + 2000, f"${v:,.0f}", ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "01_avg_salary_by_experience.png"), dpi=150)
    plt.close()

    findings.append("## 1. Average salary by experience level\n")
    findings.append(df1.to_markdown(index=False) + "\n")

    # ---- Query 2: year-over-year postings + avg salary ----
    df2 = run_query(conn, queries[1])
    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(df2["work_year"].astype(str), df2["postings"], color=GRAY, label="Postings (n)")
    ax1.set_ylabel("Postings (n)")
    ax2 = ax1.twinx()
    ax2.plot(df2["work_year"].astype(str), df2["avg_salary_usd"], color=NAVY, marker="o", linewidth=2, label="Avg Salary")
    ax2.set_ylabel("Average Salary (USD)")
    usd_fmt(ax2)
    ax1.set_title("Data/AI Job Postings & Avg Salary by Year", fontweight="bold", color=NAVY)
    fig.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "02_yearly_trend.png"), dpi=150)
    plt.close()

    findings.append("## 2. Year-over-year trend\n")
    findings.append(df2.to_markdown(index=False) + "\n")

    # ---- Query 3: top 10 highest paying titles ----
    df3 = run_query(conn, queries[2])
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    df3_sorted = df3.sort_values("avg_salary_usd")
    ax.barh(df3_sorted["job_title"], df3_sorted["avg_salary_usd"], color=ACCENT)
    ax.set_title("Top 10 Highest-Paying Data/AI Titles\n(min. 5 postings)", fontweight="bold", color=NAVY)
    ax.set_xlabel("Average Salary (USD)")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
    usd_fmt(ax, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "03_top_paying_titles.png"), dpi=150)
    plt.close()

    findings.append("## 3. Top 10 highest-paying titles (min. 5 postings)\n")
    findings.append(df3.to_markdown(index=False) + "\n")

    # ---- Query 4: remote work distribution ----
    df4 = run_query(conn, queries[3])
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    colors = [NAVY, ACCENT, GRAY]
    wedges, texts, autotexts = ax.pie(df4["n"], labels=df4["remote_type"], autopct="%1.0f%%", colors=colors,
           textprops={"color": "#333333"})
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title("Remote-Work Split (Data/AI Roles)", fontweight="bold", color=NAVY)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "04_remote_split.png"), dpi=150)
    plt.close()

    findings.append("## 4. Remote-work distribution\n")
    findings.append(df4.to_markdown(index=False) + "\n")

    # ---- Query 5: avg salary by company size ----
    df5 = run_query(conn, queries[4])
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.bar(df5["company_size"], df5["avg_salary_usd"], color=ACCENT)
    ax.set_title("Average Salary by Company Size (Data/AI Roles)", fontweight="bold", color=NAVY)
    ax.set_ylabel("Average Salary (USD)")
    usd_fmt(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "05_salary_by_company_size.png"), dpi=150)
    plt.close()

    findings.append("## 5. Average salary by company size\n")
    findings.append(df5.to_markdown(index=False) + "\n")

    # ---- Query 6: most common titles by volume ----
    df6 = run_query(conn, queries[5])
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    df6_sorted = df6.sort_values("postings")
    ax.barh(df6_sorted["job_title"], df6_sorted["postings"], color=NAVY)
    ax.set_title("Most Common Data/AI Job Titles by Volume", fontweight="bold", color=NAVY)
    ax.set_xlabel("Postings (n)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "06_most_common_titles.png"), dpi=150)
    plt.close()

    findings.append("## 6. Most common titles by posting volume\n")
    findings.append(df6.to_markdown(index=False) + "\n")

    with open(FINDINGS_PATH, "w") as f:
        f.write("\n".join(findings))

    conn.close()
    print("Charts written to:", CHARTS_DIR)
    print("Findings written to:", FINDINGS_PATH)

    # Print a few headline numbers to stdout for quick reference
    print("\n--- Headline numbers ---")
    print(f"Entry-level avg salary: ${df1[df1.experience_level=='Entry-level'].avg_salary_usd.values[0]:,.0f}")
    print(f"Senior-level avg salary: ${df1[df1.experience_level=='Senior-level'].avg_salary_usd.values[0]:,.0f}")
    top_title = df3.sort_values('avg_salary_usd', ascending=False).iloc[0]
    print(f"Highest-paying title: {top_title.job_title} (${top_title.avg_salary_usd:,.0f})")
    remote_pct = df4[df4.remote_type=='Fully remote'].pct.values
    if len(remote_pct):
        print(f"Fully remote share: {remote_pct[0]}%")
    total_n = df1["n"].sum()
    print(f"Total Data/AI rows analyzed: {total_n}")


if __name__ == "__main__":
    main()
