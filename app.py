"""
Educational Supply vs. Labor Market Demand Dashboard (AI, Data Science, Statistics)
Interactive Dash application implementing BRD and Handoff specifications.
"""

import os
import json
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_data():
    supply_path = os.path.join(DATA_DIR, "supply_data.json")
    demand_path = os.path.join(DATA_DIR, "demand_data.json")
    ai_ts_path = os.path.join(DATA_DIR, "ai_postings_timeseries.csv")
    
    if not os.path.exists(supply_path):
        supply_path = os.path.join(DATA_DIR, "supply_data.csv")
    if not os.path.exists(demand_path):
        demand_path = os.path.join(DATA_DIR, "demand_data.csv")
        
    df_supply = pd.read_json(supply_path) if supply_path.endswith(".json") else pd.read_csv(supply_path)
    df_demand = pd.read_json(demand_path) if demand_path.endswith(".json") else pd.read_csv(demand_path)
    df_ai_ts = pd.read_csv(ai_ts_path) if os.path.exists(ai_ts_path) else pd.DataFrame()
    return df_supply, df_demand, df_ai_ts

df_supply_raw, df_demand_raw, df_ai_ts_raw = load_data()

DARK_TEMPLATE = "plotly_dark"
COLOR_BG = "#0f172a"
COLOR_CARD = "#1e293b"
COLOR_BORDER = "#334155"
COLOR_CYAN = "#06b6d4"
COLOR_TEAL = "#14b8a6"
COLOR_BLUE = "#3b82f6"
COLOR_AMBER = "#f59e0b"
COLOR_EMERALD = "#10b981"
COLOR_PURPLE = "#a855f7"
COLOR_TEXT = "#f8fafc"
COLOR_MUTED = "#94a3b8"

def apply_chart_theme(fig, height=380, title=None):
    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLOR_TEXT, size=12),
        margin=dict(l=45, r=25, t=50 if title else 25, b=45),
        height=height,
        title=dict(text=title, font=dict(size=14, color=COLOR_TEXT, family="Inter")) if title else None,
        hoverlabel=dict(bgcolor=COLOR_CARD, bordercolor=COLOR_BORDER, font=dict(color=COLOR_TEXT, family="Inter")),
        xaxis=dict(gridcolor="rgba(51, 65, 85, 0.4)", zerolinecolor=COLOR_BORDER),
        yaxis=dict(gridcolor="rgba(51, 65, 85, 0.4)", zerolinecolor=COLOR_BORDER)
    )
    return fig

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    title="AIDSST Supply vs Demand Dashboard",
    suppress_callback_exceptions=True
)
server = app.server

def make_kpi_card(card_id, title, value, subtext, icon_class, border_color=COLOR_CYAN):
    return dbc.Col(
        html.Div(
            [
                html.Div(
                    [
                        html.Span(title, className="kpi-title"),
                        html.I(className=f"{icon_class} text-muted", style={"fontSize": "1.2rem", "color": border_color})
                    ],
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}
                ),
                html.Div(value, id=f"kpi-{card_id}-val", className="kpi-value"),
                html.Div(subtext, id=f"kpi-{card_id}-sub", className="kpi-sub")
            ],
            className="kpi-card",
            style={"borderLeft": f"4px solid {border_color}"}
        ),
        xs=12, sm=6, md=3, className="mb-3"
    )

def make_section_header(title, badge_text):
    return html.Div(
        [
            html.H4(title, className="section-title"),
            html.Span(badge_text, className="section-tag")
        ],
        className="section-header"
    )
