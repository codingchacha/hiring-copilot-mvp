🧠 Product Requirements Document (PRD)
📌 Project Name
Hiring Copilot MVP

🧨 Problem Statement
AI companies and enterprises struggle to fill specialized roles quickly. The scarcity of qualified candidates, manual sourcing, inefficient screening, and unconscious bias stretch the average time-to-hire beyond 60 days, significantly increasing recruitment costs.

🎯 Solution Overview
Build a natural-language-driven hiring copilot that enables recruiters to:

Instantly find top candidates using plain-English queries (e.g., "Find senior GenAI engineers with LangChain + RAG experience in Europe, open to contract work").

Automatically rank and score profiles based on skill, experience, GitHub data, pedigree, and certifications.

Screen candidate behavior using social media signals.

Send personalized outreach emails and generate screening questions using LLMs.

🧩 Core Features
Natural Language Candidate Search
Recruiters type a plain-text search. An LLM converts it to structured filters, runs a search, and fetches top-matching candidate profiles.

Candidate Scoring & Ranking
Each candidate is scored on:

Skills match

Experience match

GitHub profile (stars, activity)

Top company pedigree

Relevant certifications

Resume Fit Analysis (Alternate Entry Point)
Users can upload a resume and receive an analysis on how well the profile fits a specified job description.

Behavioral Signal Simulation (Mocked)
Basic simulated background analysis using mock LinkedIn/X (Twitter) data to flag risky or inappropriate behavior.

Candidate Outreach (via Email)
Pre-written outreach email is generated. Recruiter clicks "Send" to reach the candidate.

Auto Screening Q&A Generator
Based on the job description, the system generates technical and behavioral screening questions using an LLM.

Authentication (Optional but included)
Simple signup/login system using Supabase authentication for recruiters.

🧱 Tech Stack
Layer	Technology
Frontend	Streamlit (hosted on Streamlit Cloud)
Backend	Python (within Streamlit itself, no separate FastAPI)
Database	Supabase (PostgreSQL, Auth)
LLM	OpenRouter / Groq SDK for Claude/GPT
Email	SMTP / SendGrid (for outreach)
GitHub Data	Mocked (simulate real GitHub stars per user)

🧪 Mocked Features (For MVP)
GitHub stars per candidate (simulate highest-star repo).

Twitter/LinkedIn behavior data (flagged text strings).

Resume parsing (basic string match or mocked).

📁 Deliverables
✅ 2-minute demo video

✅ Public GitHub repository with README & PRD

✅ Live demo (Streamlit hosted)

✅ Clean modular code

