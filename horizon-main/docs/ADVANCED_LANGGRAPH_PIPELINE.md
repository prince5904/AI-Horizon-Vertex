# 🚀 Advanced LangGraph Pipeline - AI Recruiter Copilot

## Pipeline Overview

This is an **advanced conditional LangGraph workflow** with intelligent decision-making and routing based on candidate scores.

## 📊 Pipeline Visualization

### **View the Complete Graph**

Run the visualization script to see the detailed ASCII graph:
```bash
python visualize_pipeline.py
```

The graph shows:
- ✅ **8 separate nodes** (not just 7!) - Each major operation has its own node
- ✅ **Conditional routing** with dotted lines showing decision paths
- ✅ **LinkedIn enrichment** as a dedicated step
- ✅ **Two separate sheet creation nodes** (All Candidates + Interview Schedule)
- ✅ **Calendar scheduling** as a conditional node

### **ASCII Graph Structure**

```
__start__
    ↓
gmail_monitor (📧 Download resumes from Gmail)
    ↓
extract_resumes (📄 Parse PDFs with AI)
    ↓
linkedin_enrich (🔗 Try LinkedIn API, fallback to LLM)
    ↓
score_candidates (📊 AI scoring + decision point)
    ↓ ↓
    ├─→ schedule_interviews (📅 Create calendar events) [IF shortlisted > 0]
    |       ↓
    └─→ create_all_candidates_sheet (📊 Sheet for ALL candidates)
            ↓
        create_interview_sheet (📅 Sheet for SHORTLISTED only)
            ↓
        final_report (📋 Display all links)
            ↓
        __end__
```

---

## 🔄 Workflow Architecture

### **Linear Nodes (Sequential)**

```
┌─────────────────┐
│  gmail_monitor  │  ← Entry Point
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ extract_resumes │
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ enrich_candidates│  ← Tries LinkedIn API, falls back to LLM
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ score_candidates │  ← AI scoring + Decision point
└────────┬─────────┘
         │
         ▼
    ┌────┴────┐
```

### **Conditional Routing (Decision Logic)**

```
    ┌────────────────────────┐
    │  should_schedule_?     │ ← Conditional Edge
    └────────┬───────────────┘
             │
      ┌──────┴───────┐
      │              │
      ▼              ▼
IF SHORTLISTED   IF NO CANDIDATES
  (score ≥ 5.0)    (skip scheduling)
      │              │
      ▼              │
┌───────────────┐    │
│schedule_      │    │
│interviews     │    │
└───────┬───────┘    │
        │            │
        └────┬───────┘
             │
             ▼
      ┌──────────────┐
      │export_sheets │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │final_report  │
      └──────┬───────┘
             │
             ▼
           [END]
```

---

## 🎯 Key Features

### **1. Conditional Interview Scheduling**
- **Condition**: `score >= min_score_threshold`
- **If TRUE** → Schedule interviews in Google Calendar
- **If FALSE** → Skip scheduling, go directly to export

### **2. Intelligent LinkedIn Enrichment**
- **Primary**: Attempts real LinkedIn API call (if URL available)
- **Fallback**: Uses LLM-based enrichment if API fails
- **Tracking**: Marks enrichment source (`linkedin_api`, `llm_fallback`, `llm_only`)

### **3. Candidate Classification**
- **Shortlisted**: Candidates meeting score threshold
- **Rejected**: Candidates below threshold
- Both groups tracked separately in state

### **4. Comprehensive Output**
All outputs created regardless of conditional paths:
- ✅ All candidates database (Google Sheets)
- ✅ Interview schedule sheet (only if shortlisted exist)
- ✅ CSV export (only if interviews scheduled)
- ✅ Calendar event links (only if interviews scheduled)
- ✅ JSON file with all enriched data

---

## 📋 State Management

### **RecruitmentState Fields**

```python
class RecruitmentState(TypedDict):
    # Configuration
    check_gmail: bool
    max_emails: int
    min_score_threshold: float
    
    # Data Flow
    email_messages: List[Dict]
    downloaded_files: List[str]
    extracted_candidates: List[Dict]
    enriched_candidates: List[Dict]
    scored_candidates: List[Dict]
    
    # Decision Tracking
    shortlisted_candidates: List[Dict]  # Score >= threshold
    rejected_candidates: List[Dict]      # Score < threshold
    scheduled_candidates: List[Dict]     # With calendar events
    
    # Processing State
    current_candidate: Dict
    linkedin_success: bool
    
    # Outputs
    sheets_url: str                 # All candidates sheet
    interview_sheet_url: str        # Shortlisted only sheet
    csv_file: str
    json_file: str
    calendar_links: List[str]
    
    # Status
    status: str
    errors: List[str]
```

---

## 🧠 Decision Functions

### **`should_schedule_interviews(state)`**