app.layout = html.Div(
    [
        html.Div(
            [
                dbc.Container(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(className="fa-solid fa-chart-network fa-2x me-3", style={"color": COLOR_CYAN}),
                                        html.Div(
                                            [
                                                html.H2("Educational Supply vs. Labor Market Demand", className="m-0 fw-bold", style={"color": COLOR_TEXT, "fontSize": "1.6rem"}),
                                                html.Span("AI, Data Science & Statistics (AIDSST) Career & Higher Ed Intelligence Platform", style={"color": COLOR_MUTED, "fontSize": "0.9rem"})
                                            ]
                                        )
                                    ],
                                    style={"display": "flex", "alignItems": "center"}
                                ),
                                html.Div(
                                    [
                                        dbc.Badge("Python 3.12", color="dark", className="me-2 px-2 py-1 border border-secondary"),
                                        dbc.Badge("Dash & Plotly", color="info", className="me-2 px-2 py-1"),
                                        dbc.Badge("Live Cross-Filtering", color="success", className="px-2 py-1")
                                    ],
                                    className="d-none d-md-flex align-items-center"
                                )
                            ],
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "padding": "16px 0"}
                        )
                    ],
                    fluid=True,
                    style={"maxWidth": "1500px"}
                )
            ],
            style={"background": "#09101d", "borderBottom": f"1px solid {COLOR_BORDER}", "marginBottom": "20px"}
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        make_kpi_card("salary", "Global Median Salary", "$118,500", "Across filtered roles", "fa-solid fa-sack-dollar", COLOR_CYAN),
                        make_kpi_card("openings", "Tracked Job Openings", "1,842", "Active listings index", "fa-solid fa-briefcase", COLOR_TEAL),
                        make_kpi_card("skill", "Top In-Demand Skill", "Python", "84.2% mention share", "fa-solid fa-code", COLOR_AMBER),
                        make_kpi_card("grads", "Annual Grad Growth", "+14.6%", "YoY STEM supply index", "fa-solid fa-graduation-cap", COLOR_EMERALD)
                    ],
                    className="mb-3"
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Field Category", className="fw-semibold text-light mb-1", style={"fontSize": "0.85rem"}),
                                        dcc.Dropdown(
                                            id="filter-field",
                                            options=[
                                                {"label": "All Fields (AI, Data Science, Stat)", "value": "ALL"},
                                                {"label": "Artificial Intelligence (AI)", "value": "AI"},
                                                {"label": "Data Science", "value": "Data Science"},
                                                {"label": "Statistics", "value": "Statistics"}
                                            ],
                                            value="ALL",
                                            clearable=False,
                                            className="text-dark"
                                        )
                                    ],
                                    xs=12, sm=6, md=3, className="mb-2"
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Experience Level", className="fw-semibold text-light mb-1", style={"fontSize": "0.85rem"}),
                                        dcc.Dropdown(
                                            id="filter-exp",
                                            options=[
                                                {"label": "All Experience Levels", "value": "ALL"},
                                                {"label": "Entry Level (0-2 Yrs / EN)", "value": "EN"},
                                                {"label": "Mid-Level (2-5 Yrs / MI)", "value": "MI"},
                                                {"label": "Senior Level (5+ Yrs / SE)", "value": "SE"},
                                                {"label": "Executive / Director (EX)", "value": "EX"}
                                            ],
                                            value="ALL",
                                            clearable=False,
                                            className="text-dark"
                                        )
                                    ],
                                    xs=12, sm=6, md=2, className="mb-2"
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Country / Region", className="fw-semibold text-light mb-1", style={"fontSize": "0.85rem"}),
                                        dcc.Dropdown(
                                            id="filter-country",
                                            options=[
                                                {"label": "Global (All Locations)", "value": "ALL"},
                                                {"label": "United States (US)", "value": "US"},
                                                {"label": "Thailand (TH)", "value": "TH"},
                                                {"label": "Singapore (SG)", "value": "SG"},
                                                {"label": "Germany (DE)", "value": "DE"},
                                                {"label": "United Kingdom (GB)", "value": "GB"},
                                                {"label": "Japan (JP)", "value": "JP"},
                                                {"label": "Canada (CA)", "value": "CA"}
                                            ],
                                            value="ALL",
                                            clearable=False,
                                            className="text-dark"
                                        )
                                    ],
                                    xs=12, sm=6, md=2, className="mb-2"
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Graduation & Posting Year Range", className="fw-semibold text-light mb-1", style={"fontSize": "0.85rem"}),
                                        dcc.RangeSlider(
                                            id="filter-year-slider",
                                            min=2020,
                                            max=2026,
                                            step=1,
                                            value=[2020, 2026],
                                            marks={yr: {"label": str(yr), "style": {"color": COLOR_MUTED, "fontSize": "0.8rem"}} for yr in range(2020, 2027)}
                                        )
                                    ],
                                    xs=12, sm=12, md=3, className="mb-2"
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Export Data", className="fw-semibold text-light mb-1", style={"fontSize": "0.85rem", "visibility": "hidden"}),
                                        html.Button(
                                            [html.I(className="fa-solid fa-download me-2"), "Export CSV"],
                                            id="btn-export-csv",
                                            className="btn-export w-100 py-2",
                                            style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
                                        ),
                                        dcc.Download(id="download-csv-target")
                                    ],
                                    xs=12, sm=6, md=2, className="mb-2"
                                )
                            ],
                            align="center"
                        )
                    ],
                    className="filter-container"
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(label="Tab 1: Supply Side (Academic Programs & Graduates)", tab_id="tab-1", label_class_name="fw-bold"),
                        dbc.Tab(label="Tab 2: Demand Side (Labor Market & Hiring Trends)", tab_id="tab-2", label_class_name="fw-bold"),
                        dbc.Tab(label="Tab 3: Gap Analysis (Skill Mismatch & Educational ROI)", tab_id="tab-3", label_class_name="fw-bold")
                    ],
                    id="tabs-main",
                    active_tab="tab-1"
                ),
                html.Div(id="tab-content", className="mt-3 mb-5")
            ],
            fluid=True,
            style={"maxWidth": "1500px"}
        ),
        html.Div(
            [
                dbc.Container(
                    [
                        html.Div(
                            [
                                html.Span("Educational Supply vs. Labor Market Demand Intelligence Platform • Antigravity AI Dashboard", style={"color": COLOR_MUTED, "fontSize": "0.85rem"}),
                                html.Span("Data sources: IPEDS, UNESCO, Indeed Hiring Lab, Kaggle, BLS", style={"color": "#64748b", "fontSize": "0.80rem"})
                            ],
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "padding": "16px 0"}
                        )
                    ],
                    fluid=True,
                    style={"maxWidth": "1500px"}
                )
            ],
            style={"background": "#09101d", "borderTop": f"1px solid {COLOR_BORDER}", "marginTop": "40px"}
        )
    ]
)

