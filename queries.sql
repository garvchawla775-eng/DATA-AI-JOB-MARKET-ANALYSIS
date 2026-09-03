-- Data & AI Job Market Salary Analysis
-- Extracts run against the `salaries` table (SQLite here -- standard ANSI SQL,
-- runs unchanged against PostgreSQL).

-- 1. Average salary (USD) by experience level, for Data/AI roles only
SELECT
    experience_level_label AS experience_level,
    ROUND(AVG(salary_in_usd), 0) AS avg_salary_usd,
    COUNT(*) AS n
FROM salaries
WHERE role_category = 1
GROUP BY experience_level_label
ORDER BY avg_salary_usd DESC;

-- 2. Year-over-year trend: postings and average salary for Data/AI roles
SELECT
    work_year,
    COUNT(*) AS postings,
    ROUND(AVG(salary_in_usd), 0) AS avg_salary_usd
FROM salaries
WHERE role_category = 1
GROUP BY work_year
ORDER BY work_year;

-- 3. Top 10 highest-average-paying Data/AI job titles (min 5 postings)
SELECT
    job_title,
    COUNT(*) AS n,
    ROUND(AVG(salary_in_usd), 0) AS avg_salary_usd
FROM salaries
WHERE role_category = 1
GROUP BY job_title
HAVING COUNT(*) >= 5
ORDER BY avg_salary_usd DESC
LIMIT 10;

-- 4. Remote-work distribution for Data/AI roles
SELECT
    CASE remote_ratio
        WHEN 0 THEN 'On-site'
        WHEN 50 THEN 'Hybrid'
        WHEN 100 THEN 'Fully remote'
    END AS remote_type,
    COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM salaries WHERE role_category = 1), 1) AS pct
FROM salaries
WHERE role_category = 1
GROUP BY remote_ratio
ORDER BY n DESC;

-- 5. Average salary by company size, for Data/AI roles
SELECT
    company_size_label AS company_size,
    ROUND(AVG(salary_in_usd), 0) AS avg_salary_usd,
    COUNT(*) AS n
FROM salaries
WHERE role_category = 1
GROUP BY company_size_label
ORDER BY avg_salary_usd DESC;

-- 6. Most common Data/AI job titles by posting volume
SELECT
    job_title,
    COUNT(*) AS postings
FROM salaries
WHERE role_category = 1
GROUP BY job_title
ORDER BY postings DESC
LIMIT 10;
