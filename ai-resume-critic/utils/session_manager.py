"""
Session Manager - Manages Streamlit session_state for AI Resume Critic.
Ensures all state keys are safely initialized.
"""

import streamlit as st
from datetime import datetime
from typing import Any, Dict, List, Optional


def init_session_state():
    """Initialize all session state keys with safe defaults."""
    defaults = {
        # Input data
        "resume_text": "",
        "resume_file_name": "",
        "job_description": "",
        "target_role": "",
        "experience_level": "Mid-Level",
        "preferred_industry": "Technology",
        "resume_validated": False,
        "jd_validated": False,

        # Analysis results
        "analysis": None,
        "analysis_timestamp": None,
        "ats_score_detail": None,
        "job_match_detail": None,
        "resume_quality_detail": None,

        # Scoring
        "score_deltas": {"ats": None, "job_match": None, "resume_quality": None},

        # History
        "analysis_history": [],

        # Tech roast
        "tech_roast": None,

        # Interview
        "interview_mode": "Mixed Interview",
        "interview_difficulty": "Medium",
        "interview_questions": [],
        "interview_current_idx": 0,
        "interview_answers": [],
        "interview_scores": [],
        "interview_feedback": [],
        "interview_active": False,
        "interview_completed": False,
        "interview_overall_score": None,

        # Career roadmap
        "career_roadmap": None,

        # Improvement tracker (st.data_editor)
        "improvement_checklist": [],
        "_checklist_source_timestamp": None,

        # Resume upload cache (prevents re-reading an already-consumed file buffer)
        "_last_upload_signature": None,
        "_last_upload_error": None,
        "_last_upload_validation": None,

        # UI state
        "page": "home",
        "analysis_running": False,
        "demo_loaded": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def save_analysis_to_history(
    ats_score: int,
    job_match_score: int,
    resume_quality_score: int,
    target_role: str,
    verdict: str,
):
    """Save analysis results to history."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_role": target_role,
        "ats_score": ats_score,
        "job_match_score": job_match_score,
        "resume_quality_score": resume_quality_score,
        "verdict": verdict,
    }

    history = st.session_state.get("analysis_history", [])
    history.append(entry)

    # Keep last 20 analyses
    if len(history) > 20:
        history = history[-20:]

    st.session_state.analysis_history = history


def get_previous_analysis() -> Optional[Dict]:
    """Get the previous analysis for delta computation."""
    history = st.session_state.get("analysis_history", [])
    if len(history) >= 2:
        return history[-2]
    return None


def reset_session():
    """Safely reset all session state."""
    keys_to_keep = ["analysis_history"]

    saved = {}
    for key in keys_to_keep:
        if key in st.session_state:
            saved[key] = st.session_state[key]

    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

    for key, value in saved.items():
        st.session_state[key] = value

    # Re-initialize defaults
    init_session_state()


def get_analysis_count() -> int:
    """Get the number of analyses performed in this session."""
    return len(st.session_state.get("analysis_history", []))


def is_analysis_available() -> bool:
    """Check if analysis results are available."""
    return st.session_state.get("analysis") is not None
