"""
Report Generator - Creates downloadable analysis reports.
"""

import json
from datetime import datetime
from typing import Dict, Optional


def generate_text_report(analysis: Dict, scoring: Dict, resume_text: str,
                         job_description: str, target_role: str) -> str:
    """Generate a comprehensive text report of the analysis."""
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    report = []
    report.append("=" * 70)
    report.append("   AI RESUME CRITIC — TECH-ROAST")
    report.append('   "Your Resume Applied. AI Got Ruthless."')
    report.append("=" * 70)
    report.append(f"\n   Generated: {now}")
    report.append(f"   Target Role: {target_role}")
    report.append("\n" + "=" * 70)

    # Executive Summary
    report.append("\n📋 EXECUTIVE SUMMARY")
    report.append("-" * 40)
    report.append(analysis.get("executive_summary", "N/A"))

    # Scores
    report.append("\n\n📊 SCORES")
    report.append("-" * 40)
    ats = scoring.get("ats", {})
    job_match = scoring.get("job_match", {})
    quality = scoring.get("resume_quality", {})
    report.append(f"   ATS Score:            {ats.get('score', 'N/A')} / 100")
    report.append(f"   Job Match Score:      {job_match.get('score', 'N/A')} / 100")
    report.append(f"   Resume Quality Score: {quality.get('score', 'N/A')} / 100")

    # Recruiter Verdict
    report.append(f"\n\n🎖️  RECRUITER VERDICT: {analysis.get('recruiter_verdict', 'N/A')}")

    # Strengths
    report.append("\n\n✅ STRENGTHS")
    report.append("-" * 40)
    for i, s in enumerate(analysis.get("strengths", []), 1):
        report.append(f"   {i}. {s}")

    # Weaknesses
    report.append("\n\n❌ WEAKNESSES")
    report.append("-" * 40)
    for i, w in enumerate(analysis.get("weaknesses", []), 1):
        report.append(f"   {i}. {w}")

    # Matching Keywords
    report.append("\n\n🔑 MATCHING KEYWORDS")
    report.append("-" * 40)
    for kw in analysis.get("matching_keywords", []):
        report.append(f"   ✓ {kw}")

    # Missing Keywords
    report.append("\n\n⚠️  MISSING KEYWORDS")
    report.append("-" * 40)
    for kw in analysis.get("missing_keywords", []):
        if isinstance(kw, dict):
            report.append(f"   ✗ {kw.get('keyword', '')} [{kw.get('importance', '')}]")
        else:
            report.append(f"   ✗ {kw}")

    # Technical Skills
    report.append("\n\n🛠️  TECHNICAL SKILLS FOUND")
    report.append("-" * 40)
    for skill in analysis.get("technical_skills", []):
        report.append(f"   • {skill}")

    # Missing Skills
    report.append("\n\n📚 MISSING SKILLS")
    report.append("-" * 40)
    for skill in analysis.get("missing_skills", []):
        if isinstance(skill, dict):
            report.append(f"   • {skill.get('skill', '')} [{skill.get('priority', '')}]")
        else:
            report.append(f"   • {skill}")

    # Soft Skill Gaps
    report.append("\n\n🤝 SOFT SKILL GAPS")
    report.append("-" * 40)
    for gap in analysis.get("soft_skill_gaps", []):
        report.append(f"   • {gap}")

    # Section Scores
    report.append("\n\n📈 SECTION SCORES")
    report.append("-" * 40)
    section_scores = analysis.get("section_scores", {})
    for section, score in section_scores.items():
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        report.append(f"   {section.capitalize():12s} {score:3d}/100  {bar}")

    # Weak Bullet Points
    report.append("\n\n📝 WEAK BULLET POINTS & REWRITES")
    report.append("-" * 40)
    for i, bullet in enumerate(analysis.get("weak_bullets", []), 1):
        if isinstance(bullet, dict):
            report.append(f"\n   #{i}")
            report.append(f"   Original:  {bullet.get('original', 'N/A')}")
            report.append(f"   Problem:   {bullet.get('problem', 'N/A')}")
            report.append(f"   Improved:  {bullet.get('improved', 'N/A')}")

    # Recommendations
    report.append("\n\n💡 RECOMMENDATIONS")
    report.append("-" * 40)
    for i, rec in enumerate(analysis.get("recommendations", []), 1):
        report.append(f"   {i}. {rec}")

    # Priority Actions
    report.append("\n\n🎯 PRIORITY ACTIONS")
    report.append("-" * 40)
    for i, action in enumerate(analysis.get("priority_actions", []), 1):
        report.append(f"   {i}. {action}")

    # Interview Questions
    report.append("\n\n🎤 SAMPLE INTERVIEW QUESTIONS")
    report.append("-" * 40)
    for i, q in enumerate(analysis.get("interview_questions", []), 1):
        if isinstance(q, dict):
            report.append(f"   {i}. [{q.get('category', '')}] {q.get('question', '')}")
        else:
            report.append(f"   {i}. {q}")

    report.append("\n\n" + "=" * 70)
    report.append("   AI Resume Critic — Powered by Groq AI")
    report.append("   Built by Avantika Shukla")
    report.append("   " + now)
    report.append("=" * 70)

    return "\n".join(report)


