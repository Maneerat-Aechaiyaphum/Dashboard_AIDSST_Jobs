# Business Requirements Document (BRD)
## Project: Educational Supply vs. Labor Market Demand Dashboard (AI, Data Science, Statistics)

---

## 1. Project Overview & Objectives

เอกสารฉบับนี้จัดทำขึ้นเพื่อกำหนดข้อกำหนดทางธุรกิจและทางเทคนิค (Business & Technical Requirements) สำหรับส่งต่อให้ **Antigravity** นำไปพัฒนา **Interactive Dashboard** ด้วย **Python Backend** และ **Plotly** 

### Key Business Questions Addressed:
1. **Supply Side (Tab 1)**: ปริมาณผู้สำเร็จการศึกษา หลักสูตร สกิลที่ได้รับการเรียนการสอน ค่าเทอม และอัตราการได้งานทำคือเท่าใด?
2. **Demand Side (Tab 2)**: ปริมาณความต้องการจ้างงาน บริษัทที่เปิดรับ ทักษะที่ต้องการในตลาด และอัตราเงินเดือนในแต่ละระดับเป็นอย่างไร?
3. **Gap Analysis (Tab 3)**: มีความเหลื่อมล้ำทางทักษะ (Skill Mismatch) ระหว่างสิ่งที่สถาบันการศึกษาผลิตกับสิ่งที่ตลาดแรงงานต้องการมากน้อยเพียงใด?

---

## 2. Technical Stack & Architecture Guidelines

* **Backend Environment**: Python 3.10+ (FastAPI / Flask / Dash Server)
* **Visualization Framework**: **Plotly / Dash** (Plotly Express, Plotly Graph Objects)
* **Data Processing**: Pandas / NumPy / Polars
* **Interactivity Requirement**: **Cross-Filtering / Linked Callbacks** ทุกกราฟภายใน Tab เดียวกันต้องเชื่อมโยงกัน เมื่อ User คลิก/กรองข้อมูลที่กราฟใด กราฟอื่นใน Tab เดียวกันจะต้องอัปเดตข้อมูลตาม (Interactive Cross-Filtering)

---

## 3. Detailed Tab Requirements

### 3.1 Tab 1: Supply Side - ปริมาณผู้สำเร็จการศึกษาและสกิลที่เรียนมา

**วัตถุประสงค์**: วิเคราะห์ฝั่งสถาบันการศึกษาและผลิตบัณฑิตในสาขา AI, Data Science และ Statistics

#### Visual Components & Features:
1. **Graduation Volume Trends by Program (Line Chart / Stacked Bar Chart)**
   * **Description**: แสดงรายชื่อหลักสูตร/มหาวิทยาลัย ที่ผลิตบัณฑิตป้อนเข้าสู่สายงาน AI, Data Science, Stat พร้อมจำนวนผู้สำเร็จการศึกษาแยกตามรายปี (Year-on-Year)
   * **Metrics**: Total Graduates Count per Year, Program Name, University.
2. **Curriculum Compulsory Skills Matrix (Heatmap / Horizontal Bar Chart)**
   * **Description**: รายวิชาบังคับของแต่ละหลักสูตรที่ตรงกับทักษะสายงาน (เช่น Python, R, Calculus, Linear Algebra, Machine Learning)
   * **Metrics**: Frequency of Required Subjects, Skill Categories covered by degree.
3. **Employment Success Rate Over Time (Grouped Bar Chart)**
   * **Description**: จำนวนบัณฑิตที่ได้งานทำสะสมแบ่งตามช่วงเวลาหลังเรียนจบ (ปีแรก, ปีที่สอง, ปีที่สาม)
   * **Metrics**: Employed Graduates Count, Time-to-Employment (Year 1, Year 2, Year 3).
4. **Tuition Fee vs. Graduate Volume Comparison (Scatter Plot / Bar Chart)**
   * **Description**: เปรียบเทียบค่าธรรมเนียมการศึกษา (ค่าเทอมตลอดหลักสูตร) ของแต่ละหลักสูตรกับจำนวนบัณฑิตที่ผลิตได้
   * **Metrics**: Total Tuition Fee (THB/USD), Average Graduate Output.

---

### 3.2 Tab 2: Demand Side - ปริมาณงานที่จ้างและ Skill ที่ต้องการ

**วัตถุประสงค์**: วิเคราะห์ฝั่งความต้องการของตลาดแรงงานและการจ้างงานจริง

#### Visual Components & Features:
1. **Job Vacancies Volume Index (KPI Cards & Time-Series Chart)**
   * **Description**: แสดงจำนวนตำแหน่งงานที่เปิดรับสมัคร (Job Vacancies) แยกตามตำแหน่ง (AI Engineer, Data Scientist, Statistician, ML Engineer)
   * **Metrics**: Total Openings, Growth Rate, Geographic Region.
