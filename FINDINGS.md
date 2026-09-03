# Findings — Data & AI Job Market Salary Analysis

*Generated automatically from `sql/queries.sql` against the cleaned dataset.*

## 1. Average salary by experience level

| experience_level   |   avg_salary_usd |    n |
|:-------------------|-----------------:|-----:|
| Entry-level        |            67240 |  210 |
| Mid-level          |            98960 |  567 |
| Senior-level       |           152181 | 1249 |
| Executive-level    |           188807 |   64 |

## 2. Year-over-year trend

|   work_year |   postings |   avg_salary_usd |
|------------:|-----------:|-----------------:|
|        2020 |         67 |            86264 |
|        2021 |        173 |            91821 |
|        2022 |        947 |           127435 |
|        2023 |        903 |           144011 |

## 3. Top 10 highest-paying titles (min. 5 postings)

| job_title                                |   n |   avg_salary_usd |
|:-----------------------------------------|----:|-----------------:|
| Principal Data Scientist                 |   8 |           198171 |
| Machine Learning Software Engineer       |  10 |           192420 |
| Machine Learning Scientist               |  26 |           163220 |
| ML Engineer                              |  34 |           158352 |
| Analytics Engineer                       |  91 |           150152 |
| Machine Learning Engineer                | 206 |           147466 |
| Machine Learning Infrastructure Engineer |  11 |           143012 |
| Data Analytics Manager                   |  18 |           140630 |
| Data Engineer                            | 598 |           139861 |
| Lead Data Engineer                       |   6 |           139230 |

## 4. Remote-work distribution

| remote_type   |    n |   pct |
|:--------------|-----:|------:|
| Fully remote  | 1004 |  48   |
| On-site       |  943 |  45.1 |
| Hybrid        |  143 |   6.8 |

## 5. Average salary by company size

| company_size    |   avg_salary_usd |    n |
|:----------------|-----------------:|-----:|
| Medium (50-250) |           138942 | 1657 |
| Large (>250)    |           104964 |  320 |
| Small (<50)     |            75867 |  113 |

## 6. Most common titles by posting volume

| job_title                  |   postings |
|:---------------------------|-----------:|
| Data Engineer              |        598 |
| Data Scientist             |        538 |
| Data Analyst               |        396 |
| Machine Learning Engineer  |        206 |
| Analytics Engineer         |         91 |
| ML Engineer                |         34 |
| Machine Learning Scientist |         26 |
| Data Analytics Manager     |         18 |
| Business Data Analyst      |         15 |
| BI Data Analyst            |         15 |
