# 🚀 AI Recruiter Copilot

> **Intelligent Recruitment Automation with LangGraph & Composio**  
> Transform your hiring process with an AI-powered pipeline that automatically processes resumes, enriches profiles, scores candidates, schedules interviews, and maintains organized records.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6.10-green.svg)](https://github.com/langchain-ai/langgraph)
[![Composio](https://img.shields.io/badge/Composio-0.8.20-orange.svg)](https://composio.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🏆 **Winner:** "Best Idea Award" at Composio Agents in Production Hackathon

> **[🔥 View the Interactive Showcase Website (Next.js)](./showcase)**  
> *A premium visual frontend designed to present the AI Recruiter pipeline, workflow architecture, and execution demo for portfolio and case-study purposes.*

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Hackathon Compliance](#-hackathon-compliance)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 🎯 Overview

### The Problem

Traditional recruitment is painfully slow and manual:
- ⏱️ **Hours** spent manually screening resumes
- 📧 **Tedious** email monitoring and file downloads
- 🔍 **Repetitive** LinkedIn research for each candidate
- 📊 **Error-prone** data entry into spreadsheets
- 📅 **Time-consuming** interview scheduling

### The Solution

**AI Recruiter Copilot** automates the entire recruitment pipeline using:
- **LangGraph** for intelligent workflow orchestration with conditional routing
- **Composio** for seamless Gmail, LinkedIn, Google Calendar & Sheets integration
- **Groq AI** for candidate scoring and profile enrichment

### What It Does

1. ✅ **Monitors Gmail** for incoming resumes (24/7 automation)
2. ✅ **Extracts & Parses** PDF/text resumes automatically
3. ✅ **Enriches Profiles** with LinkedIn data + AI analysis (dual strategy)
4. ✅ **Scores Candidates** with customizable AI criteria
5. ✅ **Conditional Routing** - Only qualified candidates proceed to scheduling
6. ✅ **Schedules Interviews** in Google Calendar automatically
7. ✅ **Exports to Google Sheets** - 2 separate spreadsheet files: all candidates + scheduled interviews
8. ✅ **Generates Reports** - JSON & CSV exports for analysis

---

## ✨ Key Features

### 🤖 **Intelligent Automation**
- **LangGraph State Machine**: Advanced workflow with conditional branching
- **Dual Enrichment Strategy**: LinkedIn API → LLM fallback for reliability
- **Smart Routing**: Candidates automatically filtered by score threshold
- **Error Handling**: Graceful fallbacks and informative error messages

### 🔗 **Seamless Integrations**
- **Gmail**: Automatic resume downloads via Composio
- **LinkedIn**: Real profile data enrichment (when available)
- **Google Calendar**: Automated interview scheduling
- **Google Sheets**: Dual-sheet export (all candidates + interviews)
- **Groq AI**: Fast, accurate candidate scoring and enrichment

### 📊 **Comprehensive Output**
- **JSON Database**: Complete candidate data with enrichment metadata
- **Google Sheets** (TWO separate spreadsheet files): 
  - First Sheet: "AI_Recruiter_Database" - All candidates with scores and status
  - Second Sheet: "Interview Schedule" - Shortlisted candidates with interview schedules
- **CSV Export**: Interview schedule for external tools
- **Calendar Events**: Direct Google Calendar links for each interview

### 🔒 **Security & Privacy**
- **No hardcoded secrets**: All credentials via environment variables
- **Secure authentication**: Composio OAuth flows for app connections
- **Type-safe configuration**: Pydantic models for validation
- **Error handling**: Graceful failures when credentials missing

---

## 🏗️ Architecture

### 🎨 **Visual Workflow**

Below is a high-level diagram of the complete AI Recruiter pipeline, from monitoring emails to scheduling interviews and exporting data.

![AI Recruiter Workflow Diagram](docs/images/workflow.png)

> You can also generate a real-time image of the graph by running:
> `python scripts/visualize_pipeline.py`

### LangGraph Workflow (8 Nodes with Conditional Routing)

```
┌─────────────────────────────────────────────────────────────┐
│                   AI RECRUITER PIPELINE                     │
│              (Advanced LangGraph State Machine)             │
│           ✨ Features Intelligent Conditional Routing ✨    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  📧 1. Gmail Monitor    │
              │  Auto-download resumes  │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  📄 2. Extract Resumes  │
              │  PDF/TXT → Structured   │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  🔗 3. Enrich Profiles  │
              │  LinkedIn API + LLM     │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  🤖 4. AI Scoring       │
              │  Groq Evaluation        │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ ⚡ 5. DECISION POINT    │
              │ Score >= Threshold?     │
              │ (Default: 5.0/10)       │
              └─────────────────────────┘
                 │                   │
          ✅ YES │                   │ ❌ NO
      (Shortlist)│                   │ (Reject)
                 ▼                   ▼
    ┌──────────────────┐   ┌──────────────────┐
    │ 📅 Schedule      │   │ ⏭️ Skip          │
    │ Calendar Events  │   │ Go to Export     │
    └──────────────────┘   └──────────────────┘
                 │                   │
                 └─────────┬─────────┘
                           ▼
              ┌──────────────────────────┐
              │ 📊 6. All Candidates     │
              │ Google Sheet (Everyone)  │
              └──────────────────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ 📅 7. Interview Schedule │
              │ Sheet (Shortlisted Only) │
              └──────────────────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ 📋 8. Final Report       │
              │ All Links & Summary      │
              └──────────────────────────┘
```

**Key Workflow Features:**
- ✅ **8 Distinct Nodes** - Each step clearly separated
- ✅ **Conditional Routing** - Only qualified candidates get interviews
- ✅ **Dual Strategy** - LinkedIn API with LLM fallback
- ✅ **Two Separate Spreadsheet Files** - All candidates + Selected interviews
- ✅ **Smart Decisions** - Threshold-based filtering

### Technology Stack

- **Workflow**: LangGraph 0.6.10 (State machine with conditional routing)
- **Integrations**: Composio (Gmail, LinkedIn, Calendar, Sheets)
- **AI Processing**: Groq (llama-3.1-8b-instant)
- **PDF Processing**: PyMuPDF (fitz)
- **Type Safety**: Pydantic v2 (Input validation)
- **Environment**: Python 3.11+

### 🔄 Workflow Execution Flow

Here's how the components work together in the pipeline:

```
📧 STEP 1: Gmail Monitor (auto_gmail_monitor.py)
   ├─ Search Gmail for unread emails
   ├─ Filter emails with attachments
   ├─ Download PDFs to incoming_resumes/
   └─ Return: List of resume file paths
                    ↓
📄 STEP 2: Resume Extraction (pdf_extractor.py)
   ├─ Read PDF files using PyMuPDF
   ├─ Send text to Groq AI for parsing
   ├─ Extract: name, email, skills, experience
   └─ Return: List of candidate dictionaries
                    ↓
🔗 STEP 3: Profile Enrichment (linkedin_enricher.py)
   ├─ Try LinkedIn API via Composio (if available)
   ├─ Fallback to Groq LLM for inference
   ├─ Add: company history, education, certifications
   └─ Return: Enhanced candidate profiles
                    ↓
🤖 STEP 4: AI Scoring (candidate_scorer.py)
   ├─ Send profile + criteria to Groq AI
   ├─ Get score (0-10) + reasoning
   ├─ Add metadata: timestamp, criteria used
   └─ Return: Scored candidates
                    ↓
⚡ STEP 5: DECISION POINT (conditional routing in pipeline)
   ├─ IF score >= threshold (default 5.0)
   │   └─ Route to: Interview Scheduling
   └─ ELSE
       └─ Route to: Skip scheduling, go to export
                    ↓
📅 STEP 6: Interview Scheduling (interview_scheduler.py)
   ├─ For each shortlisted candidate:
   ├─ Create Google Calendar event via Composio
   ├─ Set duration, time slot, description
   └─ Return: Event IDs and calendar links
                    ↓
📊 STEP 7: All Candidates Sheet (google_sheets_manager.py)
   ├─ Create "AI_Recruiter_Database" Google Sheet
   ├─ Add ALL candidates (shortlisted + rejected)
   ├─ Include: scores, skills, status, rationale
   └─ Return: Shareable Google Sheets URL
                    ↓
📅 STEP 8: Interview Schedule Sheet (recruitment_agent.py)
   ├─ Create separate "Interview Schedule" Google Sheet
   ├─ Add ONLY shortlisted candidates
   ├─ Include: interview times, calendar links, rationale
   ├─ Export CSV: Interview schedule for external tools
   ├─ Generate JSON: Complete candidate database
   └─ Return: All URLs and file paths
```

**Key Points:**
- 🎯 **8 Sequential Steps** - Clear data flow from email to report
- 🔀 **1 Decision Point** - Conditional routing at step 5 (scoring threshold)
- 📝 **Each Step** - Uses specific utility file (see Component Details below)
- 🔗 **Orchestration** - Steps 4-5 use `recruitment_agent.py` (scoring + scheduling)
- 🚀 **Main Controller** - `ai_recruiter_pipeline.py` manages entire LangGraph workflow
- 📊 **Google Sheets Output** - 2 separate files:
  - `google_sheets_manager.py` → ALL candidates database
  - `recruitment_agent.py` → Interview schedule (shortlisted only)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Composio account with connected apps (Gmail, Google Calendar, Google Sheets)
- Groq API key
- Git (for cloning)

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/AshParmar/horizon-latex.git
cd horizon-latex

# Create and activate virtual environment
python -m venv comp
.\comp\Scripts\Activate.ps1  # Windows
# source comp/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
notepad .env  # Windows
# nano .env   # Linux/Mac
```

### 3. Validate Configuration

```bash
# Test your configuration
python scripts/validate_config.py
```

### 4. Run the Pipeline

```bash
# Activate environment (if not already active)
.\comp\Scripts\Activate.ps1

# Run the complete pipeline
python ai_recruiter_pipeline.py
```

### Expected Output

```
✅ Pipeline execution finished with status: complete

Summary:
  • Resumes downloaded: 6
  • Candidates extracted: 6
  • Candidates enriched: 6
  • ✅ Shortlisted: 4
  • ❌ Rejected: 2
  • 📅 Interviews scheduled: 4

OUTPUT FILES:
  • JSON: output/enhanced_candidates_20251021_155421.json
  • Google Sheet File #1 (All Candidates): https://docs.google.com/spreadsheets/d/... 
  • Google Sheet File #2 (Interview Schedule): https://docs.google.com/spreadsheets/d/...
  • CSV: output/Scheduled_Interviews_20251021_155604.csv
  • Calendar Events: 4 interviews created

📌 NOTE: Two separate Google Sheets **files** are created (not tabs in one sheet):
   - First Spreadsheet: "AI_Recruiter_Database" (ALL candidates with scores/status)
   - Second Spreadsheet: "Interview Schedule" (ONLY shortlisted candidates with calendar links)
```

---

## 📦 Installation

### ⚠️ READ THIS FIRST

**Critical:** This project uses **Composio SDK v0.8.20** with `ComposioToolSet` API.  
**DO NOT** install newer versions as they have incompatible APIs.

👉 **[Follow INSTALLATION.md for complete setup guide](INSTALLATION.md)**

### Quick Installation (For Experienced Users)

#### 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/AshParmar/horizon-latex.git
cd horizon-latex
python -m venv comp
source comp/bin/activate  # On Windows: .\comp\Scripts\Activate.ps1
```

#### 2. Install Exact Dependency Versions

```bash
pip install -r requirements.txt
```

**Verify Composio version:**
```bash
python -c "from composio import ComposioToolSet; print('✅ Ready')"
```

If you get `ImportError`, you have wrong version:
```bash
pip install composio==0.8.20 --force-reinstall
```

#### 3. Set Up Composio Integrations

Follow our [detailed setup guide](docs/API_KEYS_SETUP.md) to connect:

1. **Gmail** - For resume monitoring
2. **Google Calendar** - For interview scheduling
3. **Google Sheets** - For data export
4. **LinkedIn** (Optional) - For profile enrichment

#### 4. Get API Keys

- **Composio API Key**: [composio.dev/app](https://composio.dev/app)
- **Groq API Key**: [console.groq.com/keys](https://console.groq.com/keys)

#### 5. Configure Environment Variables

See [Configuration](#️-configuration) section below.

### Common Installation Issues

| Error | Solution |
|-------|----------|
| `cannot import ComposioToolSet` | Run: `pip install composio==0.8.20 --force-reinstall` |
| `'Composio' object has no attribute 'execute_action'` | Wrong version! Reinstall: `pip install composio==0.8.20` |
| `ModuleNotFoundError: composio` | Activate virtual environment and run `pip install -r requirements.txt` |

**For complete troubleshooting, see [INSTALLATION.md](INSTALLATION.md)**

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# ============================================================================
# CORE API KEYS (Required)
# ============================================================================

# Composio API Key - Get from https://composio.dev/app
COMPOSIO_API_KEY=your_composio_api_key_here

# Groq API Key - Get from https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# ============================================================================
# GMAIL CONFIGURATION (Required for resume monitoring)
# ============================================================================

# Gmail Account Details
GMAIL_ACCOUNT_ID=your_gmail_connected_account_id
GMAIL_USER_ID=your_gmail_entity_id
GMAIL_AUTH_CONFIG_ID=your_gmail_auth_config_id

# ============================================================================
# GOOGLE CALENDAR CONFIGURATION (Required for interview scheduling)
# ============================================================================

GOOGLE_CALENDAR_ACCOUNT_ID=your_calendar_account_id
GOOGLE_CALENDAR_USER_ID=your_calendar_entity_id
GOOGLE_CALENDAR_AUTH_CONFIG_ID=your_calendar_auth_config_id

# ============================================================================
# GOOGLE SHEETS CONFIGURATION (Required for data export)
# ============================================================================

GOOGLE_SHEETS_ACCOUNT_ID=your_sheets_account_id
GOOGLE_SHEETS_USER_ID=your_sheets_entity_id
GOOGLE_SHEETS_AUTH_CONFIG_ID=your_sheets_auth_config_id

# ============================================================================
# LINKEDIN CONFIGURATION (Optional - for profile enrichment)
# ============================================================================

LINKEDIN_CONNECTED_ACCOUNT_ID=your_linkedin_account_id
LINKEDIN_ENTITY_ID=your_linkedin_entity_id
```

### Getting Composio IDs

Get your Composio connection IDs from the [Composio Dashboard](https://composio.dev/app):

1. Go to "Integrations"
2. Click on each connected app (Gmail, Calendar, Sheets, LinkedIn)
3. Copy the following for each app:
   - **Connected Account ID** (e.g., `123e4567-e89b-12d3-a456-426614174000`)
   - **Entity ID** (your user/entity identifier)
   - **Auth Config ID** (authentication configuration ID)
4. Paste these values into your `.env` file

### Customization

Edit these parameters in `ai_recruiter_pipeline.py`:

```python
def main():
    result = run_complete_pipeline(
        check_gmail=True,           # Enable Gmail monitoring
        max_emails=10,              # Number of emails to check
        min_score_threshold=5.0     # Minimum score for shortlisting
    )
```

---

## 📘 Usage

### Basic Usage

```bash
# Run complete pipeline
python ai_recruiter_pipeline.py
```

### Advanced Usage

#### Custom Scoring Criteria

Edit `src/utils/candidate_scorer.py`:

```python
DEFAULT_CRITERIA = {
    "role": "Senior Software Engineer",
    "required_skills": ["Python", "LangChain", "AI/ML"],
    "min_experience_years": 5,
    "preferred_skills": ["LangGraph", "Composio"],
    # ... customize as needed
}
```

#### Process Specific Files

```python
from src.utils.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
candidates = extractor.extract_from_directory("path/to/resumes")
```

#### Visualize Workflow

```bash
python scripts/visualize_pipeline.py
```

This generates:
- ASCII graph in terminal
- PNG image: `output/recruitment_pipeline_graph.png`

---

## 📁 Project Structure

```
Composio_AI_Recruiter_Copilot/
├── ai_recruiter_pipeline.py    # Main entry point (LangGraph workflow)
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── src/                         # Source code (organized by layer)
│   ├── agents/                  # Business orchestrators
│   │   └── recruitment_agent.py # Coordinates scoring + scheduling + export
│   │
│   ├── utils/                   # Single-purpose utilities
│   │   ├── auto_gmail_monitor.py    # Gmail integration
│   │   ├── pdf_extractor.py         # Resume parsing
│   │   ├── linkedin_enricher.py     # Profile enrichment
│   │   ├── candidate_scorer.py      # AI scoring
│   │   ├── interview_scheduler.py   # Calendar integration
│   │   └── google_sheets_manager.py # Sheets export
│   │
│   └── config/                  # Configuration management
│       ├── settings.py          # Pydantic models (type-safe)
│       ├── legacy_config.py     # Environment variable loading
│       └── validator.py         # Configuration validation
│
├── scripts/                     # Utility scripts
│   ├── validate_config.py       # Test configuration
│   └── visualize_pipeline.py    # Generate workflow diagram
│
├── output/                      # Generated files
│   ├── enhanced_candidates_*.json
│   ├── Scheduled_Interviews_*.csv
│   └── recruitment_pipeline_graph.png
│
├── incoming_resumes/            # Resume PDFs (downloaded from Gmail)
├── processed_candidates/        # Parsed resume data (JSON)
├── examples/                    # Sample data for testing
└── docs/                        # Comprehensive documentation
```

### 🔍 Component Details

#### **Main Workflow** (`ai_recruiter_pipeline.py`)
The heart of the system - a LangGraph state machine that orchestrates all components:
- **What it does**: Defines 8 workflow nodes and manages state transitions
- **Key features**: 
  - Conditional routing based on candidate scores
  - Error handling and state persistence
  - Parallel processing where possible
- **State management**: Uses TypedDict to track candidates through each stage
- **Output**: Complete pipeline execution with all candidate data

#### **Business Orchestrator** (`src/agents/recruitment_agent.py`)
Coordinates scoring, scheduling, and creates the interview schedule sheet:
- **What it does**: Manages scoring, scheduling calendar events, and creating interview sheet
- **Key features**:
  - Batch processing of candidates with AI scoring
  - Threshold-based filtering (only shortlisted get interviews)
  - Creates Google Calendar events for shortlisted candidates
  - Creates "Interview Schedule" Google Sheet (shortlisted only with calendar links)
- **Used by**: Main pipeline for steps 4-5 (scoring + scheduling) and step 6B (interview sheet)
- **Note**: This creates the SECOND Google Sheet (not google_sheets_manager.py)

#### **📊 File Interaction Diagram**

Here's how the files work together:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      FILE ARCHITECTURE                               │
└─────────────────────────────────────────────────────────────────────┘

                    ai_recruiter_pipeline.py (Main Entry)
                            │
                            │ orchestrates
                            ▼
        ┌───────────────────┴───────────────────┐
        │                                       │
        │         LangGraph Workflow            │
        │    (State Machine with 8 Nodes)       │
        │                                       │
        └───────────────────┬───────────────────┘
                            │
                            │ calls utilities & orchestrator
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐   ┌──────────────────┐   ┌──────────────┐
│   UTILS     │   │   ORCHESTRATOR   │   │   CONFIG     │
│  (Step 1-3) │   │   (Step 4-8)     │   │  (Settings)  │
└─────────────┘   └──────────────────┘   └──────────────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼

┌────────────────────────────────────────────────────────┐
│  STEP 1-3: Independent Utilities                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  📧 auto_gmail_monitor.py                              │
│     └─> Composio Gmail API                             │
│     └─> Downloads to: incoming_resumes/                │
│                                                        │
│  📄 pdf_extractor.py                                   |
│     └─> PyMuPDF (fitz)                                 │
│     └─> Groq AI for parsing                            │
│     └─> Saves to: processed_candidates/                │
│                                                        │
│  🔗 linkedin_enricher.py                               │
│     └─> Composio LinkedIn API (primary)                │
│     └─> Groq LLM (fallback)                            │
│                                                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  STEP 4-8: Orchestrated via recruitment_agent.py       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  recruitment_agent.py (Orchestrator)                   │
│     ├─> Coordinates scoring + scheduling + export:     │
│     │                                                  │
│     ├─> 🤖 candidate_scorer.py                         │
│     │      └─> Groq AI evaluation                      │
│     │                                                  │
│     ├─> 📅 interview_scheduler.py                      │
│     │      └─> Composio Google Calendar                │
│     │      └─> Creates calendar events (shortlisted)   │
│     │                                                  │
│     └─> 📊 Creates "Interview Schedule" Sheet          │
│            └─> Composio Google Sheets                  │
│            └─> ONLY shortlisted with interview times   │
│                                                        │
│  📊 google_sheets_manager.py (Independent Utility)     │
│     └─> Creates "AI_Recruiter_Database" Sheet         │
│     └─> ALL candidates (shortlisted + rejected)        │
│                                                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  CONFIGURATION: Loaded by all components               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  src/config/                                           │
│     ├─> settings.py (Pydantic models)                  │
│     ├─> legacy_config.py (loads .env)                  │
│     └─> validator.py (validates setup)                 │
│                                                        │
│  Environment Variables (.env)                          │
│     ├─> COMPOSIO_API_KEY                               │
│     ├─> GROQ_API_KEY                                   │
│     ├─> GMAIL_* (3 variables)                          │
│     ├─> GOOGLE_CALENDAR_* (3 variables)                │
│     ├─> GOOGLE_SHEETS_* (3 variables)                  │
│     └─> LINKEDIN_* (2 variables, optional)             │
│                                                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  OUTPUT: Generated by pipeline execution               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  output/                                               │
│     ├─> enhanced_candidates_*.json                     │
│     ├─> Scheduled_Interviews_*.csv                     │
│     └─> recruitment_pipeline_graph.png                 │
│                                                        │
│  Google Services (via Composio)                        │
│     ├─> Google Sheets (2 separate spreadsheet files)   │
│     └─> Google Calendar (interview events)             │
│                                                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  UTILITIES: Helper Scripts                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  scripts/validate_config.py                            │
│     └─> Tests all API keys and connections             │
│                                                        │
│  scripts/visualize_pipeline.py                         │
│     └─> Generates workflow diagram (ASCII + PNG)       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Key Points:**
- ✅ **Single entry point**: `ai_recruiter_pipeline.py` orchestrates everything
- ✅ **Independent utilities**: Steps 1-3 are standalone and reusable
- ✅ **Coordinated orchestration**: Steps 4-8 managed by `recruitment_agent.py`
- ✅ **Centralized config**: All files load from `src/config/`
- ✅ **Clear data flow**: Each component has defined inputs/outputs

#### **Utilities** (`src/utils/`)

1. **`auto_gmail_monitor.py`** - Gmail Integration
   - **What it does**: Monitors Gmail for unread emails with resume attachments
   - **How it works**: 
     - Uses Composio Gmail actions to search unread emails
     - Downloads PDF/TXT attachments to `incoming_resumes/`
     - Marks processed emails as read
   - **Output**: List of downloaded resume file paths

2. **`pdf_extractor.py`** - Resume Parser
   - **What it does**: Extracts structured data from PDF/text resumes
   - **How it works**:
     - Uses PyMuPDF (fitz) to extract text from PDFs
     - Sends text to Groq AI for structured extraction
     - Parses JSON response into candidate objects
   - **Output**: Candidate dictionaries with name, email, skills, experience

3. **`linkedin_enricher.py`** - Profile Enrichment
   - **What it does**: Enriches candidate profiles with LinkedIn data
   - **How it works**:
     - **Strategy 1**: Try Composio LinkedIn API for real profile data
     - **Strategy 2**: If API fails, use Groq LLM to infer additional details
     - Adds company history, education, certifications
   - **Output**: Enhanced candidate profiles with enrichment metadata

4. **`candidate_scorer.py`** - AI Scoring Engine
   - **What it does**: Scores candidates against job requirements using AI
   - **How it works**:
     - Takes candidate profile + scoring criteria as input
     - Sends to Groq AI with detailed prompt for evaluation
     - Parses AI response for score (0-10) and reasoning
   - **Output**: Score + detailed evaluation explanation

5. **`interview_scheduler.py`** - Calendar Integration
   - **What it does**: Creates Google Calendar events for interviews
   - **How it works**:
     - Uses Composio Google Calendar actions
     - Schedules events with candidate details in description
     - Sets default duration (45 min) and time slots
   - **Output**: Calendar event IDs and links

6. **`google_sheets_manager.py`** - All Candidates Sheet Export
   - **What it does**: Creates ONE Google Sheets file with ALL candidate data (complete database)
   - **How it works**:
     - **"AI_Recruiter_Database" Spreadsheet**: All candidates with scores, skills, experience, and status
     - Uses Composio Google Sheets actions to create spreadsheet file
   - **Output**: One shareable Google Sheets URL with complete candidate database
   - **Note**: This is the main database sheet for all applicants (shortlisted + rejected)

#### **Configuration** (`src/config/`)

1. **`settings.py`** - Type-Safe Models
   - Pydantic models for configuration validation
   - Ensures all required environment variables are present
   - Provides type hints for IDE support

2. **`legacy_config.py`** - Environment Loading
   - Loads environment variables from `.env` file
   - Provides backward compatibility
   - Exports configuration dictionaries

3. **`validator.py`** - Config Validation
   - Tests API key validity
   - Checks Composio connections
   - Used by `scripts/validate_config.py`

### 🔗 How Everything Connects

Now that you understand each component, here's how they work together:

```
MAIN ENTRY POINT: ai_recruiter_pipeline.py
│
├─ Defines LangGraph workflow with 8 nodes
├─ Manages state transitions between steps
├─ Handles conditional routing logic
│
└─ CALLS COMPONENTS:
    │
    ├─ STEP 1: auto_gmail_monitor.py
    │   └─ Downloads resumes from Gmail → Returns file paths
    │
    ├─ STEP 2: pdf_extractor.py
    │   └─ Parses PDFs with AI → Returns candidate dicts
    │
    ├─ STEP 3: linkedin_enricher.py
    │   └─ Enriches profiles (API + LLM) → Returns enhanced data
    │
    ├─ STEP 4-8: recruitment_agent.py (ORCHESTRATOR)
    │   │
    │   ├─ candidate_scorer.py
    │   │   └─ Scores candidates → Returns scores + reasoning
    │   │
    │   ├─ DECISION: score >= threshold?
    │   │   ├─ YES → interview_scheduler.py
    │   │   │        └─ Creates calendar events (shortlisted only)
    │   │   └─ NO → Skip scheduling
    │   │
    │   └─ recruitment_agent.py ALSO creates:
    │       └─ "Interview Schedule" Google Sheet (shortlisted only)
    │
    ├─ STEP 6A: google_sheets_manager.py (CALLED BY PIPELINE)
    │   └─ Creates "All Candidates Database" sheet (everyone)
    │
    ├─ STEP 6B: recruitment_agent.py (CALLED BY PIPELINE)
    │   └─ Creates "Interview Schedule" sheet (shortlisted + calendar info)
    │
    └─ RETURNS: Complete results with all URLs and stats
```

**Key Integration Rules:**
- ✅ **Steps 1-3**: Independent utilities, can be tested standalone
- ✅ **Steps 4-5**: Orchestrated by `recruitment_agent.py` (scoring + scheduling)
- ✅ **Step 6A**: `google_sheets_manager.py` creates ALL candidates sheet
- ✅ **Step 6B**: `recruitment_agent.py` creates SHORTLISTED interview sheet
- ✅ **All steps**: Load configuration from `src/config/`
- ✅ **State flow**: Each step receives output from previous step via TypedDict
- ✅ **Error handling**: Each component has fallback strategies

**File Responsibility Summary:**
- `ai_recruiter_pipeline.py` → **Workflow orchestrator** (defines the 8-node graph)
- `recruitment_agent.py` → **Business orchestrator** (scoring + scheduling + interview sheet)
- `auto_gmail_monitor.py` → **Data ingestion** (gets resumes)
- `pdf_extractor.py` → **Data extraction** (parses resumes)
- `linkedin_enricher.py` → **Data enrichment** (adds profile details)
- `candidate_scorer.py` → **Evaluation** (AI scoring)
- `interview_scheduler.py` → **Calendar automation** (creates calendar events for shortlisted)
- `google_sheets_manager.py` → **Database export** (creates ALL candidates sheet)

---

## ✅ Hackathon Compliance

### Technical Conventions (7/7 Requirements Met)

#### 1. ✅ **Project Structure**
- Standard `src/` organization with `agents/`, `utils/`, and `config/`
- Comprehensive `.env.example` with all variables documented (140+ lines)
- No bundled monorepos or unnecessary boilerplate
- Clean separation of concerns (workflow, orchestration, utilities, config)

#### 2. ✅ **Code Quality**
- **Modular code**: Each file has single responsibility
- **Descriptive names**: `enrich_candidate_profile()`, not `process()`
- **Comments**: Complex sections documented with inline comments
- **Functions/Classes**: Encapsulated logic with clear interfaces
- **No hardcoded secrets**: All credentials from environment variables

#### 3. ✅ **Error Handling**
- Input validation with Pydantic models
- Graceful API error handling with try/except blocks
- Informative error messages with logging
- Fallback strategies:
  - LinkedIn API fails → LLM enrichment
  - Primary Gmail method fails → Tries alternative actions
  - Scoring AI unavailable → Heuristic fallback

#### 4. ✅ **Type Safety**
- Python type hints throughout (TypedDict, List[Dict], Optional, Literal)
- Pydantic models for configuration validation (`src/config/settings.py`)
- Input/output schemas defined with Pydantic
- Strong typing for LangGraph state machine

#### 5. ✅ **Documentation**
- **Comprehensive README**: This file (900+ lines)
- **Setup guides**: Step-by-step in `docs/SETUP_GUIDE.md`
- **API documentation**: `docs/API_KEYS_SETUP.md`
- **Testing guide**: `docs/TESTING_GUIDE.md`
- **Inline comments**: Complex sections explained in code
- **Examples**: Sample inputs/outputs in `examples/`

#### 6. ✅ **Testing & Reliability**
- Sample data provided (`examples/sample_candidates.json`)
- Configuration validator (`scripts/validate_config.py`)
- Clear authentication documentation
- Graceful failures with missing credentials
- Tested with fresh installations

#### 7. ✅ **Security & Privacy**
- No hardcoded tokens or personal data
- Composio OAuth flows for secure app connections
- `.env` in `.gitignore`
- Clear warnings about credential security
- Best practices documented

---

## 📚 Documentation

### Core Documentation

- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Complete setup instructions
- **[API_KEYS_SETUP.md](docs/API_KEYS_SETUP.md)** - API key configuration
- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Testing procedures
- **[GRAPH_VISUALIZATION_GUIDE.md](docs/GRAPH_VISUALIZATION_GUIDE.md)** - Workflow visualization

### Technical Deep Dives

- **[TRANSFORMATION_SUMMARY.md](docs/TRANSFORMATION_SUMMARY.md)** - Before/After comparison
- **[COMPLETE_GRAPH_SUMMARY.md](docs/COMPLETE_GRAPH_SUMMARY.md)** - Workflow details
- **[ADVANCED_LANGGRAPH_PIPELINE.md](docs/ADVANCED_LANGGRAPH_PIPELINE.md)** - Architecture

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Validate configuration
python scripts/validate_config.py

# Test the pipeline
python ai_recruiter_pipeline.py

# Visualize workflow
python scripts/visualize_pipeline.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎨 Workflow Visualization

Want to dive deeper into the workflow? We have **multiple visualization formats** for different needs:

### 🖼️ **Generate Visual Graphs**

Run the visualization script to generate comprehensive diagrams:

```bash
python scripts/visualize_pipeline.py
```

**What you get:**
- ✅ **ASCII Diagram** - Printed in terminal with all 8 nodes
- ✅ **PNG Image** - Saved to `output/recruitment_pipeline_graph.png`
- ✅ **Detailed Breakdown** - Node descriptions, inputs, outputs
- ✅ **Conditional Routing** - Shows decision points and paths
- ✅ **Example Execution** - Step-by-step walkthrough with sample data

**Output Preview:**
```
AI RECRUITER COPILOT - LANGGRAPH WORKFLOW VISUALIZATION
================================================================================

VISUAL GRAPH (ASCII):
--------------------------------------------------------------------------------
[Shows complete LangGraph with all nodes and edges]

DETAILED NODE BREAKDOWN:
  • gmail_monitor → extract_resumes → linkedin_enrich → score_candidates
  • DECISION POINT at score_candidates (threshold-based routing)
  • Two paths: schedule_interviews OR skip to sheets
  • Convergence at create_all_candidates_sheet
  • Final nodes: create_interview_sheet → final_report

CONDITIONAL ROUTING LOGIC:
  IF shortlisted > 0 → schedule_interviews → all sheets → report
  ELSE → skip scheduling → all sheets → report

OUTPUT FILES GENERATED:
  ✅ JSON: enhanced_candidates_*.json (always)
  ✅ Google Sheet: All Candidates (always)
  ✅ Google Sheet: Interviews (conditional)
  ✅ CSV: Scheduled_Interviews_*.csv (conditional)
  ✅ Calendar Events (conditional)
```

### 📊 **Documentation Guides**

For in-depth explanations, check our comprehensive documentation:

1. **[Graph Visualization Guide](docs/GRAPH_VISUALIZATION_GUIDE.md)** (314 lines)
   - Complete ASCII diagram with all 8 nodes
   - Shows conditional routing with dotted lines
   - Explains each node's purpose
   - Legend for understanding the graph

2. **[Advanced Pipeline Details](docs/ADVANCED_LANGGRAPH_PIPELINE.md)** (361 lines)
   - Deep dive into conditional routing logic
   - State management explained
   - Decision point analysis
   - Fallback strategies documented

3. **[Complete Graph Summary](docs/COMPLETE_GRAPH_SUMMARY.md)** (279 lines)
   - Before/After comparison
   - Shows what makes this "advanced"
   - LinkedIn enrichment strategy
   - Dual-sheet export explanation

### 🖼️ **Generate Your Own Graph**

```bash
# Run the visualization script
python scripts/visualize_pipeline.py

# Output:
# - ASCII diagram in terminal
# - PNG image: output/recruitment_pipeline_graph.png
```

The generated graph shows:
- ✅ All 8 nodes clearly labeled
- ✅ Conditional edges (dotted lines)
- ✅ Sequential edges (solid lines)
- ✅ Decision points highlighted

---

## 🙏 Acknowledgments

- **LangGraph** - For the powerful state machine framework
- **Composio** - For seamless third-party integrations
- **Groq** - For fast, accurate AI inference
- **Hackathon Organizers** - For the opportunity to build this

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AshParmar/horizon-latex/issues)
- **Documentation**: `docs/` folder
- **Email**: ashparmar08@gmail.com

---

<div align="center">

**Built with ❤️ for the Composio Hackathon**

[⭐ Star this repo](https://github.com/AshParmar/horizon-latex) | [📖 Documentation](docs/) | [🐛 Report Bug](https://github.com/AshParmar/horizon-latex/issues)

</div>