def filter_supply_df(df, field, year_range, country, university="ALL"):
    d = df.copy()
    if field != "ALL":
        d = d[d["field_category"] == field]
    if country != "ALL":
        d = d[d["country"] == country]
    if university != "ALL":
        d = d[d["university"] == university]
    d = d[(d["graduation_year"] >= year_range[0]) & (d["graduation_year"] <= year_range[1])]
    return d

def filter_demand_df(df, field, exp, year_range, country, company="ALL"):
    d = df.copy()
    if field != "ALL":
        d = d[d["field_category"] == field]
    if exp != "ALL":
        d = d[d["experience_level"] == exp]
    if country != "ALL":
        d = d[d["company_location"] == country]
    if company != "ALL":
        d = d[d["company_name"] == company]
    d = d[(d["posting_year"] >= year_range[0]) & (d["posting_year"] <= year_range[1])]
    return d
def render_tab_1(df_supply):
    unis = sorted(df_supply["university"].unique().tolist())
    uni_options = [{"label": "All Universities", "value": "ALL"}] + [{"label": u, "value": u} for u in unis]
    
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Span("Filter by University (Cross-filter):", className="fw-semibold text-light me-3"),
                                dcc.Dropdown(
                                    id="tab1-filter-uni",
                                    options=uni_options,
                                    value="ALL",
                                    clearable=False,
                                    className="text-dark",
                                    style={"minWidth": "320px"}
                                )
                            ],
                            style={"display": "flex", "alignItems": "center"}
                        ),
                        xs=12, md=8, className="mb-3"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("1. Graduation Volume Trends (YoY)", "Time-Series Output"),
                                dcc.Graph(id="chart-supply-trends", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=7, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("2. Curriculum Compulsory Skills Matrix", "Curriculum Analysis"),
                                dcc.Graph(id="chart-supply-skills-matrix", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=5, className="mb-4"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("3. Employment Success Rate Over Time", "Post-Graduation Careers"),
                                dcc.Graph(id="chart-supply-employment", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=6, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("4. Tuition Fee vs. Graduate Volume Comparison", "Economics & Scale"),
                                dcc.Graph(id="chart-supply-tuition", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=6, className="mb-4"
                    )
                ]
            )
        ]
    )

