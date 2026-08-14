"""
Scoring Engine - Calculates and manages ATS, Job Match, and Resume Quality scores.
Provides transparent scoring with detailed breakdowns.
"""

import numpy as np
from typing import Dict, List, Tuple


def calculate_ats_score(analysis: dict) -> Dict:
    """
    Calculate ATS score with transparent breakdown.
    Combines AI-generated base score with computed metrics.
    """
    ai_score = analysis.get("ats_score", 0)

    # Calculate keyword coverage
    matching_kw = analysis.get("matching_keywords", [])
    missing_kw = analysis.get("missing_keywords", [])
    total_kw = len(matching_kw) + len(missing_kw)
    keyword_coverage = (len(matching_kw) / total_kw * 100) if total_kw > 0 else 0

    # Calculate section completeness
    section_scores = analysis.get("section_scores", {})
    sections_present = sum(1 for v in section_scores.values() if v > 0)
    total_sections = 5  # summary, skills, experience, projects, education
    section_completeness = (sections_present / total_sections * 100) if total_sections > 0 else 0

    # Calculate skill coverage
    tech_skills = analysis.get("technical_skills", [])
    missing_skills = analysis.get("missing_skills", [])
    total_skills = len(tech_skills) + len(missing_skills)
    skill_coverage = (len(tech_skills) / total_skills * 100) if total_skills > 0 else 0

    # Weighted final score
    weights = {
        "ai_assessment": 0.40,
        "keyword_coverage": 0.25,
        "section_completeness": 0.20,
        "skill_coverage": 0.15,
    }

    final_score = (
        ai_score * weights["ai_assessment"]
        + keyword_coverage * weights["keyword_coverage"]
        + section_completeness * weights["section_completeness"]
        + skill_coverage * weights["skill_coverage"]
    )

    final_score = min(100, max(0, int(final_score)))

    breakdown = {
        "AI Assessment": int(ai_score),
        "Keyword Coverage": int(keyword_coverage),
        "Section Completeness": int(section_completeness),
        "Skill Coverage": int(skill_coverage),
    }

    return {
        "score": final_score,
        "breakdown": breakdown,
        "weights": weights,
    }


def calculate_job_match_score(analysis: dict) -> Dict:
    """
    Calculate Job Match score with transparent breakdown.
    """
    ai_score = analysis.get("job_match_score", 0)

    matching_kw = analysis.get("matching_keywords", [])
    missing_kw = analysis.get("missing_keywords", [])
    total_kw = len(matching_kw) + len(missing_kw)
    keyword_match = (len(matching_kw) / total_kw * 100) if total_kw > 0 else 0

    section_scores = analysis.get("section_scores", {})
    experience_score = section_scores.get("experience", 0)
    skills_score = section_scores.get("skills", 0)
    projects_score = section_scores.get("projects", 0)
    relevance_score = (experience_score + skills_score + projects_score) / 3

    # Count high-priority missing skills
    missing_skills = analysis.get("missing_skills", [])
    high_priority_missing = sum(
        1 for s in missing_skills if isinstance(s, dict) and s.get("priority", "").lower() == "high"
    )
    penalty = min(20, high_priority_missing * 5)

    final_score = min(100, max(0, int(
        ai_score * 0.5
        + keyword_match * 0.25
        + relevance_score * 0.25
        - penalty
    )))

    breakdown = {
        "AI Match Assessment": int(ai_score),
        "Keyword Match": int(keyword_match),
        "Content Relevance": int(relevance_score),
        "High-Priority Skill Penalty": -penalty,
    }

    return {
        "score": final_score,
        "breakdown": breakdown,
    }


def calculate_resume_quality_score(analysis: dict) -> Dict:
    """
    Calculate Resume Quality score based on section scores and bullet quality.
    """
    section_scores = analysis.get("section_scores", {})

    if section_scores:
        avg_section_score = np.mean(list(section_scores.values()))
    else:
        avg_section_score = 0

    # Assess bullet quality
    weak_bullets = analysis.get("weak_bullets", [])
    total_bullets = max(len(weak_bullets) + 5, 1)  # Estimate total bullets
    bullet_quality = max(0, 100 - (len(weak_bullets) / total_bullets * 100))

    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])
    balance_score = min(100, len(strengths) / max(len(strengths) + len(weaknesses), 1) * 100)

    ai_score = analysis.get("resume_quality_score", 0)

    final_score = min(100, max(0, int(
        ai_score * 0.4
        + avg_section_score * 0.25
        + bullet_quality * 0.2
        + balance_score * 0.15
    )))

    breakdown = {
        "AI Quality Assessment": int(ai_score),
        "Average Section Score": int(avg_section_score),
        "Bullet Point Quality": int(bullet_quality),
        "Content Balance": int(balance_score),
    }

    return {
        "score": final_score,
        "breakdown": breakdown,
    }


def compute_score_deltas(current: Dict, previous: Dict) -> Dict:
    """
    Compute deltas between current and previous scores.
    Returns delta values for display with st.metric().
    """
    deltas = {}

    if previous:
        for key in ["ats", "job_match", "resume_quality"]:
            curr = current.get(key, {}).get("score", 0)
            prev = previous.get(key, {}).get("score", 0)
            delta = curr - prev
            deltas[key] = delta
    else:
        deltas = {"ats": None, "job_match": None, "resume_quality": None}

    return deltas


def get_score_label(score: int) -> str:
    """Get a human-readable label for a score."""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 55:
        return "Average"
    elif score >= 40:
        return "Below Average"
    else:
        return "Needs Significant Improvement"


def get_verdict_color(verdict: str) -> str:
    """Get color for recruiter verdict."""
    verdict_upper = verdict.upper()
    if "STRONG" in verdict_upper:
        return "#22C55E"  # Green
    elif "MODERATE" in verdict_upper:
        return "#F59E0B"  # Amber
    elif "IMPROVEMENT" in verdict_upper:
        return "#F97316"  # Orange
    elif "NOT READY" in verdict_upper:
        return "#EF4444"  # Red
    else:
        return "#7C3AED"  # Purple default
