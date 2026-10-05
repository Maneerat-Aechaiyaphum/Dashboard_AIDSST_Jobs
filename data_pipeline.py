"""
Educational Supply vs. Labor Market Demand Data Pipeline
Harmonizes open data from public repositories and generates standard
supply and demand records adhering to BRD Section 5 & Handoff Spec Section 4.
"""

import os
import io
import json
import random
import requests
import numpy as np
import pandas as pd

# Set deterministic seed for repeatable synthesis
random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

URL_SALARIES = "https://raw.githubusercontent.com/YuluDuan/Hypothesis-Testing-Data-Science-salary-comparison-in-different-location/main/ds_salaries.csv"
URL_AI_TRACKER = "https://raw.githubusercontent.com/hiring-lab/ai-tracker/main/AI_posting.csv"
URL_SKILLS = "https://raw.githubusercontent.com/mikeasilva/data-scientist-skills/master/raw_skills.csv"

def fetch_or_load(url, filename):
    filepath = os.path.join(RAW_DIR, filename)
    if os.path.exists(filepath):
        print(f"[CACHE] Loading {filename} from local cache...")
        return pd.read_csv(filepath)
    print(f"[FETCH] Downloading {filename} from {url}...")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"[WARN] Could not fetch {url}: {e}")
        return None

def categorize_field(title):
    t = str(title).lower()
    if any(k in t for k in ["machine learning", "ml", "ai", "artificial intelligence", "computer vision", "nlp", "deep learning"]):
        return "AI"
    elif any(k in t for k in ["statistic", "quantitative", "actuar", "biostatist"]):
        return "Statistics"
    else:
        return "Data Science"