def generate_html_report(analysis: Dict, scoring: Dict, resume_text: str,
                         job_description: str, target_role: str) -> str:
    """Generate an HTML report of the analysis."""
    import html as html_module

    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    def esc(text):
        return html_module.escape(str(text)) if text else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Resume Critic Report — {esc(target_role)}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0F0F1A; color: #E2E8F0; padding: 40px; line-height: 1.6; }}
.container {{ max-width: 900px; margin: 0 auto; }}
h1 {{ color: #7C3AED; font-size: 2em; margin-bottom: 5px; }}
.tagline {{ color: #94A3B8; font-style: italic; margin-bottom: 20px; }}
.meta {{ color: #64748B; margin-bottom: 30px; font-size: 0.9em; }}
h2 {{ color: #A78BFA; font-size: 1.4em; margin: 30px 0 15px; border-bottom: 1px solid #2D2D44; padding-bottom: 8px; }}
.score-card {{ background: #1A1A2E; border: 1px solid #2D2D44; border-radius: 12px; padding: 20px; margin: 10px 0; display: inline-block; width: 30%; text-align: center; }}
.score-value {{ font-size: 2.5em; font-weight: bold; }}
.score-label {{ color: #94A3B8; font-size: 0.85em; margin-top: 5px; }}
.verdict {{ font-size: 1.8em; font-weight: bold; padding: 15px 25px; border-radius: 10px; display: inline-block; margin: 15px 0; }}
.strong {{ background: #166534; color: #86EFAC; }}
.moderate {{ background: #854D0E; color: #FDE047; }}
.needs-work {{ background: #9A3412; color: #FDBA74; }}
.not-ready {{ background: #991B1B; color: #FCA5A5; }}
ul {{ padding-left: 20px; margin: 10px 0; }}
li {{ margin: 8px 0; color: #CBD5E1; }}
.keyword {{ display: inline-block; background: #1E1E3A; border: 1px solid #3D3D5C; padding: 4px 12px; border-radius: 20px; margin: 3px; font-size: 0.9em; }}
.found {{ border-color: #22C55E; color: #86EFAC; }}
.missing {{ border-color: #EF4444; color: #FCA5A5; }}
.bullet-card {{ background: #1A1A2E; border-left: 3px solid #7C3AED; padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0; }}
.bullet-original {{ color: #F87171; text-decoration: line-through; }}
.bullet-improved {{ color: #4ADE80; margin-top: 8px; }}
.footer {{ text-align: center; color: #475569; margin-top: 40px; padding-top: 20px; border-top: 1px solid #2D2D44; }}
</style>
</head>
<body>
<div class="container">
<h1>🤖 AI Resume Critic Report</h1>
<p class="tagline">"Your Resume Applied. AI Got Ruthless."</p>
<p class="meta">Generated: {esc(now)} | Target Role: {esc(target_role)}</p>

<h2>📊 Scores</h2>
<div style="display: flex; gap: 15px; flex-wrap: wrap;">
<div class="score-card"><div class="score-value">{scoring.get('ats', {}).get('score', 0)}</div><div class="score-label">ATS Score</div></div>
<div class="score-card"><div class="score-value">{scoring.get('job_match', {}).get('score', 0)}</div><div class="score-label">Job Match</div></div>
<div class="score-card"><div class="score-value">{scoring.get('resume_quality', {}).get('score', 0)}</div><div class="score-label">Resume Quality</div></div>
</div>

<h2>🎖️ Recruiter Verdict</h2>
<p class="verdict {analysis.get('recruiter_verdict', '').lower().replace(' ', '-')}">{esc(analysis.get('recruiter_verdict', 'N/A'))}</p>

<h2>📋 Executive Summary</h2>
<p>{esc(analysis.get('executive_summary', 'N/A'))}</p>

<h2>✅ Strengths</h2>
<ul>{''.join(f'<li>{esc(s)}</li>' for s in analysis.get('strengths', []))}</ul>

<h2>❌ Weaknesses</h2>
<ul>{''.join(f'<li>{esc(w)}</li>' for w in analysis.get('weaknesses', []))}</ul>

<h2>🔑 Keywords</h2>
<p><strong>Found:</strong></p>
<div>{''.join(f'<span class="keyword found">{esc(kw)}</span>' for kw in analysis.get('matching_keywords', []))}</div>
<p style="margin-top:10px"><strong>Missing:</strong></p>
<div>{''.join(f'<span class="keyword missing">{esc(kw.get("keyword", "") if isinstance(kw, dict) else kw)}</span>' for kw in analysis.get('missing_keywords', []))}</div>

<h2>📝 Weak Bullet Rewrites</h2>
"""

    for bullet in analysis.get("weak_bullets", []):
        if isinstance(bullet, dict):
            html += f"""<div class="bullet-card">
<p class="bullet-original">{esc(bullet.get('original', ''))}</p>
<p><em>Problem: {esc(bullet.get('problem', ''))}</em></p>
<p class="bullet-improved">✅ {esc(bullet.get('improved', ''))}</p>
</div>"""

    html += f"""
<h2>💡 Recommendations</h2>
<ul>{''.join(f'<li>{esc(r)}</li>' for r in analysis.get('recommendations', []))}</ul>

<h2>🎯 Priority Actions</h2>
<ul>{''.join(f'<li>{esc(a)}</li>' for a in analysis.get('priority_actions', []))}</ul>

<div class="footer">
<p>AI Resume Critic — Powered by Groq AI</p>
<p>Built by Avantika Shukla</p>
</div>
</div>
</body>
</html>"""

    return html


def generate_markdown_report(analysis: Dict, scoring: Dict, resume_text: str,
                             job_description: str, target_role: str) -> str:
    """Generate a Markdown report of the analysis."""
    now = datetime.now().strftime("%B %d, %Y")

    md = f"""# 🤖 AI Resume Critic Report

> *"Your Resume Applied. AI Got Ruthless."*

**Generated:** {now} | **Target Role:** {target_role}

---

## 📊 Scores

| Metric | Score |
|--------|-------|
| ATS Score | {scoring.get('ats', {}).get('score', 0)}/100 |
| Job Match | {scoring.get('job_match', {}).get('score', 0)}/100 |
| Resume Quality | {scoring.get('resume_quality', {}).get('score', 0)}/100 |

## 🎖️ Recruiter Verdict

**{analysis.get('recruiter_verdict', 'N/A')}**

## 📋 Executive Summary

{analysis.get('executive_summary', 'N/A')}

## ✅ Strengths

{chr(10).join(f'- {s}' for s in analysis.get('strengths', []))}

## ❌ Weaknesses

{chr(10).join(f'- {w}' for w in analysis.get('weaknesses', []))}

## 🔑 Matching Keywords

{', '.join(f'`{kw}`' for kw in analysis.get('matching_keywords', []))}

## ⚠️ Missing Keywords

| Keyword | Importance |
|----------|------------|
{chr(10).join(f'| {kw.get("keyword", "") if isinstance(kw, dict) else kw} | {kw.get("importance", "") if isinstance(kw, dict) else "N/A"} |' for kw in analysis.get('missing_keywords', []))}

## 📝 Weak Bullet Rewrites

"""

    for i, bullet in enumerate(analysis.get("weak_bullets", []), 1):
        if isinstance(bullet, dict):
            md += f"""### #{i}
- **Original:** ~~{bullet.get('original', '')}~~
- **Problem:** {bullet.get('problem', '')}
- **Improved:** {bullet.get('improved', '')}

"""

    md += f"""## 💡 Recommendations

{chr(10).join(f'{i+1}. {r}' for i, r in enumerate(analysis.get('recommendations', [])))}

## 🎯 Priority Actions

{chr(10).join(f'{i+1}. {a}' for i, a in enumerate(analysis.get('priority_actions', [])))}

---

*AI Resume Critic — Powered by Groq AI | Built by Avantika Shukla*
"""

    return md
