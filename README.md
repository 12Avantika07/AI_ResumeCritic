<div align="center">

# 🤖 AI RESUME CRITIC — TECH-ROAST

### "Your Resume Applied. AI Got Ruthless."

![Python](https://python.org)
![Streamlit](https://streamlit.io)
![Groq](https://groq.com)
![License](#-license)
![Status](https://ai-resumecritic-avantika.streamlit.app/)

<br>

# 🚀 LIVE DEMO — AI RESUME CRITIC

### 👉 Launch AI Resume Critic →

Live Application:
https://ai-resumecritic-avantika.streamlit.app/

<br>

[📖 Architecture](#-system-architecture) · [✨ Features](#-features) · [🚀 Getting Started](#-installation) · [🧪 Testing](#-testing)

</div>

---

## 🎯 Overview

AI Resume Critic is a production-quality Streamlit application that acts as a ruthless but constructive senior technical recruiter.

It analyzes a resume against a target job description and provides:

* 📊 ATS Compatibility Score with transparent breakdown
* 🎯 Job Match Score with keyword analysis
* 🔍 Weak Bullet Point Detection & AI Rewriting
* 🧠 Skill Gap Analysis
* 🔥 Tech-Roast Mode
* 🎤 AI Mock Interview with scoring
* 📊 Personalized Career Roadmap
* 📥 Downloadable Analysis Reports
* 📈 Analysis history and progress tracking
* ✅ Improvement Tracker

> Built by Avantika Shukla as a B.Tech Capstone Project at MirAI School of Technology.

---

## 📡 Live Demo

### 🚀 The application is deployed and live on Streamlit Community Cloud.

<div align="center">

## 🔥 OPEN AI RESUME CRITIC

### 👉 Click Here to Launch the Live Application 👈

https://ai-resumecritic-avantika.streamlit.app/

</div>

> Note: The button above opens the deployed production application directly. No local setup is required for the live demo.

---

## ✨ Features

### 📄 Resume Analysis

* Upload PDF, TXT, or DOCX resumes
* Intelligent text extraction
* Scanned PDF detection
* Resume validation
* Section detection
* Completeness analysis

### 🎯 ATS Scoring

* Transparent multi-factor scoring
* Keyword coverage analysis
* Section completeness evaluation
* Skill coverage assessment
* Detailed score breakdown
* Visual progress indicators

### 📊 Job Matching

* Keyword overlap analysis
* Experience relevance scoring
* High-priority skill penalty calculation
* Matching vs Missing keyword comparison

### 🔍 Weak Bullet Rewriting

* Detects vague and weak bullet points
* Identifies passive writing
* AI-powered professional rewrites
* Action-oriented improvements
* [ADD REAL METRIC] placeholders prevent fabricated achievements
* One-click copying of improved bullets

### 🔥 Tech-Roast Mode

A recruiter-style roast that is:

* Witty
* Sarcastic
* Constructive
* Professional
* Focused on the resume, never the person
* Always followed by actionable improvements

### 🧠 Skill Gap Analysis

Skills are categorized into:

* 💻 Technical Skills
* 🛠️ Tools
* ☁️ Cloud
* 🤝 Soft Skills
* 🎯 Domain Skills

Each gap receives:

* Priority level
* Recommended learning area
* Improvement guidance

### 🎤 AI Mock Interview

Multiple interview modes:

* Technical
* HR
* Project
* Mixed

Difficulty levels:

* Easy
* Medium
* Hard

The system provides:

* Contextual questions
* Question-by-question scoring
* Feedback
* Progress tracking
* Final interview scorecard

### 📊 Career Insights

Personalized career intelligence including:

* 7-day action plan
* 30-day improvement plan
* 90-day roadmap
* Skill acquisition recommendations
* Certification suggestions
* Networking recommendations
* Historical analysis trends

### ✅ Improvement Tracker

The application converts identified weaknesses into an editable improvement tracker.

Users can track:

Not Started → In Progress → Done

The tracker uses Streamlit session state so updates persist during the session without unnecessarily triggering another AI analysis.

### 📥 Report Generation

Download comprehensive reports in:

* TXT
* HTML
* Markdown

Reports include:

* ATS score
* Job Match score
* Resume quality
* Missing keywords
* Skill gaps
* Weak bullets
* AI rewrites
* Recommendations
* Career insights

---

## 🛠️ Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Framework       | St
reamlit 1.40+           |
| AI Engine       | Groq API                  |
| LLM             | Llama family models       |
| Language        | Python 3.12+              |
| Data Processing | Pandas, NumPy             |
| Visualization   | Plotly                    |
| PDF Parsing     | PyPDF                     |
| DOCX Parsing    | python-docx               |
| Environment     | python-dotenv             |
| Deployment      | Streamlit Community Cloud |

---

## 🏗️ System Architecture

graph TD
    A[👤 User] --> B[🖥️ Streamlit UI]

    B --> C[📄 Resume Upload]
    B --> D[📋 Job Description]

    C --> E[🔍 Resume Parser]
    D --> F[📋 JD Parser]

    E --> G[📝 Extracted Resume Text]
    F --> H[📝 Validated Job Description]

    G --> I[🧩 Prompt Builder]
    H --> I

    I --> J[🤖 Groq AI]

    J --> K[📦 Structured Analysis]

    K --> L[🧮 Scoring Engine]

    L --> M[📊 ATS Score]
    L --> N[🎯 Job Match]
    L --> O[🧠 Skill Gap]
    L --> P[🔥 Tech Roast]
    L --> Q[🎤 Mock Interview]
    L --> R[🗺️ Career Roadmap]
    L --> S[📥 Reports]

    M --> T[📊 Dashboard]
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T


---

## 🔄 Data Flow

User
  │
  ├── Upload Resume
  │
  └── Enter Job Description
          │
          ▼
     Input Validation
          │
          ▼
      Resume Parser
          │
          ▼
      Prompt Builder
          │
          ▼
        Groq AI
          │
          ▼
   Structured JSON Output
          │
          ▼
    Scoring Engine
          │
    ┌─────┼──────────────┐
    ▼     ▼              ▼
   ATS  Job Match    Skill Gap
    │     │              │
    └─────┼──────────────┘
          ▼
      Dashboard
          │
    ┌─────┼─────────────┐
    ▼     ▼             ▼
Tech   Interview     Roadmap
Roast                   │
                       ▼
                    Reports


---

## 📁 Project Structure

AI_ResumeCritic/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── pages/
│   ├── __init__.py
│   ├── 01_Resume_Analysis.py
│   ├── 02_Job_Match.py
│   ├── 03_Interview.py
│   ├── 04_Career_Insights.py
│   └── 05_Report.py
│
├── utils/
│   ├── __init__.py
│   ├── groq_client.py
│   ├── resume_parser.py
│   ├── jd_parser.py
│   ├── prompts.py
│   ├── scoring.py
│   ├── session_manager.py
│   └── report_generator.py
│
└── data/
    └── sample_resume.txt


---

## 🧠 AI Prompt Architecture

The application uses specialized prompts for different career-intelligence tasks.

| Prompt                   | Purpose                              |
| ------------------------ | ------------------------------------ |
| RESUME_ANALYSIS_PROMPT | Full resume analysis                 |
| TECH_ROAST_PROMPT      | Recruiter-style resume roast         |
| BULLET_REWRITE_PROMPT  | Professional bullet rewriting        |
| INTERVIEW_PROMPT       | Contextual interview questions       |
| CAREER_ROADMAP_PROMPT  | Personalized career improvement plan |

All prompts dynamically incorporate the user's resume and target job description.

---

## 🔒 Security & Privacy

The project follows a privacy-first approach:

* 🔐 No hardcoded API keys
* 🔑 Environment variables / Streamlit Secrets
* 🧠 Resume processing in memory
* 🚫 No intentional persistent resume storage
* 🛡️ System prompts are not exposed
* 🧹 Error messages are sanitized
* 🔒 No unnecessary user data logging

---

## 📦 Installation

### Prerequisites

* Python 3.12+
* Git
* Groq API key

### 1. Clone the Repository

git clone https://github.com/12Avantika07/AI_ResumeCritic.git
cd AI_ResumeCritic


### 2. Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate


Linux/macOS:

python -m venv venv
source venv/bin/activate


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Configure Environment

Create .env:

GROQ_API_KEY=your_groq_api_key_here


### 5. Run Locally

streamlit run app.py


Open:

http://localhost:8501


---

## ☁️ Deployment

The project is deployed on Streamlit Community Cloud.

### Production Application

🚀 https://ai-resumecritic-avantika.streamlit.app/

### Deployment Configuration

Repository:
12Avantika07/AI_ResumeCritic

Branch:
main

Main file:
app.py


Add the following secret in Streamlit Cloud:

GROQ_API_KEY = "your_groq_api_key_here"


Then deploy the application.

---

## 🧪 Testing

The application handles:

| Scenario              | Expected Behavior            |
| --------------------- | ---------------------------- |
| Fresh launch          | Home page loads successfully |
| Demo mode             | Sample resume loads          |
| PDF upload            | Resume text extracted        |
| TXT upload            | Resume text extracted        |
| DOCX upload           | Resume text extracted        |
| Empty resume          | Validation warning           |
| Empty JD              | Validation warning           |
| Valid analysis        | Complete dashboard           |
| Invalid Groq response | Graceful error               |
| API failure           | User-friendly message        |
| Missing API key       | Setup instructions           |
| Session persistence   | Results retained             |
| Reset                 | Session cleared              |
| Multiple analyses     | History tracked              |
| Report generation     | Downloadable report          |
| Interview             | Question + scoring flow      |

---

## 🎓 Capstone Rubric Alignment

| Criteria                 | Implementation                                                |
| ------------------------ | ------------------------------------------------------------- |
| Technical Implementation | Python, Streamlit, modular architecture, session state, forms |
| AI Integration           | Groq API, dynamic prompts, structured AI output               |
| UI / Visualization       | KPI cards, Plotly charts, tables, improvement tracker         |
| Deployment               | Streamlit Community Cloud                                     |
| GitHub                   | README, architecture, setup documentation                     |
| System Design            | Mermaid architecture and data-flow diagrams                   |

---

## 🚀 Quick Access

<div align="center">

### 🔥 Ready to test it?

# 👉 LAUNCH AI RESUME CRITIC

Upload your resume. Add a job description. Let AI judge it.

> *Your Resume Applied. AI Got Ruthless.*

</div>

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

### Avantika Shukla

B.Tech Computer Science
MirAI School of Technology

Built with ❤️ as a B.Tech Capstone Project.

---

<div align="center">

### 🤖 AI Resume Critic — Tech-Roast

"Your Resume Applied. AI Got Ruthless."

🚀 Live Demo · ⭐ Star the repository if you found it useful!

</div>