def render_tab_2(df_demand):
    comps = sorted(df_demand["company_name"].unique().tolist())
    comp_options = [{"label": "All Companies", "value": "ALL"}] + [{"label": c, "value": c} for c in comps]
    
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Span("Filter by Company (Cross-filter):", className="fw-semibold text-light me-3"),
                                dcc.Dropdown(
                                    id="tab2-filter-company",
                                    options=comp_options,
                                    value="ALL",
                                    clearable=False,
                                    className="text-dark",
                                    style={"minWidth": "320px"}
                                )
                            ],
                            style={"display": "flex", "alignItems": "center"}
                        ),
                        xs=12, md=8, className="mb-3"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("1. Job Vacancies & Indeed AI Postings Index", "Hiring Momentum"),
                                dcc.Graph(id="chart-demand-openings-trend", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=7, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("2. Top Demanded Skills Frequency", "Market Skill Ranking"),
                                dcc.Graph(id="chart-demand-skills-rank", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=5, className="mb-4"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("3. Global Hiring & Salary Geographic Map", "Geographic Density"),
                                dcc.Graph(id="chart-demand-geo-map", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=7, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("4. Salary Distribution by Career Level", "Compensation Tiers"),
                                dcc.Graph(id="chart-demand-salary-dist", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=5, className="mb-4"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("5. Top Hiring Companies & Industry Sectors", "Employer Concentration"),
                                dcc.Graph(id="chart-demand-companies-treemap", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=12, className="mb-4"
                    )
                ]
            )
        ]
    )

def render_tab_3():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("1. Dynamic Supply vs. Demand Skill Gap Matrix", "Mismatch Delta (Demand % - Supply %)"),
                                dcc.Graph(id="chart-gap-diverging", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=7, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("2. Critical Shortage vs. Excess Skills Summary", "Talent Imbalance"),
                                html.Div(id="gap-summary-cards-container")
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=5, className="mb-4"
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("3. Tuition Fee vs. Entry-Level Salary ROI Index", "Payback & Economic Value"),
                                dcc.Graph(id="chart-gap-roi-scatter", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=6, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                make_section_header("4. Career Progression & Entry Qualifications Flow", "Degree to Salary Pathways"),
                                dcc.Graph(id="chart-gap-career-pathways", config={"displayModeBar": True})
                            ],
                            className="dash-card"
                        ),
                        xs=12, lg=6, className="mb-4"
                    )
                ]
            )
        ]
    )
@app.callback(
    Output("tab-content", "children"),
    Input("tabs-main", "active_tab")
)
def switch_tabs(active_tab):
    if active_tab == "tab-1":
        return render_tab_1(df_supply_raw)
    elif active_tab == "tab-2":
        return render_tab_2(df_demand_raw)
    else:
        return render_tab_3()

@app.callback(
    [
        Output("kpi-salary-val", "children"),
        Output("kpi-salary-sub", "children"),
        Output("kpi-openings-val", "children"),
        Output("kpi-openings-sub", "children"),
        Output("kpi-skill-val", "children"),
        Output("kpi-skill-sub", "children"),
        Output("kpi-grads-val", "children"),
        Output("kpi-grads-sub", "children")
    ],
    [
        Input("filter-field", "value"),
        Input("filter-exp", "value"),
        Input("filter-country", "value"),
        Input("filter-year-slider", "value")
    ]
)
def update_kpi_cards(field, exp, country, year_range):
    df_d = filter_demand_df(df_demand_raw, field, exp, year_range, country)
    df_s = filter_supply_df(df_supply_raw, field, year_range, country)
    
    if not df_d.empty and "salary_in_usd" in df_d.columns:
        med_sal = df_d["salary_in_usd"].median()
        p25 = df_d["salary_in_usd"].quantile(0.25)
        p75 = df_d["salary_in_usd"].quantile(0.75)
        sal_val = f"${med_sal:,.0f}"
        sal_sub = f"IQR: ${p25/1000:.0f}k - ${p75/1000:.0f}k (N={len(df_d):,})"
    else:
        sal_val = "N/A"
        sal_sub = "No matching records"
        
    if not df_d.empty:
        openings = int(df_d["vacancies_count"].sum())
        open_val = f"{openings:,}"
        open_sub = f"Across {df_d['company_name'].nunique()} hiring companies"
    else:
        open_val = "0"
        open_sub = "No active listings"
        
    all_skills = []
    if not df_d.empty:
        for sk_list in df_d["required_skills"]:
            if isinstance(sk_list, list):
                all_skills.extend(sk_list)
        if all_skills:
            sk_counts = pd.Series(all_skills).value_counts()
            top_sk = sk_counts.index[0]
            top_sk_pct = (sk_counts.iloc[0] / len(df_d)) * 100
            sk_val = f"{top_sk}"
            sk_sub = f"{top_sk_pct:.1f}% of postings require this"
        else:
            sk_val = "Python"
            sk_sub = "Default baseline"
    else:
        sk_val = "N/A"
        sk_sub = "No listings"
        
    if not df_s.empty:
        total_grads = df_s["graduates_count"].sum()
        grads_by_yr = df_s.groupby("graduation_year")["graduates_count"].sum()
        if len(grads_by_yr) >= 2:
            y_first = grads_by_yr.iloc[0]
            y_last = grads_by_yr.iloc[-1]
            growth = ((y_last - y_first) / y_first) * 100 if y_first > 0 else 0
            grads_val = f"{total_grads:,}"
            grads_sub = f"+{growth:.1f}% aggregate expansion"
        else:
            grads_val = f"{total_grads:,}"
            grads_sub = f"{len(df_s)} degree batches"
    else:
        grads_val = "0"
        grads_sub = "No academic records"
        
    return sal_val, sal_sub, open_val, open_sub, sk_val, sk_sub, grads_val, grads_sub

