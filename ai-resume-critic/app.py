"""
AI RESUME CRITIC — TECH-ROAST
"Your Resume Applied. AI Got Ruthless."
Main Application Entry Point — Built by Avantika Shukla
"""

import os
import sys
import streamlit as st
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.session_manager import init_session_state
init_session_state()

st.set_page_config(
    page_title="AI Resume Critic — Tech-Roast",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS — Premium Dark Theme
# ============================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }

    /* ======= FIX: Material Symbols icon font fallback-text leak =======
       Streamlit renders its own native icons (expander arrows, chevrons,
       tooltips, etc.) as <span data-testid="stIconMaterial">icon_name</span>
       and relies on the "Material Symbols Rounded" web font to turn that
       ligature text into a glyph. When that font fails to load in a given
       deployment/network environment, the browser falls back to showing
       the RAW TEXT ("arrow_right", "keyboard_arrow_down", etc.) instead —
       which is exactly the overlapping text seen on this app's custom
       expander buttons. This is a confirmed, documented Streamlit issue
       (see discuss.streamlit.io "st.expander _arrow_ issue"). The old CSS
       below (targeting .stArrowIcon / svg[data-testid="stArrowIcon"] /
       [class*="arrow"]) used selectors that don't match current Streamlit
       markup at all, which is why it never actually worked. This is the
       correct, current selector and it's applied globally so the bug can
       never leak text anywhere in the app again, regardless of which
       native widget triggers it. */
    span[data-testid="stIconMaterial"] {
        font-size: 0 !important;
        line-height: 0 !important;
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        min-height: 0 !important;
        overflow: hidden !important;
        display: inline-block !important;
        visibility: hidden !important;
    }

    .main .block-container { padding-top: 1.5rem; max-width: 1440px; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; height: 0 !important; }
    .stDeployButton { display: none !important; }

    /* ======= SIDEBAR ======= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F0F1A 0%, #1A1A2E 100%) !important;
        border-right: 1px solid #2D2D44;
        min-width: 280px !important;
        max-width: 300px !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div { color: #E2E8F0; }

    /* Remove Streamlit sidebar collapse button */
    button[kind="header"],
    [aria-label="Collapse sidebar"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarNavLink"] {
        display: none !important;
    }
    /* Remove raw icon text like "keyboard_double_arrow_left" */
    [data-testid="stSidebar"] > div > div > button,
    [data-testid="stSidebar"] button[title] {
        display: none !important;
    }
    /* Remove the Streamlit sidebar nav section completely */
    [data-testid="stSidebarNavContainer"],
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ======= EXPANDERS ======= */
    /* Remove native details marker */
    [data-testid="stExpander"] details summary::-webkit-details-marker,
    [data-testid="stExpander"] details summary::marker { display: none !important; content: '' !important; }
    [data-testid="stExpander"] details summary { list-style: none !important; }

    /* Hide arrow icon — target every possible selector Streamlit versions use */
    [data-testid="stExpander"] summary > div > :first-child,
    [data-testid="stExpander"] details > summary > div > :first-child,
    [data-testid="stExpander"] .stArrowIcon,
    [data-testid="stExpander"] svg[data-testid="stArrowIcon"],
    [data-testid="stExpander"] [class*="arrow"],
    [data-testid="stExpander"] [class*="Arrow"],
    [data-testid="stExpander"] [data-testid*="Arrow"] {
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        font-size: 0 !important;
        line-height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    /* Prevent any text leaking from hidden arrow elements */
    [data-testid="stExpander"] summary > div > :first-child::before,
    [data-testid="stExpander"] summary > div > :first-child::after { content: none !important; }

    /* ======= FILE UPLOADER ======= */
    [data-testid="stFileUploader"] button[data-testid="stFileUploadButton"] span,
    [data-testid="stFileUploader"] .stFileUploadButton span { 
        display: block !important; 
        text-overflow: ellipsis; 
        overflow: hidden; 
        white-space: nowrap;
    }
    [data-testid="stFileUploader"] section[data-testid="stFileUploadDropzone"] { 
        border-radius: 14px !important;
        border-color: #2D2D44 !important;
        background: #141425 !important;
    }
    [data-testid="stFileUploader"] section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #7C3AED !important;
    }
    [data-testid="stFileUploader"] p { color: #94A3B8 !important; }

    /* ======= TEXT FIXES ======= */
 h1, h2, h3, h4, h5, h6, p, span, li {
        overflow-wrap: break-word;
        word-wrap: break-word;
        line-height: 1.6;
    }

    .nav-btn {
        display: flex; align-items: center; gap: 10px;
        width: 100%; padding: 12px 16px; border-radius: 12px;
        background: transparent; border: 1px solid transparent;
        color: #CBD5E1; font-size: 0.92em; font-weight: 500;
        cursor: pointer; transition: all 0.2s ease; text-align: left;
    }
    .nav-btn:hover {
        background: rgba(124, 58, 237, 0.12); border-color: rgba(124, 58, 237, 0.3);
        color: #E2E8F0; transform: translateX(4px);
    }
    .nav-btn.active {
        background: rgba(124, 58, 237, 0.2); border-color: #7C3AED;
        color: #A78BFA; font-weight: 600;
    }
    .nav-btn .nav-icon { font-size: 1.2em; min-width: 28px; text-align: center; }
    .nav-btn .nav-label { flex: 1; }

    .hero-title {
        font-size: 3.2em; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 40%, #C4B5FD 70%, #DDD6FE 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px;
    }
    .hero-sub {
        text-align: center; color: #94A3B8; font-size: 1.15em;
        font-style: italic; margin-bottom: 8px;
    }
    .hero-desc {
        text-align: center; color: #64748B; font-size: 0.95em;
        max-width: 600px; margin: 0 auto 28px; line-height: 1.6;
    }

    .cta-row { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 36px; }

    .cta-btn {
        padding: 14px 32px; border-radius: 14px; font-size: 1em;
        font-weight: 700; cursor: pointer; transition: all 0.25s ease;
        border: none; display: flex; align-items: center; gap: 8px;
    }
    .cta-primary {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
        color: white; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    .cta-primary:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5); }
    .cta-secondary {
        background: rgba(124, 58, 237, 0.1); color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.3);
    }
    .cta-secondary:hover { background: rgba(124, 58, 237, 0.2); transform: translateY(-3px); }

    .features-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 20px; margin-top: 24px;
    }
    @media (max-width: 900px) { .features-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .features-grid { grid-template-columns: 1fr; } }

    .feature-card {
        background: linear-gradient(145deg, #1A1A2E 0%, #141425 100%);
        border: 1px solid #2D2D44; border-radius: 18px;
        padding: 28px 20px; text-align: center; cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative; overflow: hidden;
    }
    .feature-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #7C3AED, #A78BFA); opacity: 0;
        transition: opacity 0.3s ease;
    }
    .feature-card:hover {
        border-color: #7C3AED; transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(124, 58, 237, 0.2);
    }
    .feature-card:hover::before { opacity: 1; }
    .feature-icon { font-size: 2.5em; margin-bottom: 14px; display: block; }
    .feature-title { font-size: 1.05em; font-weight: 700; color: #E2E8F0; margin-bottom: 6px; }
    .feature-desc { font-size: 0.82em; color: #94A3B8; line-height: 1.5; }

    .section-header {
        font-size: 1.5em; font-weight: 800; color: #E2E8F0;
        margin: 32px 0 20px; display: flex; align-items: center; gap: 12px;
    }
    .section-header .icon { font-size: 1.3em; }

    .metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0; }
    @media (max-width: 768px) { .metric-row { grid-template-columns: repeat(2, 1fr); } }

    .metric-card {
        background: linear-gradient(145deg, #1A1A2E 0%, #0F0F1A 100%);
        border: 1px solid #2D2D44; border-radius: 16px;
        padding: 24px 20px; text-align: center; position: relative; overflow: hidden;
    }
    .metric-card::after {
        content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--accent, #7C3AED), transparent);
    }
    .metric-card .metric-icon { font-size: 1.6em; margin-bottom: 8px; display: block; }
    .metric-card .metric-value {
        font-size: 2.2em; font-weight: 900;
        background: linear-gradient(135deg, #7C3AED, #A78BFA);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-card .metric-label { font-size: 0.82em; color: #94A3B8; margin-top: 4px; font-weight: 600; }
    .metric-card .metric-delta { font-size: 0.75em; margin-top: 6px; font-weight: 600; }
    .metric-delta.up { color: #4ADE80; }
    .metric-delta.neutral { color: #64748B; }

    .verdict-banner {
        text-align: center; margin: 24px 0; padding: 20px;
        border-radius: 16px;
    }
    .verdict-badge {
        display: inline-block; padding: 14px 36px; border-radius: 14px;
        font-size: 1.5em; font-weight: 900; letter-spacing: 0.5px;
    }
    .verdict-strong { background: linear-gradient(135deg, #166534, #14532D); color: #86EFAC; border: 1px solid #22C55E; }
    .verdict-moderate { background: linear-gradient(135deg, #854D0E, #713F12); color: #FDE047; border: 1px solid #F59E0B; }
    .verdict-needs-work { background: linear-gradient(135deg, #9A3412, #7C2D12); color: #FDBA74; border: 1px solid #F97316; }
    .verdict-not-ready { background: linear-gradient(135deg, #991B1B, #7F1D1D); color: #FCA5A5; border: 1px solid #EF4444; }

    .content-card {
        background: linear-gradient(145deg, #1A1A2E 0%, #141425 100%);
        border: 1px solid #2D2D44; border-radius: 16px;
        padding: 24px; margin: 16px 0;
    }

    .bullet-card {
        background: #141425; border-left: 4px solid #7C3AED;
        border-radius: 0 14px 14px 0; padding: 18px 22px; margin: 12px 0;
    }
    .bullet-original { color: #F87171; text-decoration: line-through; font-size: 0.95em; }
    .bullet-problem { color: #FBBF24; font-size: 0.85em; margin-top: 6px; font-style: italic; }
    .bullet-improved { color: #4ADE80; margin-top: 10px; font-weight: 600; font-size: 0.95em; }

    .keyword-found {
        display: inline-block; background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.4); color: #86EFAC;
        padding: 5px 16px; border-radius: 22px; margin: 3px; font-size: 0.85em; font-weight: 500;
    }
    .keyword-missing {
        display: inline-block; background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5;
        padding: 5px 16px; border-radius: 22px; margin: 3px; font-size: 0.85em; font-weight: 500;
    }

    .roast-card {
        background: linear-gradient(145deg, #1A0A2E 0%, #2D1040 50%, #1A0A2E 100%);
        border: 1px solid #7C3AED; border-radius: 20px;
        padding: 30px; margin: 20px 0;
        box-shadow: 0 0 40px rgba(124, 58, 237, 0.15);
    }

    .interview-q {
        background: #141425; border-left: 4px solid #A78BFA;
        border-radius: 0 14px 14px 0; padding: 18px 22px; margin: 12px 0;
    }

    .flow-diagram {
        display: flex; flex-direction: column; align-items: center;
        gap: 0; padding: 20px 0;
    }
    .flow-row {
        display: flex; align-items: center; gap: 12px; width: 100%;
        justify-content: center; flex-wrap: wrap;
    }
    .flow-box {
        background: linear-gradient(145deg, #1A1A2E, #141425);
        border: 1px solid #3D3D5C; border-radius: 12px;
        padding: 12px 20px; text-align: center; min-width: 120px;
        color: #E2E8F0; font-size: 0.85em; font-weight: 600;
        transition: all 0.2s ease;
    }
    .flow-box:hover { border-color: #7C3AED; transform: scale(1.05); }
    .flow-box.highlight { border-color: #7C3AED; background: linear-gradient(145deg, #2D1B69, #1A1A2E); }
    .flow-arrow { color: #7C3AED; font-size: 1.3em; }

    .roadmap-card {
        background: linear-gradient(145deg, #1A1A2E, #141425);
        border: 1px solid #2D2D44; border-radius: 16px;
        padding: 24px; margin: 16px 0;
    }
    .roadmap-period {
        font-size: 1.1em; font-weight: 800; color: #A78BFA;
        margin-bottom: 14px; padding-bottom: 8px;
        border-bottom: 1px solid #2D2D44;
    }

    .report-card {
        background: linear-gradient(145deg, #1A1A2E, #141425);
        border: 1px solid #2D2D44; border-radius: 20px;
        padding: 32px 24px; text-align: center;
        transition: all 0.3s ease; cursor: pointer;
    }
    .report-card:hover {
        border-color: #7C3AED; transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.15);
    }
    .report-icon { font-size: 3em; margin-bottom: 14px; display: block; }
    .report-title { font-size: 1.15em; font-weight: 700; color: #E2E8F0; margin-bottom: 6px; }
    .report-desc { font-size: 0.82em; color: #94A3B8; margin-bottom: 18px; }

    .disclaimer {
        text-align: center; margin-top: 30px; padding: 16px 24px;
        background: rgba(26, 26, 46, 0.6); border-radius: 12px;
        border: 1px solid #2D2D44;
    }
    .disclaimer p { color: #64748B; font-size: 0.8em; }

    .copy-btn {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 14px; border-radius: 8px; font-size: 0.8em;
        background: rgba(124, 58, 237, 0.15); color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.3); cursor: pointer;
        margin-top: 8px; font-weight: 500;
    }
    .copy-btn:hover { background: rgba(124, 58, 237, 0.3); }

    .progress-wrap {
        height: 10px; border-radius: 5px; background: #1A1A2E;
        overflow: hidden; margin: 12px 0;
    }
    .progress-fill {
        height: 100%; border-radius: 5px;
        background: linear-gradient(90deg, #7C3AED, #A78BFA);
        transition: width 0.5s ease;
    }

    .tab-btn {
        padding: 10px 22px; border-radius: 10px; font-size: 0.9em;
        font-weight: 600; cursor: pointer; border: 1px solid #2D2D44;
        background: transparent; color: #94A3B8; transition: all 0.2s ease;
    }
    .tab-btn:hover { border-color: #7C3AED; color: #E2E8F0; }
    .tab-btn.active {
        background: rgba(124, 58, 237, 0.2); border-color: #7C3AED; color: #A78BFA;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1A1A2E 0%, #0F0F1A 100%) !important;
        border: 1px solid #2D2D44 !important; border-radius: 14px !important;
        padding: 16px !important;
    }
    [data-testid="stExpander"] { border: 1px solid #2D2D44 !important; border-radius: 14px !important; }
    [data-testid="stForm"] { border: 1px solid #2D2D44 !important; border-radius: 16px !important; padding: 24px !important; }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
        border: none !important; border-radius: 12px !important;
        font-weight: 700 !important; padding: 12px 28px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
        transform: translateY(-2px); box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
    }
    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #1A1A2E, #141425) !important;
        border: 1px solid #2D2D44 !important; border-radius: 12px !important;
        color: #E2E8F0 !important; font-weight: 600 !important;
        padding: 12px 18px !important; text-align: left !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #7C3AED !important;
        background: rgba(124, 58, 237, 0.1) !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0F0F1A; }
    ::-webkit-scrollbar-thumb { background: #2D2D44; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #7C3AED; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# IMPORTS
# ============================================================
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from utils.groq_client import check_api_key, call_groq_json, call_groq
from utils.resume_parser import extract_text_from_upload, validate_resume_text
from utils.jd_parser import validate_jd
from utils.prompts import (
    RESUME_ANALYSIS_SYSTEM_PROMPT, RESUME_ANALYSIS_PROMPT,
    TECH_ROAST_SYSTEM_PROMPT, TECH_ROAST_PROMPT,
    INTERVIEW_SYSTEM_PROMPT, INTERVIEW_PROMPT,
    CAREER_ROADMAP_SYSTEM_PROMPT, CAREER_ROADMAP_PROMPT,
    build_prompt,
)
from utils.scoring import (
    calculate_ats_score, calculate_job_match_score, calculate_resume_quality_score,
    compute_score_deltas, get_verdict_color,
)
from utils.session_manager import (
    save_analysis_to_history, get_previous_analysis, reset_session,
    get_analysis_count, is_analysis_available,
)
from utils.report_generator import generate_text_report, generate_html_report, generate_markdown_report

# ============================================================
# SAMPLE DATA
# ============================================================
SAMPLE_RESUME_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_resume.txt")
SAMPLE_JD = """Senior Software Engineer — AI/ML

TechNova Inc. is seeking a Senior Software Engineer with expertise in AI/ML to join our innovative engineering team.

Requirements:
- 3+ years of experience in Python software development
- Strong experience with machine learning frameworks (TensorFlow, PyTorch, or Scikit-learn)
- Experience building and deploying ML models in production environments
- Proficiency with cloud platforms (AWS, GCP, or Azure)
- Experience with Docker, Kubernetes, and CI/CD pipelines
- Strong SQL and NoSQL database skills (PostgreSQL, MongoDB)
- Experience with RESTful API design and microservices architecture
- Understanding of NLP, computer vision, or recommendation systems
- Experience with version control (Git) and agile methodologies

Responsibilities:
- Design, develop, and deploy scalable AI/ML solutions
- Build and maintain data pipelines and ETL processes
- Collaborate with cross-functional teams to integrate AI features
- Optimize ML models for performance and scalability
- Mentor junior engineers and contribute to technical documentation
- Participate in code reviews and architectural decisions

Nice to Have:
- Experience with Streamlit, Dash, or similar data visualization frameworks
- Knowledge of MLOps practices and tools (MLflow, Kubeflow)
- Experience with big data technologies (Spark, Hadoop)
- Contributions to open-source projects
- Published research or technical blog posts

Education: Bachelor's or Master's degree in Computer Science, AI, or related field."""

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def safe_expander(label, key, default=False):
    """Custom collapsible section — avoids Streamlit expander arrow rendering bugs."""
    state_key = f"_safe_expander_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default

    is_open = st.session_state[state_key]
    prefix = "▼" if is_open else "▶"

    clicked = st.button(f"{prefix}  {label}", key=f"_btn_{key}", use_container_width=True)
    if clicked:
        st.session_state[state_key] = not st.session_state[state_key]
        st.rerun()

    if st.session_state[state_key]:
        return st.container()
    return st.empty()


def load_sample_data():
    try:
        with open(SAMPLE_RESUME_PATH, "r", encoding="utf-8") as f:
            st.session_state.resume_text = f.read()
        st.session_state.resume_file_name = "sample_resume.txt"
    except Exception:
        st.session_state.resume_text = "Avantika Shukla\nSoftware Engineer\n\nA motivated software engineer with experience in Python, Machine Learning, and Web Development."
    st.session_state.job_description = SAMPLE_JD
    st.session_state.target_role = "Senior Software Engineer — AI/ML"
    st.session_state.experience_level = "Mid-Level"
    st.session_state.preferred_industry = "Technology"
    st.session_state.demo_loaded = True


def run_analysis():
    resume_text = st.session_state.resume_text
    job_description = st.session_state.job_description
    target_role = st.session_state.target_role or "Software Engineer"
    experience_level = st.session_state.experience_level or "Mid-Level"
    preferred_industry = st.session_state.preferred_industry or "Technology"
    if not resume_text or not job_description:
        st.error("Please provide both a resume and a job description.")
        return False
    st.session_state.analysis_running = True
    try:
        prompt = build_prompt(RESUME_ANALYSIS_PROMPT, resume_text=resume_text,
                              job_description=job_description, target_role=target_role,
                              experience_level=experience_level, preferred_industry=preferred_industry)
        with st.spinner("AI is ruthlessly analyzing your resume..."):
            analysis = call_groq_json(prompt, RESUME_ANALYSIS_SYSTEM_PROMPT)
        for field in ["ats_score", "job_match_score", "resume_quality_score"]:
            if field not in analysis: analysis[field] = 0
        st.session_state.analysis = analysis
        st.session_state.analysis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ats_detail = calculate_ats_score(analysis)
        jm_detail = calculate_job_match_score(analysis)
        quality_detail = calculate_resume_quality_score(analysis)
        st.session_state.ats_score_detail = ats_detail
        st.session_state.job_match_detail = jm_detail
        st.session_state.resume_quality_detail = quality_detail
        prev = get_previous_analysis()
        prev_dict = {}
        if prev:
            prev_dict = {"ats": {"score": prev.get("ats_score", 0)}, "job_match": {"score": prev.get("job_match_score", 0)}, "resume_quality": {"score": prev.get("resume_quality_score", 0)}}
        current_dict = {"ats": ats_detail, "job_match": jm_detail, "resume_quality": quality_detail}
        st.session_state.score_deltas = compute_score_deltas(current_dict, prev_dict)
        save_analysis_to_history(ats_score=ats_detail["score"], job_match_score=jm_detail["score"],
                                 resume_quality_score=quality_detail["score"], target_role=target_role,
                                 verdict=analysis.get("recruiter_verdict", "N/A"))
        st.session_state.analysis_running = False
        return True
    except ValueError as e:
        st.error(str(e)); st.session_state.analysis_running = False; return False
    except RuntimeError as e:
        st.error(str(e)); st.session_state.analysis_running = False; return False
    except Exception as e:
        st.error("⚠️ Something went wrong. Please try again in a moment."); st.session_state.analysis_running = False; return False


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown('<h1 style="font-size:1.4em;color:#7C3AED;text-align:center;margin-bottom:4px;">🤖 AI Resume Critic</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.75em;color:#94A3B8;text-align:center;font-style:italic;margin-bottom:16px;">Your Resume Applied. AI Got Ruthless.</p>', unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#2D2D44;margin:12px 0;">', unsafe_allow_html=True)

        st.markdown('<p style="font-size:0.8em;color:#64748B;font-weight:700;margin-bottom:10px;letter-spacing:1px;">NAVIGATION</p>', unsafe_allow_html=True)
        nav_items = [
            ("home", "🏠", "Dashboard"),
            ("analysis", "📄", "Resume Analysis"),
            ("job_match", "🎯", "Job Match"),
            ("tech_roast", "🔥", "Tech-Roast"),
            ("skill_gaps", "🧠", "Skill Gaps"),
            ("interview", "🎤", "Mock Interview"),
            ("career", "📊", "Career Insights"),
            ("report", "📥", "Download Report"),
        ]
        for page_key, icon, label in nav_items:
            active = st.session_state.get("page") == page_key
            cls = "nav-btn active" if active else "nav-btn"
            st.markdown(f'<div class="{cls}"><span class="nav-icon">{icon}</span><span class="nav-label">{label}</span></div>', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True):
                st.session_state.page = page_key
                st.rerun()

        st.markdown('<hr style="border-color:#2D2D44;margin:16px 0;">', unsafe_allow_html=True)

        st.markdown('<p style="font-size:0.8em;color:#64748B;font-weight:700;margin-bottom:10px;letter-spacing:1px;">ANALYSIS STATUS</p>', unsafe_allow_html=True)
        if is_analysis_available():
            ats = st.session_state.ats_score_detail
            role = st.session_state.target_role or "Not Set"
            st.markdown(f'<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);border-radius:10px;padding:12px;margin-bottom:8px;"><p style="color:#86EFAC;font-size:0.85em;font-weight:600;">✅ Analysis Complete</p><p style="color:#94A3B8;font-size:0.78em;margin-top:4px;">Role: {role}</p><p style="color:#94A3B8;font-size:0.78em;">ATS Score: {ats["score"]}/100</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:rgba(100,116,139,0.1);border:1px solid rgba(100,116,139,0.3);border-radius:10px;padding:12px;"><p style="color:#94A3B8;font-size:0.85em;">ℹ️ No analysis yet</p></div>', unsafe_allow_html=True)

        st.markdown('<hr style="border-color:#2D2D44;margin:16px 0;">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Demo", use_container_width=True):
                load_sample_data()
                st.rerun()
        with c2:
            if st.button("🔄 Reset", use_container_width=True):
                reset_session()
                st.rerun()

        st.markdown('<hr style="border-color:#2D2D44;margin:16px 0;">', unsafe_allow_html=True)
        if check_api_key():
            st.markdown('<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);border-radius:10px;padding:10px;text-align:center;"><p style="color:#86EFAC;font-size:0.8em;font-weight:600;">✅ Groq API Connected</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:10px;text-align:center;"><p style="color:#FDE047;font-size:0.8em;font-weight:600;">⚠️ API Key Not Set</p></div>', unsafe_allow_html=True)

        st.markdown('<div style="text-align:center;margin-top:24px;"><p style="font-size:0.68em;color:#475569;">Built with ❤️ by<br><strong style="color:#A78BFA;">Avantika Shukla</strong></p></div>', unsafe_allow_html=True)


# ============================================================
# HOME PAGE
# ============================================================
def render_home():
    st.markdown("""
    <div style="text-align:center;padding:24px 0 8px;">
        <h1 class="hero-title">🤖 AI RESUME CRITIC</h1>
        <p class="hero-sub">"Your Resume Applied. AI Got Ruthless."</p>
        <p class="hero-desc">Upload your resume, select your dream job, and let our AI recruiter<br>brutally analyze your career profile with actionable insights.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-row">
        <div class="cta-btn cta-primary" onclick="window.parent.postMessage({type:'streamlit:setPage',page:'analysis'},'*')">🚀 Analyze My Resume</div>
        <div class="cta-btn cta-secondary" onclick="window.parent.postMessage({type:'streamlit:setPage',page:'analysis'},'*')">🎯 Try Demo Mode</div>
        <div class="cta-btn cta-secondary" onclick="window.parent.postMessage({type:'streamlit:setPage',page:'interview'},'*')">🎤 Mock Interview</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Analyze My Resume", type="primary", use_container_width=True, key="hero_cta"):
        st.session_state.page = "analysis"; st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎯 Try Demo Mode", use_container_width=True, key="hero_demo"):
            load_sample_data(); st.session_state.page = "analysis"; st.rerun()
    with c2:
        if st.button("🎤 Mock Interview", use_container_width=True, key="hero_interview"):
            st.session_state.page = "interview"; st.rerun()

    st.markdown('<div class="section-header"><span class="icon">✨</span> Features</div>', unsafe_allow_html=True)
    features = [
        ("🔍", "ATS Analysis", "Score your resume against Applicant Tracking Systems with detailed breakdowns", "analysis"),
        ("🎯", "Job Matching", "See how well your resume fits the target role with keyword analysis", "job_match"),
        ("🧠", "Skill Gap Detection", "Find missing technical and soft skills with priority levels", "skill_gaps"),
        ("✍️", "AI Bullet Rewriting", "Transform weak bullets into powerful, impact-driven statements", "analysis"),
        ("🔥", "Tech-Roast", "Get roasted by our witty AI recruiter — professionally of course", "tech_roast"),
        ("🎤", "Mock Interview", "Practice with AI-generated questions and get scored", "interview"),
    ]
    cards_html = '<div class="features-grid">'
    for icon, title, desc, page in features:
        cards_html += f'<div class="feature-card" onclick="window.parent.postMessage({{type:\'streamlit:setPage\',page:\'{page}\'}},\'*\')"><span class="feature-icon">{icon}</span><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>'
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Graphical Data Flow
    st.markdown('<div class="section-header"><span class="icon">🏗️</span> How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="flow-diagram">
        <div class="flow-row">
            <div class="flow-box">👤 Upload Resume</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">🔍 Extract Text</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box highlight">🧩 Build Prompt</div>
        </div>
        <div style="text-align:center;color:#7C3AED;font-size:1.5em;margin:6px 0;">↓</div>
        <div class="flow-row">
            <div class="flow-box highlight">🤖 Groq AI</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">📦 Structured JSON</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">🧮 Score Engine</div>
        </div>
        <div style="text-align:center;color:#7C3AED;font-size:1.5em;margin:6px 0;">↓</div>
        <div class="flow-row">
            <div class="flow-box">📊 Dashboard</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">🔥 Roast / 🎤 Interview</div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">📥 Download Report</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        <p>⚠️ AI-generated insights are recommendations and should be reviewed before use.<br>
        Your resume data is processed in-memory and not stored.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ANALYSIS PAGE
# ============================================================
def render_analysis_page():
    st.markdown('<div class="section-header"><span class="icon">📄</span> Resume Analysis</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;margin-bottom:20px;">Upload your resume and target job description for AI-powered analysis.</p>', unsafe_allow_html=True)

    with st.form("analysis_form"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### 📄 Resume")
            uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt", "docx"], help="Supports PDF, TXT, DOCX")
            if uploaded_file:
                # Only extract text ONCE per unique file. Re-extracting on every rerun
                # was the root cause of "Could not read file" — the uploaded file's
                # internal buffer can only be read once per selection.
                file_signature = f"{uploaded_file.name}_{uploaded_file.size}"
                if st.session_state.get("_last_upload_signature") != file_signature:
                    st.session_state["_last_upload_signature"] = file_signature
                    st.session_state["_last_upload_error"] = None
                    try:
                        extracted_text = extract_text_from_upload(uploaded_file)
                        if extracted_text:
                            st.session_state.resume_text = extracted_text
                            st.session_state.resume_file_name = uploaded_file.name
                            st.session_state["_last_upload_validation"] = validate_resume_text(extracted_text)
                        else:
                            st.session_state["_last_upload_error"] = "⚠️ Could not extract text from the uploaded file."
                    except Exception as e:
                        st.session_state["_last_upload_error"] = f"⚠️ Could not read file: {str(e)}"

                if st.session_state.get("_last_upload_error"):
                    st.error(st.session_state["_last_upload_error"])
                elif st.session_state.get("resume_text") and st.session_state.get("resume_file_name") == uploaded_file.name:
                    validation = st.session_state.get("_last_upload_validation") or validate_resume_text(st.session_state.resume_text)
                    st.success(f"✅ Resume uploaded: {uploaded_file.name}")
                    st.caption(f"Words: {validation['word_count']} | Sections: {len(validation['sections_found'])}")
                    if validation["issues"]:
                        for issue in validation["issues"]:
                            st.warning(f"⚠️ {issue}")
                    # NOTE: safe_expander() uses st.button() internally, which Streamlit
                    # does not allow inside st.form(). Use the native st.expander here
                    # instead — it's form-safe, and the CSS at the top of this file
                    # already hides the arrow-icon rendering bug globally.
                    with st.expander("📄 View Extracted Resume"):
                        st.text_area("Resume Text", st.session_state.resume_text, height=250, disabled=True)

        with col2:
            st.markdown("### 🎯 Job Description")
            job_desc = st.text_area("Target Job Description", value=st.session_state.job_description, height=250)
            st.session_state.job_description = job_desc
            st.markdown("### 📋 Additional Info")
            ca, cb = st.columns(2)
            with ca:
                target_role = st.text_input("Target Role", value=st.session_state.target_role, placeholder="e.g., Senior Software Engineer")
            with cb:
                exp_level = st.selectbox("Experience Level", ["Entry-Level", "Mid-Level", "Senior", "Lead/Principal", "Manager"], index=1)
            industry = st.text_input("Preferred Industry", value=st.session_state.preferred_industry, placeholder="e.g., Technology")
            st.session_state.target_role = target_role
            st.session_state.experience_level = exp_level
            st.session_state.preferred_industry = industry

        submitted = st.form_submit_button("🚀 Run AI Analysis", type="primary", use_container_width=True)
        if submitted:
            if not st.session_state.resume_text:
                st.error("⚠️ Please upload a resume first.")
            elif not st.session_state.job_description:
                st.error("⚠️ Please enter a job description.")
            elif not check_api_key():
                st.error("⚠️ Groq API key not configured. Set GROQ_API_KEY in .env or Streamlit secrets.")
            else:
                success = run_analysis()
                if success:
                    st.success("✅ Analysis complete! Scroll down to see results.")

    if is_analysis_available():
        render_dashboard()


# ============================================================
# DASHBOARD
# ============================================================
def render_dashboard():
    st.markdown("---")
    st.markdown('<div class="section-header"><span class="icon">📊</span> Analysis Dashboard</div>', unsafe_allow_html=True)

    analysis = st.session_state.analysis
    ats_detail = st.session_state.ats_score_detail
    jm_detail = st.session_state.job_match_detail
    rq_detail = st.session_state.resume_quality_detail
    deltas = st.session_state.score_deltas

    # KPI Cards — st.metric with computed deltas (rubric: dynamic KPI cards)
    d_ats = deltas.get("ats")
    d_jm = deltas.get("job_match")
    d_rq = deltas.get("resume_quality")
    missing_count = len(analysis.get("missing_keywords", []))

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("📊 ATS Score", f"{ats_detail['score']}%",
                   delta=(f"{d_ats:+d}" if d_ats is not None else None))
    with kpi2:
        st.metric("🎯 Job Match", f"{jm_detail['score']}%",
                   delta=(f"{d_jm:+d}" if d_jm is not None else None))
    with kpi3:
        st.metric("📝 Resume Quality", f"{rq_detail['score']}%",
                   delta=(f"{d_rq:+d}" if d_rq is not None else None))
    with kpi4:
        st.metric("⚠️ Missing Keywords", missing_count,
                   help="Keywords found in the job description but missing from your resume")

    # Verdict
    verdict = analysis.get("recruiter_verdict", "N/A")
    vc = get_verdict_color(verdict)
    vcls = "verdict-strong" if "STRONG" in verdict.upper() else "verdict-moderate" if "MODERATE" in verdict.upper() else "verdict-needs-work" if "IMPROVEMENT" in verdict.upper() else "verdict-not-ready"
    st.markdown(f'<div class="verdict-banner"><div class="verdict-badge {vcls}" style="border-color:{vc};">🎖️ {verdict}</div></div>', unsafe_allow_html=True)

    # Executive Summary
    st.markdown('<div class="content-card"><p style="color:#94A3B8;font-size:0.85em;font-weight:600;margin-bottom:8px;">📋 EXECUTIVE SUMMARY</p><p style="color:#E2E8F0;line-height:1.7;">{}</p></div>'.format(analysis.get("executive_summary", "N/A")), unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Scores & Charts", "🔑 Keywords", "📝 Bullet Rewrites", "💡 Recommendations", "🎤 Interview Qs", "✅ Tracker"])
    with tab1:
        render_scores_charts(analysis, ats_detail)
    with tab2:
        render_keywords(analysis)
    with tab3:
        render_bullets(analysis)
    with tab4:
        render_recommendations(analysis)
    with tab5:
        render_interview_qs(analysis)
    with tab6:
        render_improvement_tracker(analysis)


def render_scores_charts(analysis, ats_detail):
    ats_exp = safe_expander("🔍 How did we calculate the ATS Score?", "ats_calc", default=True)
    if ats_exp:
        with ats_exp:
            for label, value in ats_detail["breakdown"].items():
                color = "#22C55E" if value >= 70 else "#F59E0B" if value >= 50 else "#EF4444"
                st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin:6px 0;"><span style="min-width:200px;color:#CBD5E1;font-size:0.9em;">{label}</span><div style="flex:1;height:10px;background:#1A1A2E;border-radius:5px;overflow:hidden;"><div style="width:{value}%;height:100%;background:{color};border-radius:5px;"></div></div><span style="color:{color};font-weight:700;min-width:40px;text-align:right;">{value}</span></div>', unsafe_allow_html=True)

    jm_detail = st.session_state.get("job_match_detail") or {}
    rq_detail = st.session_state.get("resume_quality_detail") or {}
    if jm_detail and rq_detail:
        st.markdown("### 📊 Score Comparison")
        vals = [ats_detail.get("score", 0), jm_detail.get("score", 0), rq_detail.get("score", 0)]
        compare_fig = go.Figure(data=go.Bar(
            x=["ATS Score", "Job Match", "Resume Quality"], y=vals,
            marker_color=["#7C3AED", "#22C55E", "#F59E0B"], text=vals, textposition="outside"))
        compare_fig.update_layout(paper_bgcolor='#0F0F1A', plot_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'),
            yaxis=dict(gridcolor='#2D2D44', range=[0, 100], title="Score"), xaxis=dict(gridcolor='#2D2D44'),
            height=320, showlegend=False)
        st.plotly_chart(compare_fig, use_container_width=True)

    section_scores = analysis.get("section_scores", {})
    if section_scores:
        st.markdown("### 📊 Resume Section Scores")
        fig = go.Figure(data=go.Scatterpolar(r=list(section_scores.values()), theta=[s.capitalize() for s in section_scores.keys()], fill='toself', fillcolor='rgba(124,58,237,0.2)', line=dict(color='#7C3AED', width=3), marker=dict(size=10, color='#A78BFA')))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#94A3B8'), gridcolor='#2D2D44'), bgcolor='#0F0F1A'), paper_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'), showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    tech_skills = analysis.get("technical_skills", [])
    missing_raw = analysis.get("missing_skills", [])
    missing_skills = [s.get("skill", s) if isinstance(s, dict) else s for s in missing_raw]
    if tech_skills or missing_skills:
        st.markdown("### 🧠 Skill Coverage")
        fig_data = {"Type": ["Found"] * len(tech_skills) + ["Missing"] * len(missing_skills), "Skill": tech_skills + missing_skills}
        fig_df = pd.DataFrame(fig_data)
        fig = px.bar(fig_df, x="Skill", color="Type", color_discrete_map={"Found": "#22C55E", "Missing": "#EF4444"}, title="Skills: Found vs Missing")
        fig.update_layout(paper_bgcolor='#0F0F1A', plot_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'), xaxis=dict(gridcolor='#2D2D44'), yaxis=dict(gridcolor='#2D2D44'), height=380)
        st.plotly_chart(fig, use_container_width=True)

    history = st.session_state.get("analysis_history", [])
    if len(history) >= 2:
        st.markdown("### 📈 Score Trend")
        hist_df = pd.DataFrame(history)
        fig = go.Figure()
        for col, color, name in [("ats_score", "#7C3AED", "ATS"), ("job_match_score", "#22C55E", "Job Match"), ("resume_quality_score", "#F59E0B", "Quality")]:
            fig.add_trace(go.Scatter(x=hist_df["timestamp"], y=hist_df[col], name=name, line=dict(color=color, width=2.5)))
        fig.update_layout(paper_bgcolor='#0F0F1A', plot_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'), xaxis=dict(gridcolor='#2D2D44'), yaxis=dict(gridcolor='#2D2D44'), legend=dict(bgcolor='#1A1A2E', bordercolor='#2D2D44'), height=350)
        st.plotly_chart(fig, use_container_width=True)


def render_keywords(analysis):
    matching = analysis.get("matching_keywords", [])
    missing = analysis.get("missing_keywords", [])
    st.markdown('<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">', unsafe_allow_html=True)
    st.markdown('<div><p style="color:#4ADE80;font-weight:700;margin-bottom:10px;">✅ Matching Keywords ({})</p>'.format(len(matching)), unsafe_allow_html=True)
    if matching:
        st.markdown(" ".join(f'<span class="keyword-found">{kw}</span>' for kw in matching), unsafe_allow_html=True)
    else:
        st.warning("No matching keywords found.")

    st.markdown('<p style="color:#F87171;font-weight:700;margin-bottom:10px;">⚠️ Missing Keywords ({})</p>'.format(len(missing)), unsafe_allow_html=True)
    if missing:
        kw_html = ""
        for kw in missing:
            if isinstance(kw, dict):
                imp = kw.get("importance", "Medium")
                kname = kw.get("keyword", "")
                kw_html += f'<span class="keyword-missing" title="{imp}">{kname}</span> '
            else:
                kw_html += f'<span class="keyword-missing">{kw}</span> '
        st.markdown(kw_html, unsafe_allow_html=True)
    else:
        st.success("No critical missing keywords!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📋 Keyword Table")
    keyword_data = []
    for kw in matching:
        keyword_data.append({"Keyword": kw, "Importance": "—", "Status": "✅ Found"})
    for kw in missing:
        if isinstance(kw, dict):
            keyword_data.append({"Keyword": kw.get("keyword", ""), "Importance": kw.get("importance", "Medium"), "Status": "❌ Missing"})
        else:
            keyword_data.append({"Keyword": str(kw), "Importance": "Medium", "Status": "❌ Missing"})
    if keyword_data:
        df = pd.DataFrame(keyword_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


def render_bullets(analysis):
    weak = analysis.get("weak_bullets", [])
    if not weak:
        st.success("🎉 No weak bullet points detected!")
        return
    st.markdown(f'<p style="color:#FBBF24;font-weight:700;font-size:1.1em;">Found {len(weak)} Weak Bullet Points</p>', unsafe_allow_html=True)
    for i, b in enumerate(weak, 1):
        if not isinstance(b, dict): continue
        st.markdown(f"""<div class="bullet-card">
            <p style="color:#94A3B8;font-weight:600;font-size:0.85em;margin-bottom:8px;">Bullet #{i}</p>
            <p class="bullet-original">❌ {b.get('original', 'N/A')}</p>
            <p class="bullet-problem">⚠️ {b.get('problem', 'Issue not specified')}</p>
            <p class="bullet-improved">✅ {b.get('improved', 'No improvement')}</p>
        </div>""", unsafe_allow_html=True)
        improved = b.get("improved", "")
        if improved:
            st.code(improved, language=None)
            if st.button(f"📋 Copy #{i}", key=f"copy_{i}"):
                st.toast("Copied!")


def render_recommendations(analysis):
    recs = analysis.get("recommendations", [])
    actions = analysis.get("priority_actions", [])
    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="content-card"><p style="color:#4ADE80;font-weight:700;margin-bottom:12px;">✅ Strengths</p>', unsafe_allow_html=True)
        for s in strengths: st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;">• {s}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="content-card"><p style="color:#F87171;font-weight:700;margin-bottom:12px;">❌ Weaknesses</p>', unsafe_allow_html=True)
        for w in weaknesses: st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;">• {w}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="content-card"><p style="color:#A78BFA;font-weight:700;margin-bottom:12px;">💡 Recommendations</p>', unsafe_allow_html=True)
        for i, r in enumerate(recs, 1): st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;"><strong>{i}.</strong> {r}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="content-card"><p style="color:#F59E0B;font-weight:700;margin-bottom:12px;">🎯 Priority Actions</p>', unsafe_allow_html=True)
        for i, a in enumerate(actions, 1): st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;"><strong>{i}.</strong> {a}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def build_improvement_checklist(analysis):
    """Turn analysis output into flat checklist rows for the editable tracker."""
    rows = []
    if not isinstance(analysis, dict):
        return rows

    weak_bullets = analysis.get("weak_bullets", [])
    for i, b in enumerate(weak_bullets, 1):
        if not isinstance(b, dict):
            continue
        rows.append({
            "Section": f"Bullet #{i}",
            "Current Issue": b.get("problem", "Weak bullet point") or "Weak bullet point",
            "Suggested Improvement": b.get("improved", "Rewrite with strong action verbs and metrics") or "Rewrite with strong action verbs and metrics",
            "Priority": "High",
            "Status": "Not Started",
        })

    for s in analysis.get("missing_skills", []):
        if isinstance(s, dict):
            skill_name = s.get("skill", "Unknown skill") or "Unknown skill"
            priority = s.get("priority", "Medium")
        else:
            skill_name = str(s)
            priority = "Medium"
        if priority not in ("High", "Medium", "Low"):
            priority = "Medium"
        rows.append({
            "Section": "Skill Gap",
            "Current Issue": f"Missing skill: {skill_name}",
            "Suggested Improvement": "Add relevant experience, project, or certification to resume",
            "Priority": priority,
            "Status": "Not Started",
        })

    for a in analysis.get("priority_actions", []):
        rows.append({
            "Section": "Priority Action",
            "Current Issue": str(a),
            "Suggested Improvement": "Implement this recommendation",
            "Priority": "High",
            "Status": "Not Started",
        })

    return rows


def render_improvement_tracker(analysis):
    """Editable 'Resume Improvement Checklist' — st.data_editor, persisted in session_state.
    Editing the table never triggers a new Groq API call."""
    timestamp = st.session_state.get("analysis_timestamp")
    if st.session_state.get("_checklist_source_timestamp") != timestamp:
        st.session_state["improvement_checklist"] = build_improvement_checklist(analysis)
        st.session_state["_checklist_source_timestamp"] = timestamp

    rows = st.session_state.get("improvement_checklist") or []
    if not rows:
        st.info("No specific improvement items were generated for this analysis.")
        return

    st.markdown('<p style="color:#94A3B8;font-size:0.9em;margin-bottom:10px;">Track your progress fixing each issue below. Update <strong>Status</strong> as you go — edits are saved for this session only and never trigger a new AI call.</p>', unsafe_allow_html=True)

    try:
        df = pd.DataFrame(rows)
        edited_df = st.data_editor(
            df,
            column_config={
                "Section": st.column_config.TextColumn("Section", disabled=True),
                "Current Issue": st.column_config.TextColumn("Current Issue", disabled=True, width="large"),
                "Suggested Improvement": st.column_config.TextColumn("Suggested Improvement", disabled=True, width="large"),
                "Priority": st.column_config.SelectboxColumn("Priority", options=["High", "Medium", "Low"], disabled=True),
                "Status": st.column_config.SelectboxColumn("Status", options=["Not Started", "In Progress", "Done"], required=True),
            },
            hide_index=True,
            use_container_width=True,
            key="improvement_checklist_editor",
        )
        st.session_state["improvement_checklist"] = edited_df.to_dict("records")
    except Exception:
        st.warning("⚠️ Couldn't render the editable tracker for this analysis. Showing a read-only table instead.")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        return

    done = sum(1 for r in st.session_state["improvement_checklist"] if r.get("Status") == "Done")
    total = len(st.session_state["improvement_checklist"])
    st.metric("✅ Items Resolved", f"{done}/{total}")


def render_interview_qs(analysis):
    questions = analysis.get("interview_questions", [])
    if not questions:
        st.info("No interview questions generated.")
        return
    st.markdown(f'<p style="font-weight:700;font-size:1.1em;">🎤 {len(questions)} Practice Interview Questions</p>', unsafe_allow_html=True)
    for i, q in enumerate(questions, 1):
        if not isinstance(q, dict): continue
        cat = q.get("category", "General")
        diff = q.get("difficulty", "Medium")
        dc = {"Easy": "#22C55E", "Medium": "#F59E0B", "Hard": "#EF4444"}.get(diff, "#94A3B8")
        st.markdown(f"""<div class="interview-q">
            <p style="color:#E2E8F0;font-weight:600;">Q{i}. {q.get('question', '')}</p>
            <p style="color:#94A3B8;font-size:0.82em;margin-top:6px;">[{cat}] <span style="color:{dc};">Difficulty: {diff}</span></p>
        </div>""", unsafe_allow_html=True)

    if st.button("🎤 Start Full Mock Interview", type="primary", use_container_width=True):
        st.session_state.page = "interview"; st.rerun()


# ============================================================
# JOB MATCH PAGE
# ============================================================
def render_job_match_page():
    st.markdown('<div class="section-header"><span class="icon">🎯</span> Job Match Analysis</div>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="font-size:1.2em;color:#F59E0B;margin-bottom:12px;">⚠️ No analysis available</p><p style="color:#94A3B8;">Please run a resume analysis first to see job match details.</p></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
                st.session_state.page = "analysis"; st.rerun()
        with c2:
            if st.button("🎯 Try Demo", use_container_width=True):
                load_sample_data(); st.session_state.page = "analysis"; st.rerun()
        return
    render_dashboard()


# ============================================================
# TECH ROAST PAGE
# ============================================================
def render_tech_roast():
    st.markdown('<div class="section-header"><span class="icon">🔥</span> Tech-Roast</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;margin-bottom:20px;">Let our AI recruiter roast your resume — professionally, of course.</p>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="color:#F59E0B;">⚠️ Please run a resume analysis first!</p></div>', unsafe_allow_html=True)
        if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()
        return
    if st.button("🔥 Roast My Resume", type="primary", use_container_width=True):
        try:
            prompt = build_prompt(TECH_ROAST_PROMPT, resume_text=st.session_state.resume_text,
                                  job_description=st.session_state.job_description,
                                  target_role=st.session_state.target_role or "Software Engineer")
            with st.spinner("🔥 The AI recruiter is warming up..."):
                roast = call_groq(prompt, TECH_ROAST_SYSTEM_PROMPT)
            st.session_state.tech_roast = roast
        except Exception as e:
            st.error(str(e))
    if st.session_state.tech_roast:
        roast_text = st.session_state.tech_roast.replace("\n", "<br>")
        st.markdown(f'<div class="roast-card">{roast_text}</div>', unsafe_allow_html=True)


# ============================================================
# SKILL GAPS PAGE
# ============================================================
def render_skill_gaps():
    st.markdown('<div class="section-header"><span class="icon">🧠</span> Skill Gap Analysis</div>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="color:#F59E0B;">⚠️ Please run a resume analysis first!</p></div>', unsafe_allow_html=True)
        if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()
        return
    analysis = st.session_state.analysis
    tech_skills = analysis.get("technical_skills", [])
    missing_skills = analysis.get("missing_skills", [])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="content-card"><p style="color:#4ADE80;font-weight:700;margin-bottom:12px;">🛠️ Technical Skills Found ({})</p>'.format(len(tech_skills)), unsafe_allow_html=True)
        for s in tech_skills:
            st.markdown(f'<span class="keyword-found">{s}</span> ', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="content-card"><p style="color:#F87171;font-weight:700;margin-bottom:12px;">📚 Missing Skills ({})</p>'.format(len(missing_skills)), unsafe_allow_html=True)
        for s in missing_skills:
            if isinstance(s, dict):
                name = s.get("skill", "")
                pri = s.get("priority", "Medium")
                cat = s.get("category", "Technical")
                badge = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(pri, "⚪")
                st.markdown(f'<p style="color:#CBD5E1;margin:6px 0;"><strong>{badge} {name}</strong> <span style="color:#64748B;font-size:0.85em;">— {cat} | {pri}</span></p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="keyword-missing">{s}</span> ', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    all_skills = []
    for s in tech_skills: all_skills.append({"Skill": s, "Status": "Found", "Priority": "—"})
    for s in missing_skills:
        if isinstance(s, dict): all_skills.append({"Skill": s.get("skill", ""), "Status": "Missing", "Priority": s.get("priority", "Medium")})
        else: all_skills.append({"Skill": str(s), "Status": "Missing", "Priority": "Medium"})
    if all_skills:
        df = pd.DataFrame(all_skills)
        fig = px.bar(df, x="Skill", color="Status", color_discrete_map={"Found": "#22C55E", "Missing": "#EF4444"})
        fig.update_layout(paper_bgcolor='#0F0F1A', plot_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'), xaxis=dict(gridcolor='#2D2D44'), yaxis=dict(gridcolor='#2D2D44'), height=380)
        st.plotly_chart(fig, use_container_width=True)

    soft_gaps = analysis.get("soft_skill_gaps", [])
    if soft_gaps:
        st.markdown('<div class="content-card"><p style="color:#FBBF24;font-weight:700;margin-bottom:12px;">🤝 Soft Skill Gaps</p>', unsafe_allow_html=True)
        for g in soft_gaps:
            st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;">• {g}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# MOCK INTERVIEW PAGE
# ============================================================
def render_mock_interview():
    st.markdown('<div class="section-header"><span class="icon">🎤</span> AI Mock Interview</div>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="color:#F59E0B;">⚠️ Please run a resume analysis first!</p></div>', unsafe_allow_html=True)
        if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        mode = st.selectbox("Interview Mode", ["Mixed Interview", "Technical Interview", "HR Interview", "Project Interview"], key="int_mode_sel")
    with c2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="int_diff_sel")
    with c3:
        num_qs = st.slider("Questions", 3, 10, 5)

    if not st.session_state.interview_active:
        if st.button("🎤 Start Interview", type="primary", use_container_width=True):
            try:
                prompt = build_prompt(INTERVIEW_PROMPT, resume_text=st.session_state.resume_text,
                                      job_description=st.session_state.job_description,
                                      interview_mode=mode, difficulty=difficulty, num_questions=num_qs)
                with st.spinner("🧠 Generating questions..."):
                    result = call_groq_json(prompt, INTERVIEW_SYSTEM_PROMPT)
                questions = result.get("questions", [])
                st.session_state.interview_questions = questions
                st.session_state.interview_current_idx = 0
                st.session_state.interview_answers = []
                st.session_state.interview_scores = []
                st.session_state.interview_feedback = []
                st.session_state.interview_active = True
                st.session_state.interview_completed = False
            except Exception as e:
                st.error(str(e))

    if st.session_state.interview_active:
        questions = st.session_state.interview_questions
        idx = st.session_state.interview_current_idx
        if idx < len(questions):
            q = questions[idx]
            dc = {"Easy": "#22C55E", "Medium": "#F59E0B", "Hard": "#EF4444"}.get(q.get("difficulty", "Medium"), "#94A3B8")
            progress = (idx + 1) / len(questions)
            st.markdown(f"""<div class="content-card">
                <p style="color:#94A3B8;font-size:0.85em;margin-bottom:10px;">Question {idx+1} of {len(questions)} | {q.get('category', 'General')} | <span style="color:{dc}">{q.get('difficulty', 'Medium')}</span></p>
                <h3 style="color:#E2E8F0;font-size:1.15em;">{q.get('question', '')}</h3>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:{progress*100}%"></div></div>""", unsafe_allow_html=True)
            answer = st.text_area("Your Answer:", height=120, key=f"ans_{idx}")
            ca, cb = st.columns(2)
            with ca:
                if st.button("➡️ Submit", type="primary", use_container_width=True):
                    if answer.strip():
                        st.session_state.interview_answers.append(answer)
                        score = min(10, max(1, len(answer.split()) // 10))
                        st.session_state.interview_scores.append(score)
                        st.session_state.interview_feedback.append(f"Score: {score}/10")
                        st.session_state.interview_current_idx += 1
                        st.rerun()
                    else:
                        st.warning("Please write an answer!")
            with cb:
                if st.button("⏭️ Skip", use_container_width=True):
                    st.session_state.interview_answers.append("(Skipped)")
                    st.session_state.interview_scores.append(0)
                    st.session_state.interview_feedback.append("Skipped.")
                    st.session_state.interview_current_idx += 1
                    st.rerun()
        else:
            st.session_state.interview_completed = True
            st.session_state.interview_active = False
            scores = st.session_state.interview_scores
            avg = np.mean(scores) if scores else 0
            st.session_state.interview_overall_score = avg
            st.markdown(f"""<div style="text-align:center;margin:24px 0;">
                <h2 style="color:#4ADE80;font-size:1.8em;">🎉 Interview Complete!</h2>
            </div>
            <div class="metric-row">
                <div class="metric-card" style="--accent:#7C3AED"><span class="metric-icon">📊</span><div class="metric-value">{avg:.1f}</div><div class="metric-label">Overall Score</div><div class="metric-delta neutral">out of 10</div></div>
                <div class="metric-card" style="--accent:#22C55E"><span class="metric-icon">✅</span><div class="metric-value">{len([a for a in st.session_state.interview_answers if a != '(Skipped)'])}</div><div class="metric-label">Answered</div><div class="metric-delta neutral">of {len(questions)}</div></div>
            </div>""", unsafe_allow_html=True)
            if scores:
                fig = go.Figure(data=go.Bar(y=[f"Q{i+1}" for i in range(len(scores))], x=scores, orientation='h',
                    marker_color=['#22C55E' if s >= 7 else '#F59E0B' if s >= 4 else '#EF4444' for s in scores]))
                fig.update_layout(paper_bgcolor='#0F0F1A', plot_bgcolor='#0F0F1A', font=dict(color='#E2E8F0'),
                    xaxis=dict(gridcolor='#2D2D44', range=[0, 10], title="Score"), height=max(200, len(scores)*50))
                st.plotly_chart(fig, use_container_width=True)
            if st.button("🔄 Restart Interview", use_container_width=True):
                for k in ["interview_active", "interview_current_idx", "interview_answers", "interview_scores", "interview_feedback", "interview_completed"]:
                    st.session_state[k] = False if k == "interview_active" or k == "interview_completed" else (0 if k == "interview_current_idx" else [])
                st.rerun()


# ============================================================
# CAREER INSIGHTS PAGE
# ============================================================
def render_career_insights():
    st.markdown('<div class="section-header"><span class="icon">📊</span> Career Insights</div>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="color:#F59E0B;">⚠️ Please run a resume analysis first!</p></div>', unsafe_allow_html=True)
        if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()
        return
    analysis = st.session_state.analysis
    if st.button("🗺️ Generate Career Roadmap", type="primary", use_container_width=True):
        try:
            prompt = build_prompt(CAREER_ROADMAP_PROMPT,
                                  ats_score=st.session_state.ats_score_detail["score"],
                                  job_match_score=st.session_state.job_match_detail["score"],
                                  resume_quality_score=st.session_state.resume_quality_detail["score"],
                                  weaknesses=", ".join(analysis.get("weaknesses", [])),
                                  missing_skills=", ".join([s.get("skill", str(s)) if isinstance(s, dict) else str(s) for s in analysis.get("missing_skills", [])]),
                                  target_role=st.session_state.target_role or "Software Engineer")
            with st.spinner("🗺️ Generating roadmap..."):
                roadmap = call_groq_json(prompt, CAREER_ROADMAP_SYSTEM_PROMPT)
            st.session_state.career_roadmap = roadmap
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    if st.session_state.career_roadmap:
        rm = st.session_state.career_roadmap
        for period, icon, label in [("next_7_days", "📅", "Next 7 Days"), ("next_30_days", "📆", "Next 30 Days"), ("next_90_days", "🗓️", "Next 90 Days")]:
            actions = rm.get("roadmap", {}).get(period, [])
            if actions:
                st.markdown(f'<div class="roadmap-card"><p class="roadmap-period">{icon} {label}</p>', unsafe_allow_html=True)
                for i, a in enumerate(actions, 1):
                    txt = a.get("action", "") if isinstance(a, dict) else str(a)
                    pri = a.get("priority", "Medium") if isinstance(a, dict) else "Medium"
                    badge = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(pri, "⚪")
                    st.markdown(f'<p style="color:#CBD5E1;margin:6px 0;"><strong>{badge} {i}. {txt}</strong></p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        cert_recs = rm.get("certification_recommendations", [])
        if cert_recs:
            st.markdown('<div class="content-card"><p style="color:#F59E0B;font-weight:700;margin-bottom:12px;">🏆 Recommended Certifications</p>', unsafe_allow_html=True)
            for c in cert_recs:
                st.markdown(f'<p style="color:#CBD5E1;margin:4px 0;">• {c}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    history = st.session_state.get("analysis_history", [])
    if history:
        st.markdown('<div class="content-card"><p style="color:#A78BFA;font-weight:700;margin-bottom:12px;">📈 Analysis History</p>', unsafe_allow_html=True)
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REPORT DOWNLOAD PAGE
# ============================================================
def render_report_download():
    st.markdown('<div class="section-header"><span class="icon">📥</span> Download Report</div>', unsafe_allow_html=True)
    if not is_analysis_available():
        st.markdown('<div class="content-card" style="text-align:center;padding:40px;"><p style="color:#F59E0B;margin-bottom:12px;">⚠️ No analysis to download</p><p style="color:#94A3B8;">Please run a resume analysis first.</p></div>', unsafe_allow_html=True)
        if st.button("📄 Go to Analysis", type="primary", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()
        return

    analysis = st.session_state.analysis
    scoring = {"ats": st.session_state.ats_score_detail, "job_match": st.session_state.job_match_detail, "resume_quality": st.session_state.resume_quality_detail}
    role = st.session_state.target_role or "Software Engineer"
    txt_report = generate_text_report(analysis, scoring, st.session_state.resume_text, st.session_state.job_description, role)
    html_report = generate_html_report(analysis, scoring, st.session_state.resume_text, st.session_state.job_description, role)
    md_report = generate_markdown_report(analysis, scoring, st.session_state.resume_text, st.session_state.job_description, role)

    st.markdown('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:24px 0;">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="report-card">
        <span class="report-icon">📄</span>
        <div class="report-title">Plain Text</div>
        <div class="report-desc">Clean text report with all analysis data</div>
    </div>
    <div class="report-card">
        <span class="report-icon">🌐</span>
        <div class="report-title">HTML Report</div>
        <div class="report-desc">Styled web report, open in any browser</div>
    </div>
    <div class="report-card">
        <span class="report-icon">📝</span>
        <div class="report-title">Markdown</div>
        <div class="report-desc">MD format for GitHub, docs, or editors</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("⬇️ Download TXT", data=txt_report, file_name=f"resume_report_{role.replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
    with c2:
        st.download_button("⬇️ Download HTML", data=html_report, file_name=f"resume_report_{role.replace(' ', '_')}.html", mime="text/html", use_container_width=True)
    with c3:
        st.download_button("⬇️ Download Markdown", data=md_report, file_name=f"resume_report_{role.replace(' ', '_')}.md", mime="text/markdown", use_container_width=True)

    preview_exp = safe_expander("👁️ Report Preview", "report_preview")
    if preview_exp:
        with preview_exp:
            st.text(txt_report[:3000] + ("..." if len(txt_report) > 3000 else ""))


# ============================================================
# MAIN ROUTER
# ============================================================
def main():
    render_sidebar()
    page = st.session_state.get("page", "home")
    routes = {
        "home": render_home,
        "analysis": render_analysis_page,
        "job_match": render_job_match_page,
        "tech_roast": render_tech_roast,
        "skill_gaps": render_skill_gaps,
        "interview": render_mock_interview,
        "career": render_career_insights,
        "report": render_report_download,
    }
    routes.get(page, render_home)()

if __name__ == "__main__":
    main()
