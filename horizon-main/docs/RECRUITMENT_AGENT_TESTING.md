# 🎯 Recruitment Agent - Testing Guide

## 📋 Overview

The recruitment pipeline is organized into modular components in the `src/` directory:

### File Structure:
1. **`src/utils/candidate_scorer.py`** - Scores candidates using Groq AI
2. **`src/utils/interview_scheduler.py`** - Schedules interviews in Google Calendar
3. **`src/utils/google_sheets_manager.py`** - Manages Google Sheets export
4. **`src/agents/recruitment_agent.py`** - Orchestrates scoring + scheduling + export
5. **`ai_recruiter_pipeline.py`** - Complete LangGraph workflow (main entry point)

## 🧪 Testing Instructions

### Test 1: Complete LangGraph Pipeline (Recommended)
```powershell
python ai_recruiter_pipeline.py
```
**What it does:**
1. ✅ Monitors Gmail for resumes
2. ✅ Extracts candidate data from PDFs
3. ✅ Enriches profiles with LinkedIn/LLM
4. ✅ Scores all candidates using AI
5. ✅ Filters by minimum score (default: 5.0)
6. ✅ Schedules calendar interviews for shortlisted candidates
7. ✅ Creates Google Sheets (all candidates + interviews)
8. ✅ Saves CSV export to `output/` folder

### Test 2: Validate Configuration
```powershell
python scripts/validate_config.py
```
**What it does:** Verifies all API keys and configurations are valid

### Test 3: Visualize Workflow
```powershell
python scripts/visualize_pipeline.py
```
**What it does:** Generates workflow diagram in `output/recruitment_pipeline_graph.png`

## 📊 Default Criteria

```python
DEFAULT_CRITERIA = {
    "role": "AI/Software Professional",
    "required_skills": [
        "python", "machine learning", "ai", "data science"
    ],
    "preferred_skills": [
        "react", "node.js", "leadership", "cloud computing"
    ],
    "min_experience_years": 2
}
```

## ⚙️ Customization

### Change Minimum Score Threshold
Edit `ai_recruiter_pipeline.py`, in the `main()` function:
```python
def main():
    result = run_complete_pipeline(
        check_gmail=True,
        max_emails=10,
        min_score_threshold=5.0  # Change this (0-10)
    )
```

### Change Scoring Criteria
Edit `src/utils/candidate_scorer.py` and modify the `DEFAULT_CRITERIA` dict:
```python
DEFAULT_CRITERIA = {
    "role": "Data Scientist",
    "required_skills": ["python", "sql", "statistics"],
    "preferred_skills": ["machine learning", "deep learning"],
    "min_experience_years": 3
}
```

## � Output Files

After running `ai_recruiter_pipeline.py`:
- **JSON:** `output/enhanced_candidates_YYYYMMDD_HHMMSS.json`
- **CSV:** `output/Scheduled_Interviews_YYYYMMDD_HHMMSS.csv`
- **Google Sheets:** Links printed in console
  - All Candidates Sheet
  - Interview Schedule Sheet
- **Calendar Events:** Created in Google Calendar
- **Workflow Diagram:** `output/recruitment_pipeline_graph.png` (if visualized)

## 📂 File Organization

All source files are now organized in the `src/` directory:
- **`src/agents/`** - Business orchestrators
  - `recruitment_agent.py` - Coordinates scoring, scheduling, and export
- **`src/utils/`** - Single-purpose utilities
  - `auto_gmail_monitor.py` - Gmail integration
  - `pdf_extractor.py` - Resume parsing
  - `linkedin_enricher.py` - Profile enrichment
  - `candidate_scorer.py` - AI scoring
  - `interview_scheduler.py` - Calendar integration
  - `google_sheets_manager.py` - Sheets export
- **`src/config/`** - Configuration management
  - `settings.py` - Type-safe Pydantic models
  - `legacy_config.py` - Environment variable loading
  - `validator.py` - Configuration validation
- `recruitment_agent.py` (replaces main.py + google_sheet.py)

## 🚀 Next Steps

1. Run `python recruitment_agent.py` to test full pipeline
2. Check Google Calendar for created events
3. Check Google Sheets for scheduled interviews sheet
4. Review CSV output file
5. Adjust min_score threshold as needed
6. Once satisfied, integrate into main pipeline