@app.callback(
    [
        Output("chart-supply-trends", "figure"),
        Output("chart-supply-skills-matrix", "figure"),
        Output("chart-supply-employment", "figure"),
        Output("chart-supply-tuition", "figure")
    ],
    [
        Input("filter-field", "value"),
        Input("filter-country", "value"),
        Input("filter-year-slider", "value"),
        Input("tab1-filter-uni", "value")
    ]
)
def update_tab1_charts(field, country, year_range, university):
    df_s = filter_supply_df(df_supply_raw, field, year_range, country, university)
    
    if df_s.empty:
        empty_fig = apply_chart_theme(go.Figure().add_annotation(text="No Supply Data Matching Filters", showarrow=False, font=dict(size=14, color=COLOR_MUTED)))
        return empty_fig, empty_fig, empty_fig, empty_fig
        
    trend_data = df_s.groupby(["graduation_year", "field_category"])["graduates_count"].sum().reset_index()
    fig_trends = px.area(
        trend_data,
        x="graduation_year",
        y="graduates_count",
        color="field_category",
        color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
    )
    fig_trends.update_layout(xaxis_title="Graduation Year", yaxis_title="Total Graduates Produced", legend_title="Discipline", hovermode="x unified")
    apply_chart_theme(fig_trends)
    
    skills_expanded = []
    for _, row in df_s.iterrows():
        skills = row.get("compulsory_skills", [])
        if isinstance(skills, list):
            for s in skills:
                skills_expanded.append({"skill": s, "field": row["field_category"]})
    df_sk = pd.DataFrame(skills_expanded)
    
    if not df_sk.empty:
        top_skills = df_sk["skill"].value_counts().head(10).index.tolist()
        skill_counts = df_sk[df_sk["skill"].isin(top_skills)].groupby(["skill", "field"]).size().reset_index(name="count")
        
        fig_skills = px.bar(
            skill_counts,
            y="skill",
            x="count",
            color="field",
            orientation="h",
            color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
        )
        fig_skills.update_layout(yaxis=dict(categoryorder="total ascending"), xaxis_title="Programs Requiring Skill", yaxis_title="")
    else:
        fig_skills = go.Figure()
    apply_chart_theme(fig_skills)
    
    emp_by_uni = df_s.groupby("university")[["employment_rate_yr1", "employment_rate_yr2", "employment_rate_yr3"]].mean().reset_index().head(8)
    fig_emp = go.Figure()
    fig_emp.add_trace(go.Bar(name="Year 1 After Grad", x=emp_by_uni["university"], y=emp_by_uni["employment_rate_yr1"], marker_color=COLOR_CYAN))
    fig_emp.add_trace(go.Bar(name="Year 2 After Grad", x=emp_by_uni["university"], y=emp_by_uni["employment_rate_yr2"], marker_color=COLOR_TEAL))
    fig_emp.add_trace(go.Bar(name="Year 3 After Grad", x=emp_by_uni["university"], y=emp_by_uni["employment_rate_yr3"], marker_color=COLOR_EMERALD))
    fig_emp.update_layout(barmode="group", yaxis_title="Employment Rate (%)", yaxis=dict(range=[50, 100]), xaxis_tickangle=-25)
    apply_chart_theme(fig_emp)
    
    uni_summary = df_s.groupby(["university", "field_category"]).agg({
        "total_tuition_fee": "mean",
        "graduates_count": "sum",
        "employment_rate_yr3": "mean"
    }).reset_index()
    
    fig_tuition = px.scatter(
        uni_summary,
        x="total_tuition_fee",
        y="graduates_count",
        color="field_category",
        size="employment_rate_yr3",
        hover_name="university",
        color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
    )
    fig_tuition.update_layout(xaxis_title="Average Total Tuition Fee (USD $)", yaxis_title="Total Graduates Output", xaxis=dict(tickprefix="$"))
    apply_chart_theme(fig_tuition)
    
    return fig_trends, fig_skills, fig_emp, fig_tuition

