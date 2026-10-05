# Educational Supply vs. Labor Market Demand Dashboard
### AI, Data Science & Statistics (AIDSST)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: Dash/Plotly](https://img.shields.io/badge/framework-Dash%20%2F%20Plotly-00bcd4.svg)](https://plotly.com/dash/)
[![Design: Dark Slate & Cyan](https://img.shields.io/badge/theme-Dark%20Slate%20%26%20Cyan-06b6d4.svg)](#uiux-design-system)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 1. Project Overview & Vision

The **Educational Supply vs. Labor Market Demand Dashboard** is a high-performance interactive web application developed with **Python**, **Plotly**, and **Dash**. The platform bridges the intelligence gap between higher education institutions producing graduates in Quantitative & Computational fields (**Artificial Intelligence**, **Data Science**, and **Statistics**) and the real-world demands of the global labor market.

### Core Business Objectives:
1. **Analyze Supply Dynamics (Tab 1)**: Track annual graduation volumes across global & domestic universities, curriculum compulsory skill coverage, tuition fee economics, and time-to-employment rates.
2. **Monitor Labor Demand & Compensation (Tab 2)**: Measure active job vacancy volumes, employer hiring trends, demanded skill frequencies, salary distributions across seniority tiers, and geographic hiring density.
3. **Quantify Skill Mismatch & Educational ROI (Tab 3)**: Dynamically calculate the supply-demand skill delta ($\text{Demand \%} - \text{Supply \%}$), pinpoint industry **Shortage Skills** vs. academic **Excess Skills**, and compute Tuition-to-Salary Return on Investment (ROI).

---

## 2. System Architecture & Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Dash / Plotly Frontend                      │
│   (Dark Slate #0f172a, Cyan #06b6d4, Interactive Callbacks) │
├──────────────────────────────┬──────────────────────────────┤
│    Tab 1: Supply Side        │     Tab 2: Demand Side       │
│  - Graduation Trends         │  - Job Vacancies Index       │
│  - Curriculum Skills Heatmap │  - Demanded Skills Frequency │
│  - Employment Success Rate   │  - Geographic Salary Map     │
│  - Tuition vs Volume         │  - Seniority Salary Box Plot │
├──────────────────────────────┴──────────────────────────────┤
│                 Tab 3: Gap & ROI Analysis                   │
│  - Dynamic Skill Mismatch Matrix (Demand % - Supply %)      │
│  - Over-supplied vs Under-supplied Skill Cards              │
│  - Tuition vs Entry Salary ROI Scatter Plot                 │
│  - Career Progression & Entry Qualifications Flow           │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               │   Data Pipeline & Backend     │
               │   (Pandas, NumPy, Requests)   │
               └───────────────┬───────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  Academic Supply Open Data   │        │   Labor Market Open Data     │
│  (IPEDS, UNESCO, Benchmarks) │        │ (ds_salaries, Indeed, Skills)│
└──────────────────────────────┘        └──────────────────────────────┘
```

- **Backend & Web Framework**: Python 3.10+ with Dash Server (`dash`, `dash-bootstrap-components`, `flask`)
- **Data Visualization**: Plotly Graph Objects (`plotly.graph_objects`) & Plotly Express (`plotly.express`)
- **Data Engineering**: Pandas, NumPy
- **Interactivity Engine**: Dash Reactive Callbacks with cross-chart filtering and dynamic client state management

---

## 3. Dashboard Features & Layout

### 3.1 Top KPI Summary Cards
- **Global Median Salary**: Aggregated median compensation across filtered roles and experience tiers in USD.
- **Total Tracked Job Openings**: Live hiring demand index calculated across tracked market positions.
- **Top In-Demand Skill**: Dynamically computed #1 skill demanded based on the active role filter.
- **Annual Graduates Growth**: Estimated Year-over-Year (YoY) growth of STEM/Quantitative degree graduates.

### 3.2 Global Filter Control Bar
- **Field Category**: All, Artificial Intelligence (`AI`), Data Science (`Data Science`), Statistics (`Statistics`)
- **Experience Level**: All, Entry (`EN`), Mid-Level (`MI`), Senior (`SE`), Executive (`EX`)
- **Year Range Slider**: Filter historical & forecasted records (2020 – 2026)
- **Geographic Region**: Global, North America, Europe, Asia-Pacific, Latin America

### 3.3 Visual Components Breakdown

| Tab | Component | Chart Type | Key Metrics & Dimensions |
| :--- | :--- | :--- | :--- |
| **Tab 1: Supply Side** | Graduation Volume Trends | Line / Stacked Area | Annual graduates by university and program |
| | Curriculum Compulsory Skills | Heatmap / Matrix | Required subject frequency across degrees |
| | Employment Success Rate | Grouped Bar Chart | Employment % at Year 1, Year 2, and Year 3 |
| | Tuition Fee vs Graduate Volume | Scatter Plot | Total degree tuition (USD) vs total graduates produced |
| **Tab 2: Demand Side** | Job Vacancies Volume Index | Area / Time-Series | Job openings trajectory across fields |
| | Top Demanded Skills Frequency | Ranked Horizontal Bar | Frequency and percentage share of demanded skills |
| | Global Hiring & Salary Map | Choropleth Map | Average salary and job volume by country ISO code |
| | Salary Distribution by Level | Box / Violin Plot | Salary percentiles (P25, Median, P75) by role & tier |
| | Top Hiring Companies & Sectors | Treemap / Bar Chart | Openings count grouped by sector & employer |
| **Tab 3: Gap Analysis** | Supply vs Demand Skill Gap | Diverging Bar Chart | Coverage delta: $(\text{Demand \%} - \text{Supply \%})$ |
| | Shortage vs Excess Skills | Highlight Status Cards | Critical shortage skills vs over-supplied skills |
| | Tuition Fee vs Salary ROI | Scatter / Quadrant | Degree cost vs entry salary payback ratio |
| | Career Progression Pathway | Sankey / Stacked Flow | Degree qualification $\rightarrow$ Level $\rightarrow$ Salary bracket |

---

## 4. Unified Data Schemas

All ingested datasets are harmonized into the standardized schema below:

### 4.1 Academic Supply Schema
```json
{
  "university": "string (e.g. Stanford University, Chulalongkorn University)",
  "program_name": "string (e.g. B.S. in Data Science & AI)",
  "field_category": "AI | Data Science | Statistics",
  "graduation_year": 2024,
  "graduates_count": 185,
  "compulsory_skills": ["Python", "SQL", "Linear Algebra", "Machine Learning"],
  "employed_year_1": 152,
  "employed_year_2": 170,
  "employed_year_3": 178,
  "total_tuition_fee": 48000.0
}
```

### 4.2 Labor Market Demand Schema
```json
{
  "job_id": "string (e.g. JOB-10492)",
  "company_name": "string (e.g. DeepMind, Microsoft, Kasikorn Bank)",
  "job_title": "string (e.g. Machine Learning Engineer)",
  "field_category": "AI | Data Science | Statistics",
  "experience_level": "EN | MI | SE | EX",
  "employment_type": "FT | PT | CT | FL",
  "required_education": "Bachelor | Master | PhD",
  "required_skills": ["Python", "PyTorch", "Docker", "SQL", "Cloud/AWS"],
  "salary_in_usd": 125000.0,
  "salary_min": 110000.0,
  "salary_max": 140000.0,
  "employee_residence": "US",
  "company_location": "US",
  "company_size": "S | M | L",
  "vacancies_count": 3
}
```

---

## 5. UI/UX Design System

The application strictly implements the **Dark Mode Tech Aesthetic** outlined in the project specifications:
- **Background Canvas**: Deep Slate (`#0f172a`)
- **Card & Component Surfaces**: Midnight Slate (`#1e293b`)
- **Border & Separators**: Slate 700 (`#334155`)
- **Primary Accent**: Electric Cyan (`#06b6d4`)
- **Secondary Accent**: Vibrant Teal (`#14b8a6`)
- **Warning / Shortage Accent**: Amber / Rose (`#f59e0b` / `#f43f5e`)
- **Success / Excess Accent**: Emerald (`#10b981`)
- **Typography**: Inter / system sans-serif, Light Slate (`#f1f5f9`), Muted Slate (`#94a3b8`)

---

## 6. Open Data Sources

The dashboard leverages curated public datasets:
1. **ds_salaries.csv**: Global AI and Data Science salary survey records (`YuluDuan/Hypothesis-Testing-Data-Science-salary-comparison-in-different-location`).
2. **Indeed AI Tracker**: Job postings demanding AI/ML/Data skills over time (`hiring-lab/ai-tracker`).
3. **Data Scientist Skills Matrix**: Parsed frequencies for programming languages, frameworks, and tools (`mikeasilva/data-scientist-skills`).
4. **IPEDS & UNESCO STEM Statistics**: Degree completions and enrollment benchmarks across higher education institutions.

---

## 7. Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Maneerat-Aechaiyaphum/Dashboard_AIDSST_Jobs.git
cd Dashboard_AIDSST_Jobs

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### Ingest Data & Run Application
```bash
# Step 1: Run the automated data pipeline to fetch & harmonize datasets
python data_pipeline.py

# Step 2: Start the Dash web application
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:8050/
```

---

## 8. Project Roadmap & Status
Real-time tracking of milestones, deliverables, and progress updates is maintained in [PROJECT_STATUS.md](PROJECT_STATUS.md).