**Purpose**: Determines whether to schedule interviews based on shortlisted candidates

**Returns**:
- `"schedule_interviews"` → If shortlisted candidates exist
- `"skip_scheduling"` → If no candidates passed threshold

**Logic**:
```python
if len(shortlisted_candidates) > 0:
    return "schedule_interviews"
else:
    return "skip_scheduling"
```

---

## 📊 Example Execution Results

### **Scenario 1: Some Candidates Shortlisted**
```
✅ Candidates extracted: 4
✅ Candidates enriched: 4
📊 Scoring Results:
   • Ashish Kumar: 8.2/10 → ✅ SHORTLISTED
   • Ashish Kumar: 9.2/10 → ✅ SHORTLISTED
   • Damanpreet Singh: 4.8/10 → ❌ REJECTED
   • Jane Doe: 9.2/10 → ✅ SHORTLISTED

🔀 ROUTING DECISION: 3 shortlisted → Proceeding to interview scheduling

📅 Interviews Scheduled: 3
📊 Sheets Created: 2 (All candidates + Interview schedule)
📅 Calendar Events: 3
```

### **Scenario 2: No Candidates Shortlisted**
```
✅ Candidates extracted: 4
✅ Candidates enriched: 4
📊 Scoring Results:
   • All candidates: Score < 5.0 → ❌ REJECTED

🔀 ROUTING DECISION: No shortlisted candidates → Skipping scheduling

⚠️ NO INTERVIEWS SCHEDULED
📊 Sheets Created: 1 (All candidates only)
📅 Calendar Events: 0
```

---

## 🛠️ Usage

### **Run the Pipeline**
```python
python ai_recruiter_pipeline.py
```

### **Customize Parameters**
```python
from ai_recruiter_pipeline import run_complete_pipeline

result = run_complete_pipeline(
    check_gmail=True,           # Check Gmail for new resumes
    max_emails=10,              # Check last 10 emails
    min_score_threshold=6.0     # Require score >= 6.0 for shortlisting
)
```

### **Visualize the Graph**
```python
from ai_recruiter_pipeline import create_recruitment_pipeline, visualize_pipeline

pipeline = create_recruitment_pipeline()
visualize_pipeline(pipeline, save_path="my_graph.png")
```

---

## 📈 Output Files

### **Always Created**
1. `enhanced_candidates_TIMESTAMP.json` - All enriched candidate data
2. Google Sheet - All candidates applied

### **Conditionally Created** (if shortlisted candidates exist)
3. Google Sheet - Interview schedule (shortlisted only)
4. `Scheduled_Interviews_TIMESTAMP.csv` - Interview schedule CSV
5. `recruitment_pipeline_graph.png` - Visual workflow diagram

---

## 🎨 Graph Visualization Details

The pipeline automatically generates a **Mermaid diagram** showing:

✅ All nodes (gmail_monitor, extract_resumes, etc.)
✅ Sequential edges (→)
✅ Conditional edges (◆ decision diamond)
✅ Routing paths based on conditions
✅ End state

**Image Format**: PNG (can be opened in any image viewer)
**Generation**: Automatic on each run
**Location**: `recruitment_pipeline_graph.png` in project root

---

## 🚀 Advanced Features

### **1. Multi-Path Execution**
- Pipeline handles both success and failure scenarios
- No candidates shortlisted? Pipeline completes gracefully
- All candidates shortlisted? Full automation kicks in

### **2. Error Resilience**
- Errors tracked in state
- Pipeline continues even if one step partially fails
- Final report shows all errors encountered

### **3. Extensibility**
- Easy to add more conditional nodes
- Can add additional enrichment strategies
- Can implement custom scoring logic

### **4. State Inspection**
- Full state available at end
- Can inspect intermediate results
- Debugging-friendly architecture

---

## 🔍 Debugging

View detailed routing decisions:
```bash
python ai_recruiter_pipeline.py | grep "ROUTING DECISION"
```

Check scores and classifications:
```bash
python ai_recruiter_pipeline.py | grep "SHORTLISTED\|REJECTED"
```

---

## 📦 Dependencies

```bash
langgraph>=0.6.10
langchain>=0.3.27
langchain-groq>=0.3.8
composio-langchain
google-auth
```

Install visualization dependencies (optional):
```bash
pip install pygraphviz
pip install IPython
```

---

## ✨ Summary

This is a **production-ready, intelligent recruitment pipeline** with:
- ✅ Conditional routing based on AI scoring
- ✅ Multi-strategy enrichment (LinkedIn + LLM)
- ✅ Automatic decision-making
- ✅ Comprehensive output tracking
- ✅ Visual workflow representation
- ✅ Error-resilient architecture

The pipeline demonstrates advanced LangGraph features including conditional edges, state management, and intelligent routing! 🎉