@app.callback(
    [
        Output("chart-demand-openings-trend", "figure"),
        Output("chart-demand-skills-rank", "figure"),
        Output("chart-demand-geo-map", "figure"),
        Output("chart-demand-salary-dist", "figure"),
        Output("chart-demand-companies-treemap", "figure")
    ],
    [
        Input("filter-field", "value"),
        Input("filter-exp", "value"),
        Input("filter-country", "value"),
        Input("filter-year-slider", "value"),
        Input("tab2-filter-company", "value")
    ]
)
def update_tab2_charts(field, exp, country, year_range, company):
    df_d = filter_demand_df(df_demand_raw, field, exp, year_range, country, company)
    
    if df_d.empty:
        empty_fig = apply_chart_theme(go.Figure().add_annotation(text="No Demand Data Matching Filters", showarrow=False, font=dict(size=14, color=COLOR_MUTED)))
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
        
    d_trend = df_d.groupby(["posting_year", "field_category"])["vacancies_count"].sum().reset_index()
    fig_trend = px.line(
        d_trend,
        x="posting_year",
        y="vacancies_count",
        color="field_category",
        markers=True,
        color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
    )
    fig_trend.update_layout(xaxis_title="Posting Year", yaxis_title="Total Tracked Vacancies")
    apply_chart_theme(fig_trend)
    
    all_skills = []
    for _, r in df_d.iterrows():
        sks = r.get("required_skills", [])
        if isinstance(sks, list):
            for s in sks:
                all_skills.append({"skill": s, "field": r["field_category"]})
    df_sk = pd.DataFrame(all_skills)
    
    if not df_sk.empty:
        top_names = df_sk["skill"].value_counts().head(12).index.tolist()
        sk_rank = df_sk[df_sk["skill"].isin(top_names)].groupby(["skill", "field"]).size().reset_index(name="mentions")
        fig_skills = px.bar(
            sk_rank,
            y="skill",
            x="mentions",
            color="field",
            orientation="h",
            color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
        )
        fig_skills.update_layout(yaxis=dict(categoryorder="total ascending"), xaxis_title="Job Ads Demanding Skill", yaxis_title="")
    else:
        fig_skills = go.Figure()
    apply_chart_theme(fig_skills)
    
    geo_data = df_d.groupby("company_location").agg({
        "salary_in_usd": "median",
        "vacancies_count": "sum"
    }).reset_index()
    iso2_to_iso3 = {"US": "USA", "GB": "GBR", "DE": "DEU", "TH": "THA", "SG": "SGP", "JP": "JPN", "CA": "CAN", "IN": "IND", "AU": "AUS", "FR": "FRA", "CH": "CHE", "CN": "CHN"}
    geo_data["iso3"] = geo_data["company_location"].map(iso2_to_iso3).fillna("USA")
    
    fig_map = px.choropleth(
        geo_data,
        locations="iso3",
        color="salary_in_usd",
        hover_name="company_location",
        hover_data={"salary_in_usd": ":$,.0f", "vacancies_count": ":,", "iso3": False},
        color_continuous_scale="Tealgrn"
    )
    fig_map.update_geos(showcoastlines=True, coastlinecolor=COLOR_BORDER, showland=True, landcolor="#1e293b", bgcolor="rgba(0,0,0,0)", lakecolor="#0f172a")
    fig_map.update_layout(coloraxis_colorbar=dict(title="Median Pay ($)", tickprefix="$"), margin=dict(l=0, r=0, t=10, b=10))
    apply_chart_theme(fig_map)
    
    fig_box = px.box(
        df_d,
        x="experience_level",
        y="salary_in_usd",
        color="field_category",
        category_orders={"experience_level": ["EN", "MI", "SE", "EX"]},
        color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
    )
    fig_box.update_layout(xaxis_title="Experience Level", yaxis_title="Salary (USD $)", yaxis=dict(tickprefix="$"), boxmode="group")
    apply_chart_theme(fig_box)
    
    comp_data = df_d.groupby(["company_name", "industry_sector"])["vacancies_count"].sum().reset_index().sort_values(by="vacancies_count", ascending=False).head(12)
    fig_comp = px.bar(
        comp_data,
        x="company_name",
        y="vacancies_count",
        color="industry_sector",
        color_discrete_sequence=[COLOR_CYAN, COLOR_TEAL, COLOR_BLUE, COLOR_PURPLE, COLOR_AMBER]
    )
    fig_comp.update_layout(xaxis_title="Company Name", yaxis_title="Open Vacancies", xaxis_tickangle=-25)
    apply_chart_theme(fig_comp, height=320)
    
    return fig_trend, fig_skills, fig_map, fig_box, fig_comp