2. **Top Demanded Skills Frequency (Horizontal Ranked Bar Chart)**
   * **Description**: ทักษะความรู้ Frameworks และ Tools ที่ระบุเป็นข้อกำหนดในประกาศรับสมัครงาน
   * **Metrics**: Skill Mentions Count, Percentage of Job Ads.
3. **Top Hiring Companies & Industry Sectors (Treemap / Bar Chart)**
   * **Description**: รายชื่อบริษัทและกลุ่มอุตสาหกรรมที่เปิดรับสมัครงานด้าน AI, Data Science และ Stat มากที่สุด
   * **Metrics**: Company Name, Job Count, Industry Sector.
4. **Salary Distribution by Career Level (Box Plot / Grouped Bar Chart)**
   * **Description**: ค่าตอบแทน/เงินเดือนเริ่มต้นและเฉลี่ย แบ่งตามระดับสายงาน
   * **Metrics**: Entry Level (0-2 Yrs), Mid Level (2-5 Yrs), Senior/Lead Level (5+ Yrs).

---

### 3.3 Tab 3: Gap Analysis - วิเคราะห์ Skill Mismatch

**วัตถุประสงค์**: เปรียบเทียบความแตกต่างระหว่างหลักสูตรการศึกษากับความต้องการของตลาดแรงงาน

#### Visual Components & Features:
1. **Supply vs. Demand Skill Gap Matrix (Diverging Bar Chart / Radar Chart)**
   * **Description**: เปรียบเทียบสัดส่วน % การสอนทักษะในหลักสูตร (Supply) กับ % ความต้องการทักษะในประกาศรับสมัครงาน (Demand)
   * **Metrics**: Skill Coverage Gap ($\text{Demand \%} - \text{Supply \%}$).
2. **Over-supplied vs. Under-supplied Skills List (KPI Table / Highlight Cards)**
   * **Description**: สรุปทักษะที่เป็น **Shortage Skills** (ตลาดต้องการสูง แต่หลักสูตรสอนน้อย) และ **Excess Skills** (สอนเยอะ แต่ตลาดต้องการน้อย).
3. **Tuition Fee vs. Entry Salary ROI Index (Scatter Chart)**
   * **Description**: วิเคราะห์ผลตอบแทนการศึกษา เปรียบเทียบค่าเทอมเฉลี่ยของหลักสูตรกับเงินเดือนเริ่มต้น (Entry Salary) ของสายงาน.

---

## 4. Interactivity & State Management (Cross-Filtering Logic)

Antigravity ต้องรองรับ Callback State Management ดังนี้:

* **Global Filter Bar**: Dropdown เลือก **สาขาวิชา/ตำแหน่ง (AI, Data Science, Statistics)**, **ช่วงปี (Year Range)** และ **ระดับประสบการณ์ (Experience Level)**
* **Cross-Chart Interaction**:
  * เมื่อคลิกเลือก *ชื่อหลักสูตร* ใน Tab 1 กราฟ รายวิชา, อัตราการได้งาน และค่าเทอม ต้องปรับตามหลักสูตรนั้น
  * เมื่อคลิกเลือก *ชื่อบริษัท* หรือ *ตำแหน่งงาน* ใน Tab 2 กราฟ สกิลที่ต้องการ และเงินเดือน ต้องปรับเปลี่ยนเพื่อแสดงข้อมูลเฉพาะของบริษัท/ตำแหน่งนั้น
  * ข้อมูลจาก Tab 1 และ Tab 2 ต้องถูกส่งต่อเข้า Callback Processing Loop ของ Tab 3 เพื่อประมวลผลคำนวณ Skill Mismatch แบบ Dynamic

---

## 5. Standard Data Schema Expected by Backend

```json
{
  "supply_data": [
    {
      "university": "string",
      "program_name": "string",
      "field_category": "AI | Data Science | Statistics",
      "graduation_year": "integer",
      "graduates_count": "integer",
      "compulsory_skills": ["Python", "SQL", "Math"],
      "employed_year_1": "integer",
      "employed_year_2": "integer",
      "employed_year_3": "integer",
      "total_tuition_fee": "float"
    }
  ],
  "demand_data": [
    {
      "job_id": "string",
      "company_name": "string",
      "job_title": "string",
      "field_category": "AI | Data Science | Statistics",
      "experience_level": "Entry | Mid | Senior",
      "required_skills": ["Python", "PyTorch", "Docker"],
      "salary_min": "float",
      "salary_max": "float",
      "vacancies_count": "integer"
    }
  ]
}
```

---

## 6. Action Plan for Antigravity

1. **Setup Environment**: ติดตั้ง `dash`, `plotly`, `pandas`
2. **Data Pipeline**: สร้าง Script แปลงข้อมูล Input จาก CSV/JSON ให้เข้าตาม Data Schema ในข้อ 5
3. **Build Layout & Callbacks**: สร้าง UI Component แยกตาม 3 Tabs พร้อมผูก `dash.dependencies.Input` และ `Output` เพื่อทำ Cross-Filtering
4. **Deploy Dashboard**: ทดสอบ Performance และ Interactive Updating บน Web Application