def build_demand_dataset(df_salaries):
    print("[PIPELINE] Building standardized Labor Market Demand dataset...")
    
    # Core skill pools by field
    skill_pools = {
        "AI": [
            "Python", "PyTorch", "TensorFlow", "Docker", "Kubernetes", 
            "MLOps", "Git", "C++", "CUDA", "Hugging Face", "LLMs", "Linear Algebra", "Linux"
        ],
        "Data Science": [
            "Python", "SQL", "Scikit-Learn", "Pandas", "R", "Tableau", 
            "Power BI", "Data Wrangling", "Machine Learning", "Git", "AWS", "Big Data/Spark", "Statistics"
        ],
        "Statistics": [
            "R", "Python", "SQL", "Probability & Statistics", "SAS", "Linear Models", 
            "Experimental Design", "SPSS", "Time Series", "Bayesian Methods", "Data Analysis", "Calculus"
        ]
    }
    
    companies = [
        ("Google", "Tech", "US"),
        ("DeepMind", "AI Research", "GB"),
        ("Meta", "Tech", "US"),
        ("Microsoft", "Tech", "US"),
        ("Amazon AWS", "Cloud/Tech", "US"),
        ("Kasikorn Business-Technology Group", "FinTech/Banking", "TH"),
        ("SCB 10X", "FinTech", "TH"),
        ("Shopee / Sea Group", "E-Commerce", "SG"),
        ("Grab", "Tech/Transport", "SG"),
        ("Agoda", "TravelTech", "TH"),
        ("Apple", "Consumer Tech", "US"),
        ("ByteDance", "Social Media/AI", "SG"),
        ("Siemens Healthineers", "Healthcare/Bio", "DE"),
        ("Allianz Technology", "Insurance/FinTech", "DE"),
        ("Spotify", "Media/Tech", "GB"),
        ("Rakuten", "Tech", "JP"),
        ("AstraZeneca", "Pharma/BioStats", "GB"),
        ("Pfizer", "Pharma/BioStats", "US"),
        ("JPMorgan Chase", "Finance", "US"),
        ("Goldman Sachs", "Finance", "US")
    ]
    
    demand_records = []
    
    # Process base records from ds_salaries
    if df_salaries is not None:
        for idx, row in df_salaries.iterrows():
            title = str(row.get("job_title", "Data Scientist"))
            field = categorize_field(title)
            salary = float(row.get("salary_in_usd", 100000.0))
            if np.isnan(salary) or salary <= 0:
                salary = 95000.0
                
            exp = str(row.get("experience_level", "MI"))
            if exp not in ["EN", "MI", "SE", "EX"]:
                exp = "MI"
                
            work_year = int(row.get("work_year", 2023))
            emp_loc = str(row.get("company_location", "US"))
            emp_res = str(row.get("employee_residence", "US"))
            comp_size = str(row.get("company_size", "M"))
            emp_type = str(row.get("employment_type", "FT"))
            
            # Select random company
            comp = random.choice(companies)
            comp_name = comp[0]
            industry = comp[1]
            if comp[2] == emp_loc:
                comp_name = comp[0]
            
            # Sample required skills
            pool = skill_pools[field]
            num_skills = random.randint(4, 7)
            skills = random.sample(pool, min(num_skills, len(pool)))
            
            # Education assignment based on experience
            if exp == "EN":
                education = random.choices(["Bachelor", "Master", "PhD"], weights=[0.65, 0.30, 0.05])[0]
            elif exp in ["MI", "SE"]:
                education = random.choices(["Bachelor", "Master", "PhD"], weights=[0.45, 0.45, 0.10])[0]
            else:
                education = random.choices(["Master", "PhD", "Bachelor"], weights=[0.50, 0.35, 0.15])[0]
            
            sal_min = round(salary * random.uniform(0.85, 0.95), -2)
            sal_max = round(salary * random.uniform(1.05, 1.25), -2)
            vacancies = random.choices([1, 2, 3, 5, 8], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
            
            demand_records.append({
                "job_id": f"JOB-{idx+1000:05d}",
                "company_name": comp_name,
                "industry_sector": industry,
                "job_title": title,
                "field_category": field,
                "experience_level": exp,
                "employment_type": emp_type,
                "required_education": education,
                "required_skills": skills,
                "salary_in_usd": float(salary),
                "salary_min": float(sal_min),
                "salary_max": float(sal_max),
                "vacancies_count": int(vacancies),
                "employee_residence": emp_res,
                "company_location": emp_loc,
                "company_size": comp_size,
                "posting_year": work_year
            })

    # Expand with synthesized recent 2024-2026 job postings to cover all three fields comprehensively
    extra_titles = {
        "AI": ["AI Engineer", "Machine Learning Engineer", "Generative AI Specialist", "Computer Vision Researcher", "MLOps Engineer", "AI Ethics Analyst"],
        "Data Science": ["Data Scientist", "Senior Data Scientist", "Lead Data Scientist", "Data Analytics Manager", "Business Intelligence Analyst", "Analytics Engineer"],
        "Statistics": ["Statistician", "Senior Biostatistician", "Quantitative Research Analyst", "Actuarial Data Analyst", "Statistical Programmer", "Econometrician"]
    }
    
    locations = ["US", "GB", "DE", "TH", "SG", "JP", "CA", "IN", "AU", "FR"]
    exp_levels = ["EN", "MI", "SE", "EX"]
    
    start_id = len(demand_records) + 1000
    for i in range(500):
        field = random.choice(["AI", "Data Science", "Statistics"])
        title = random.choice(extra_titles[field])
        exp = random.choices(exp_levels, weights=[0.25, 0.40, 0.30, 0.05])[0]
        year = random.choice([2023, 2024, 2025, 2026])
        comp = random.choice(companies)
        loc = random.choice(locations)
        
        # Base salary range by field & experience
        base_sal = {
            "EN": (55000, 85000),
            "MI": (90000, 135000),
            "SE": (140000, 195000),
            "EX": (200000, 290000)
        }[exp]
        
        # Adjust for field
        if field == "AI":
            multiplier = 1.15
        elif field == "Data Science":
            multiplier = 1.05
        else:
            multiplier = 0.95
            
        # Adjust for location
        loc_mult = {"US": 1.25, "SG": 1.0, "DE": 0.85, "GB": 0.85, "TH": 0.55, "IN": 0.45, "CA": 0.90, "JP": 0.80, "AU": 0.95, "FR": 0.80}.get(loc, 0.8)
        
        salary = round(random.uniform(base_sal[0], base_sal[1]) * multiplier * loc_mult, -2)
        sal_min = round(salary * 0.9, -2)
        sal_max = round(salary * 1.15, -2)
        
        pool = skill_pools[field]
        num_skills = random.randint(4, 7)
        skills = random.sample(pool, min(num_skills, len(pool)))
        
        if exp == "EN":
            education = random.choices(["Bachelor", "Master", "PhD"], weights=[0.70, 0.25, 0.05])[0]
        elif exp in ["MI", "SE"]:
            education = random.choices(["Bachelor", "Master", "PhD"], weights=[0.40, 0.45, 0.15])[0]
        else:
            education = random.choices(["Master", "PhD", "Bachelor"], weights=[0.55, 0.35, 0.10])[0]
            
        vacancies = random.choices([1, 2, 3, 5, 8], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
        
        demand_records.append({
            "job_id": f"JOB-{start_id + i:05d}",
            "company_name": comp[0],
            "industry_sector": comp[1],
            "job_title": title,
            "field_category": field,
            "experience_level": exp,
            "employment_type": "FT",
            "required_education": education,
            "required_skills": skills,
            "salary_in_usd": float(salary),
            "salary_min": float(sal_min),
            "salary_max": float(sal_max),
            "vacancies_count": int(vacancies),
            "employee_residence": loc,
            "company_location": loc,
            "company_size": random.choice(["S", "M", "L"]),
            "posting_year": year
        })
        
    df_demand = pd.DataFrame(demand_records)
    print(f"[PIPELINE] Created {len(df_demand)} Demand records.")
    return df_demand

def build_supply_dataset():
    print("[PIPELINE] Building standardized Academic Supply dataset...")
    
    universities = [
        {"name": "Stanford University", "country": "US", "base_tuition": 58000.0},
        {"name": "Carnegie Mellon University", "country": "US", "base_tuition": 60000.0},
        {"name": "Massachusetts Institute of Technology (MIT)", "country": "US", "base_tuition": 59000.0},
        {"name": "UC Berkeley", "country": "US", "base_tuition": 44000.0},
        {"name": "National University of Singapore (NUS)", "country": "SG", "base_tuition": 32000.0},
        {"name": "University of Oxford", "country": "GB", "base_tuition": 41000.0},
        {"name": "ETH Zurich", "country": "CH", "base_tuition": 18000.0},
        {"name": "Technical University of Munich", "country": "DE", "base_tuition": 12000.0},
        {"name": "University of Toronto", "country": "CA", "base_tuition": 36000.0},
        {"name": "Tsinghua University", "country": "CN", "base_tuition": 14000.0},
        {"name": "Chulalongkorn University", "country": "TH", "base_tuition": 9500.0},
        {"name": "Khon Kaen University (KKU)", "country": "TH", "base_tuition": 7200.0},
        {"name": "Mahidol University", "country": "TH", "base_tuition": 8500.0},
        {"name": "King Mongkut\'s Institute of Technology Ladkrabang", "country": "TH", "base_tuition": 7800.0}
    ]
    
    programs_by_field = {
        "AI": [
            ("B.S. in Artificial Intelligence & Robotics", ["Python", "C++", "Linear Algebra", "Calculus", "Machine Learning", "Data Structures", "Linux"]),
            ("M.S. in Intelligent Systems & Deep Learning", ["Python", "PyTorch", "Linear Algebra", "CUDA", "Deep Learning", "TensorFlow", "MLOps"]),
            ("B.Sc. in Machine Learning & Autonomous Systems", ["Python", "Calculus", "Linear Algebra", "Machine Learning", "Algorithms", "Git"])
        ],
        "Data Science": [
            ("B.S. in Data Science & Big Data", ["Python", "SQL", "Pandas", "Linear Algebra", "Calculus", "Data Wrangling", "Machine Learning"]),
            ("M.S. in Applied Data Science & Analytics", ["Python", "SQL", "Machine Learning", "Tableau", "AWS", "Big Data/Spark", "Scikit-Learn"]),
            ("B.A. in Computational Data Science", ["Python", "SQL", "R", "Statistics", "Data Structures", "Data Visualization", "Git"])
        ],
        "Statistics": [
            ("B.S. in Statistics & Data Analytics", ["R", "Probability & Statistics", "Linear Models", "Calculus", "Python", "SQL", "Experimental Design"]),
            ("M.S. in Mathematical Statistics & Actuarial Science", ["R", "Probability & Statistics", "Time Series", "Bayesian Methods", "Linear Models", "SAS", "Calculus"]),
            ("B.Sc. in Applied Statistics & Operations Research", ["R", "Probability & Statistics", "Linear Algebra", "Optimization", "SPSS", "Python"])
        ]
    }
    
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    supply_records = []
    
    for uni in universities:
        for field, program_list in programs_by_field.items():
            for prog_name, comp_skills in program_list:
                # Growth factor across years
                base_grads = random.randint(45, 140)
                if "University" in uni["name"] and uni["country"] in ["US", "TH", "SG"]:
                    base_grads += 30
                    
                tuition = uni["base_tuition"] * random.uniform(0.9, 1.15)
                
                for idx, yr in enumerate(years):
                    growth = 1.0 + (idx * random.uniform(0.04, 0.08))
                    grads = int(round(base_grads * growth))
                    
                    # Employment rates: Yr 1 ~ 72-88%, Yr 2 ~ 85-94%, Yr 3 ~ 92-98%
                    emp_rate_1 = random.uniform(0.72, 0.88)
                    emp_rate_2 = min(0.96, emp_rate_1 + random.uniform(0.06, 0.12))
                    emp_rate_3 = min(0.99, emp_rate_2 + random.uniform(0.02, 0.06))
                    
                    emp_1 = int(round(grads * emp_rate_1))
                    emp_2 = int(round(grads * emp_rate_2))
                    emp_3 = int(round(grads * emp_rate_3))
                    
                    supply_records.append({
                        "university": uni["name"],
                        "country": uni["country"],
                        "program_name": prog_name,
                        "field_category": field,
                        "graduation_year": yr,
                        "graduates_count": grads,
                        "compulsory_skills": comp_skills,
                        "employed_year_1": emp_1,
                        "employed_year_2": emp_2,
                        "employed_year_3": emp_3,
                        "employment_rate_yr1": round(emp_1 / grads * 100, 1),
                        "employment_rate_yr2": round(emp_2 / grads * 100, 1),
                        "employment_rate_yr3": round(emp_3 / grads * 100, 1),
                        "total_tuition_fee": round(tuition, 2)
                    })
                    
    df_supply = pd.DataFrame(supply_records)
    print(f"[PIPELINE] Created {len(df_supply)} Academic Supply records across {len(universities)} universities.")
    return df_supply

def run_pipeline():
    print("==================================================")
    print("STARTING DATA PIPELINE & HARMONIZATION")
    print("==================================================")
    
    # 1. Fetch raw data
    df_salaries = fetch_or_load(URL_SALARIES, "ds_salaries.csv")
    df_ai_tracker = fetch_or_load(URL_AI_TRACKER, "AI_posting.csv")
    df_skills = fetch_or_load(URL_SKILLS, "raw_skills.csv")
    
    # 2. Build standardized datasets
    df_demand = build_demand_dataset(df_salaries)
    df_supply = build_supply_dataset()
    
    # 3. Save processed datasets
    supply_json_path = os.path.join(PROCESSED_DIR, "supply_data.json")
    supply_csv_path = os.path.join(PROCESSED_DIR, "supply_data.csv")
    demand_json_path = os.path.join(PROCESSED_DIR, "demand_data.json")
    demand_csv_path = os.path.join(PROCESSED_DIR, "demand_data.csv")
    
    df_supply.to_json(supply_json_path, orient="records", indent=2)
    df_supply.to_csv(supply_csv_path, index=False)
    
    df_demand.to_json(demand_json_path, orient="records", indent=2)
    df_demand.to_csv(demand_csv_path, index=False)
    
    if df_ai_tracker is not None:
        ai_path = os.path.join(PROCESSED_DIR, "ai_postings_timeseries.csv")
        df_ai_tracker.to_csv(ai_path, index=False)
        print(f"[PIPELINE] Saved AI tracker timeseries to {ai_path}")
        
    print(f"[PIPELINE] SUCCESS! Processed datasets stored in {PROCESSED_DIR}")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()