@app.callback(
    [
        Output("chart-gap-diverging", "figure"),
        Output("gap-summary-cards-container", "children"),
        Output("chart-gap-roi-scatter", "figure"),
        Output("chart-gap-career-pathways", "figure")
    ],
    [
        Input("filter-field", "value"),
        Input("filter-exp", "value"),
        Input("filter-country", "value"),
        Input("filter-year-slider", "value")
    ]
)
def update_tab3_gap_analysis(field, exp, country, year_range):
    df_d = filter_demand_df(df_demand_raw, field, exp, year_range, country)
    df_s = filter_supply_df(df_supply_raw, field, year_range, country)
    
    if df_d.empty or df_s.empty:
        empty_fig = apply_chart_theme(go.Figure().add_annotation(text="Insufficient Data for Gap Analysis", showarrow=False, font=dict(size=14, color=COLOR_MUTED)))
        return empty_fig, html.Div("No data available"), empty_fig, empty_fig
        
    demand_skill_counts = {}
    for sks in df_d["required_skills"]:
        if isinstance(sks, list):
            for s in set(sks):
                demand_skill_counts[s] = demand_skill_counts.get(s, 0) + 1
    total_postings = len(df_d)
    demand_pct = {k: (v / total_postings) * 100 for k, v in demand_skill_counts.items()}
    
    supply_skill_counts = {}
    prog_df = df_s.drop_duplicates(subset=["university", "program_name"])
    total_programs = len(prog_df)
    for sks in prog_df["compulsory_skills"]:
        if isinstance(sks, list):
            for s in set(sks):
                supply_skill_counts[s] = supply_skill_counts.get(s, 0) + 1
    supply_pct = {k: (v / total_programs) * 100 for k, v in supply_skill_counts.items()}
    
    all_keys = set(demand_pct.keys()).union(set(supply_pct.keys()))
    gap_records = []
    for k in all_keys:
        d_val = demand_pct.get(k, 0.0)
        s_val = supply_pct.get(k, 0.0)
        delta = d_val - s_val
        gap_records.append({
            "skill": k,
            "demand_pct": round(d_val, 1),
            "supply_pct": round(s_val, 1),
            "gap_delta": round(delta, 1),
            "status": "Shortage (Industry Deficit)" if delta > 0 else "Surplus (Academic Excess)"
        })
    df_gap = pd.DataFrame(gap_records).sort_values(by="gap_delta", ascending=True)
    
    colors = [COLOR_AMBER if g > 0 else COLOR_TEAL for g in df_gap["gap_delta"]]
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        y=df_gap["skill"],
        x=df_gap["gap_delta"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"{v:+.1f}%" for v in df_gap["gap_delta"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Skill Gap Delta: %{x:+.1f}%<extra></extra>"
    ))
    fig_gap.update_layout(
        xaxis_title="Skill Gap Delta (%)  [ + Deficit in Academia  |  - Surplus in Academia ]",
        yaxis_title="",
        xaxis=dict(zeroline=True, zerolinecolor="#64748b", zerolinewidth=2)
    )
    apply_chart_theme(fig_gap, height=420)
    
    top_shortages = df_gap[df_gap["gap_delta"] > 0].sort_values(by="gap_delta", ascending=False).head(3)
    top_excess = df_gap[df_gap["gap_delta"] < 0].sort_values(by="gap_delta", ascending=True).head(3)
    
    cards_html = html.Div(
        [
            html.Div(
                [
                    html.H6("🚨 Critical Shortage Skills (High Market Demand, Low Curriculum)", style={"color": COLOR_AMBER, "fontWeight": "700"}),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                [
                                    html.Span(row["skill"], className="fw-bold text-light"),
                                    dbc.Badge(f"+{row['gap_delta']:.1f}% deficit", color="warning", className="ms-auto")
                                ],
                                style={"background": "rgba(245, 158, 11, 0.12)", "border": "1px solid rgba(245, 158, 11, 0.3)", "display": "flex", "alignItems": "center", "marginBottom": "6px", "borderRadius": "6px"}
                            ) for _, row in top_shortages.iterrows()
                        ],
                        flush=True
                    )
                ],
                className="mb-3"
            ),
            html.Div(
                [
                    html.H6("✅ Excess / Well-Covered Academic Skills (High Curriculum Coverage)", style={"color": COLOR_TEAL, "fontWeight": "700"}),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                [
                                    html.Span(row["skill"], className="fw-bold text-light"),
                                    dbc.Badge(f"{row['gap_delta']:.1f}% excess", color="info", className="ms-auto")
                                ],
                                style={"background": "rgba(20, 184, 166, 0.12)", "border": "1px solid rgba(20, 184, 166, 0.3)", "display": "flex", "alignItems": "center", "marginBottom": "6px", "borderRadius": "6px"}
                            ) for _, row in top_excess.iterrows()
                        ],
                        flush=True
                    )
                ]
            )
        ]
    )
    
    entry_sals = df_d[df_d["experience_level"] == "EN"].groupby("field_category")["salary_in_usd"].median().to_dict()
    uni_roi = df_s.groupby(["university", "field_category"]).agg({
        "total_tuition_fee": "mean",
        "employment_rate_yr1": "mean"
    }).reset_index()
    uni_roi["entry_salary"] = uni_roi["field_category"].map(entry_sals).fillna(72000.0)
    uni_roi["payback_ratio"] = uni_roi["entry_salary"] / uni_roi["total_tuition_fee"]
    
    fig_roi = px.scatter(
        uni_roi,
        x="total_tuition_fee",
        y="entry_salary",
        color="field_category",
        size="employment_rate_yr1",
        hover_name="university",
        hover_data={"payback_ratio": ":.2f", "total_tuition_fee": ":$,.0f", "entry_salary": ":$,.0f"},
        color_discrete_map={"AI": COLOR_CYAN, "Data Science": COLOR_TEAL, "Statistics": COLOR_BLUE}
    )
    fig_roi.update_layout(xaxis_title="Total Degree Tuition Cost (USD $)", yaxis_title="Market Entry Starting Salary (USD $)", xaxis=dict(tickprefix="$"), yaxis=dict(tickprefix="$"))
    apply_chart_theme(fig_roi)
    
    edu_flow = df_d.groupby(["required_education", "experience_level"])["salary_in_usd"].median().reset_index()
    fig_flow = px.bar(
        edu_flow,
        x="experience_level",
        y="salary_in_usd",
        color="required_education",
        barmode="group",
        category_orders={"experience_level": ["EN", "MI", "SE", "EX"], "required_education": ["Bachelor", "Master", "PhD"]},
        color_discrete_map={"Bachelor": COLOR_CYAN, "Master": COLOR_TEAL, "PhD": COLOR_PURPLE}
    )
    fig_flow.update_layout(xaxis_title="Career Experience Level", yaxis_title="Median Salary (USD $)", yaxis=dict(tickprefix="$"), legend_title="Required Degree")
    apply_chart_theme(fig_flow)
    
    return fig_gap, cards_html, fig_roi, fig_flow

@app.callback(
    Output("download-csv-target", "data"),
    Input("btn-export-csv", "n_clicks"),
    [
        State("filter-field", "value"),
        State("filter-exp", "value"),
        State("filter-country", "value"),
        State("filter-year-slider", "value")
    ],
    prevent_initial_call=True
)
def export_filtered_csv(n_clicks, field, exp, country, year_range):
    if not n_clicks:
        return dash.no_update
    df_d = filter_demand_df(df_demand_raw, field, exp, year_range, country)
    return dcc.send_data_frame(df_d.to_csv, "filtered_aidsst_labor_demand.csv", index=False)

if __name__ == "__main__":
    print("[SERVER] Starting Educational Supply vs Demand Dashboard...")
    app.run(debug=False, host="127.0.0.1", port=8050)