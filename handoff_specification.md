# Handoff Specification: AI & Data Science Market Dashboard

## 1. Executive Summary & Objective

* **Target Agent / Developer**: Antigravity AI
* **Goal**: Build an interactive data visualization dashboard to analyze global trends, salaries, hiring specs, skill requirements, and graduate statistics in AI, Data Science, and Statistics.
* **Source Context**: Open Data aggregated from public academic data systems, national labor statistics, and verified open datasets (IPEDS, UNESCO, BLS, Indeed Hiring Lab, Kaggle/GitHub Open Repos).
* **Target Output**: Single-page interactive web application / dashboard interface.

---

## 2. Expanded Open Data Sources Repository

Antigravity should utilize these open data sources to hydrate the dashboard UI and run data pipelines:

### 2.1 University Graduates Statistics (AI, Data Science & Stats)
1. **IPEDS (Integrated Postsecondary Education Data System) - US NCES**
   * **Description**: Microdata on completion rates for Computer Science, Data Analytics, and Mathematical Statistics degrees.
   * **Format**: CSV / API
   * **URL**: `https://nces.ed.gov/ipeds/use-the-data`
2. **UNESCO Institute for Statistics (UIS) - Tertiary STEM Education**
   * **Description**: Global graduation rates in STEM and Quantitative disciplines across 100+ countries.
   * **Format**: CSV / JSON API
   * **URL**: `http://data.uis.unesco.org/`

### 2.2 Global Salary, Degree & Experience Datasets
1. **Data Science & AI Salaries Open Dataset (ds_salaries.csv)**
   * **Description**: Salary surveys including job titles, experience levels (`EN`, `MI`, `SE`, `EX`), employment types, base pay in USD, and residence/company ISO country codes.
   * **Format**: Raw CSV
   * **URL**: `https://raw.githubusercontent.com/YuluDuan/Hypothesis-Testing-Data-Science-salary-comparison-in-different-location/main/ds_salaries.csv`
2. **Global AI & Data Science Jobs Salary Dataset**
   * **Description**: Extended datasets capturing salary ranges, company sizing, and degree requirements.
   * **Format**: Raw CSV / Kaggle API
   * **URL**: `https://www.kaggle.com/datasets/mohankrishnathalla/global-ai-and-data-jobs-salary-dataset`
3. **U.S. Bureau of Labor Statistics (BLS) Occupational Employment & Wages**
   * **Description**: Official 10-year job outlook, median pay, and entry-level degree baselines for Data Scientists and Statisticians.
   * **Format**: CSV / BLS Public API
   * **URL**: `https://www.bls.gov/ooh/math/data-scientists.htm`

### 2.3 Job Listings, Hiring Volume & Skill Extraction
1. **Indeed Hiring Lab - Global AI Job Postings Tracker**
   * **Description**: Time-series tracking proportion of job postings demanding AI/ML/Data skills per country.
   * **Format**: CSV
   * **URL**: `https://raw.githubusercontent.com/hiring-lab/ai-tracker/main/AI_posting.csv`
2. **Data Science Job Requirements & Skills Matrix**
   * **Description**: Parsed text dataset extracting required programming languages (Python, SQL, R), ML frameworks (PyTorch, TensorFlow), and cloud platforms (AWS, GCP).
   * **Format**: Raw CSV
   * **URL**: `https://raw.githubusercontent.com/mikeasilva/data-scientist-skills/master/raw_skills.csv`
3. **AI & Data Science Job Market Dataset (2020–2026)**
   * **Description**: Consolidated job listings containing company names, industries, skill tags, and entry qualifications.
   * **Format**: CSV
   * **URL**: `https://www.kaggle.com/datasets/shree0910/ai-and-data-science-job-market-dataset-20202026`

---

## 3. Core Features & Dashboard Layout Requirements

### 3.1 Top KPI Summary Cards
1. **Global Median Salary**: Aggregated median salary (in USD) across filtered roles.
2. **Total Tracked Job Openings**: Active hiring index calculated from Indeed/Kaggle datasets.
3. **Top In-Demand Skill**: Dynamic #1 required skill based on user filters (e.g., Python, SQL).
4. **Annual Graduates Growth**: Estimated YoY growth rate of Quantitative/STEM graduates.

### 3.2 Visual Components

#### Chart 1: Salary Distribution by Role & Experience Level
* **Type**: Grouped Bar / Box Plot
* **X-Axis**: Role (`Data Scientist`, `AI Engineer`, `ML Engineer`, `Statistician`)
* **Y-Axis**: Salary in USD
* **Group By**: Experience Level (`EN` Entry, `MI` Mid, `SE` Senior, `EX` Executive)

#### Chart 2: Global Hiring & Salary Geographic Map
* **Type**: Interactive Map or Ranked Bar Chart
* **Dimension**: Country Code (ISO 2-letter: `US`, `GB`, `DE`, `IN`, `SG`, etc.)
* **Metric**: Average Salary vs. Job Volume Index

#### Chart 3: Required Skill Frequency Matrix
* **Type**: Horizontal Bar / Co-occurrence Network
* **Categories**: Programming Languages, Frameworks, MLOps, Soft Skills
* **Interactive Filter**: Toggle between Experience Levels (`Junior/Entry` vs `Senior/Lead`)

#### Chart 4: Career Progression & Entry Qualifications
* **Type**: Stacked Bar Chart / Flow Diagram
* **Dimensions**: Entry Education (`Bachelor`, `Master`, `PhD`) $\rightarrow$ Experience Level $\rightarrow$ Target Salary Range

---

## 4. Unified Data Schema

When fetching or unifying datasets, map fields to the following JSON/Dataframe schema:

```json
{
  "job_id": "STRING (e.g., 'JOB-1029')",
  "job_title": "STRING (e.g., 'Data Scientist', 'AI Engineer')",
  "experience_level": "ENUM ['EN', 'MI', 'SE', 'EX']",
  "employment_type": "ENUM ['FT', 'PT', 'CT', 'FL']",
  "salary_in_usd": "FLOAT",
  "employee_residence": "STRING (ISO 2-letter country code)",
  "company_location": "STRING (ISO 2-letter country code)",
  "company_size": "ENUM ['S', 'M', 'L']",
  "required_education": "ENUM ['Bachelor', 'Master', 'PhD', 'Self-taught']",
  "required_skills": "ARRAY[STRING] (e.g., ['Python', 'SQL', 'PyTorch'])"
}
```

---

## 5. UI/UX Design System & Theme Guidelines

* **Visual Style**: Dark Mode Tech Aesthetic (Background `#0f172a`, Primary Accent Cyan `#06b6d4`, Secondary Accent Teal `#14b8a6`, Text `#f1f5f9`).
* **Global Filters Header**:
  * Filter dropdowns for **Country**, **Experience Level**, and **Job Role**.
  * Filter updates all charts and metric cards simultaneously.
* **Tooltips**: Display exact sample size ($N$), median, 25th/75th percentiles, and percentage relative to total.

---

## 6. Action Items for Antigravity AI

1. **Ingest Open Data**: Fetch CSV files directly from the URLs listed in Section 2.
2. **Data Cleaning & Normalization**: Standardize currency to USD, map country codes, and harmonize experience level tags (`EN`, `MI`, `SE`, `EX`).
3. **Build Dynamic Components**: Construct the layout using web frameworks (e.g., React with Recharts/Chart.js/D3).
4. **Export Capabilities**: Ensure users can filter and export aggregated metrics as CSV or PNG charts.