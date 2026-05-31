"""
🚀 AI RECRUITER COPILOT - Advanced LangGraph Pipeline with Conditional Routing
End-to-end recruitment automation with intelligent decision-making

Pipeline Flow:
1. Monitor Gmail for resume attachments
2. Extract & parse resume data
3. Conditional Enrichment:
   - Try LinkedIn enrichment first
   - If fails → Fallback to LLM enrichment
4. Score candidates with AI
5. Conditional Scheduling:
   - If score >= threshold → Schedule interview
   - If score < threshold → Reject candidate
6. Export selected candidates to Google Sheets & CSV
"""

import os
import sys
from typing import TypedDict, List, Dict, Annotated, Literal
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# LangGraph imports
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# For graph visualization
try:
    from IPython.display import Image, display
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

# Import our modules from src/
from src.utils.auto_gmail_monitor import AutoGmailMonitor
from src.utils.pdf_extractor import PDFExtractor
from src.utils.linkedin_enricher import LinkedInEnricher
from src.utils.candidate_scorer import CandidateScorer, DEFAULT_CRITERIA
from src.utils.interview_scheduler import InterviewScheduler
from src.utils.google_sheets_manager import GoogleSheetsManager
from src.agents.recruitment_agent import RecruitmentAgent
from src.config.legacy_config import GROQ_API_KEY, GROQ_MODEL

load_dotenv()


# ============================================================================
# STATE DEFINITION
# ============================================================================

class RecruitmentState(TypedDict):
    """State that flows through the pipeline"""
    # Input
    check_gmail: bool
    max_emails: int
    min_score_threshold: float
    
    # Data collected through pipeline
    email_messages: List[Dict]
    downloaded_files: List[str]
    extracted_candidates: List[Dict]
    enriched_candidates: List[Dict]
    scored_candidates: List[Dict]
    shortlisted_candidates: List[Dict]
    rejected_candidates: List[Dict]
    scheduled_candidates: List[Dict]
    
    # Processing state
    current_candidate: Dict  # Currently processing candidate
    linkedin_success: bool  # Did LinkedIn enrichment work?
    
    # Output files and links
    sheets_url: str  # Main candidate database sheet
    interview_sheet_url: str  # Selected candidates interview schedule sheet
    csv_file: str
    json_file: str
    calendar_links: List[str]  # Individual calendar event links
    
    # Status
    status: str
    errors: List[str]


# ============================================================================
# PIPELINE NODES (Each represents a modular component)
# ============================================================================

def gmail_monitor_node(state: RecruitmentState) -> RecruitmentState:
    """Node 1: Monitor Gmail for resume attachments"""
    print("\n" + "="*60)
    print("📧 STEP 1: Gmail Monitoring")
    print("="*60)
    
    if not state.get("check_gmail", True):
        print("⏭️  Skipping Gmail check")
        return {**state, "email_messages": [], "status": "gmail_skipped"}
    
    try:
        # Initialize Gmail monitor
        gmail = AutoGmailMonitor()
        
        # Auto-monitor and download attachments
        downloaded = gmail.auto_monitor_and_download(max_emails=state.get("max_emails", 10))
        
        print(f"📥 Downloaded {len(downloaded)} resume(s)")
        
        return {
            **state,
            "email_messages": [],  # Not needed for this flow
            "downloaded_files": downloaded,
            "status": "gmail_complete"
        }
        
    except Exception as e:
        print(f"❌ Gmail monitoring failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Gmail: {str(e)}")
        return {**state, "errors": errors, "status": "gmail_failed"}


def extract_resumes_node(state: RecruitmentState) -> RecruitmentState:
    """Node 2: Extract & parse resume data"""
    print("\n" + "="*60)
    print("📄 STEP 2: Resume Extraction & Parsing")
    print("="*60)
    
    try:
        extractor = PDFExtractor()
        candidates = extractor.extract_from_directory()
        
        print(f"✅ Extracted {len(candidates)} candidate(s)")
        
        return {
            **state,
            "extracted_candidates": candidates,
            "status": "extraction_complete"
        }
        
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Extraction: {str(e)}")
        return {**state, "errors": errors, "status": "extraction_failed"}


def try_linkedin_enrichment_node(state: RecruitmentState) -> RecruitmentState:
    """Node 3: LinkedIn API + LLM Enrichment (Dual Strategy)"""
    print("\n" + "="*60)
    print("🔗 STEP 3: LinkedIn Enrichment (API + LLM Fallback)")
    print("="*60)
    
    try:
        candidates = state.get("extracted_candidates", [])
        
        if not candidates:
            print("⚠️  No candidates to enrich")
            return {**state, "enriched_candidates": [], "status": "no_candidates"}
        
        enricher = LinkedInEnricher()
        enriched = []
        
        for candidate in candidates:
            name = candidate.get('name', candidate.get('full_name', 'Unknown'))
            print(f"\n🔗 Enriching: {name}")
            
            # Enrich with dual strategy (LinkedIn API attempt + LLM enrichment)
            enriched_candidate = enricher.enrich_candidate_profile(candidate)
            
            # Check what enrichment source was used
            linkedin_source = enriched_candidate.get('linkedin_source', 'unknown')
            
            if linkedin_source == 'api_verified':
                print(f"   ✅ Enriched with: LinkedIn API (verified) + LLM")
                enriched_candidate['enrichment_source'] = 'linkedin_api_verified'
            elif linkedin_source == 'api_unverified':
                print(f"   ✅ Enriched with: LinkedIn API (unverified) + LLM")
                enriched_candidate['enrichment_source'] = 'linkedin_api_partial'
            elif linkedin_source == 'llm_fallback':
                print(f"   ✅ Enriched with: LLM only (LinkedIn API failed)")
                enriched_candidate['enrichment_source'] = 'llm_fallback'
            else:
                print(f"   ✅ Enriched with: LLM only (no LinkedIn URL)")
                enriched_candidate['enrichment_source'] = 'llm_only'
            
            enriched.append(enriched_candidate)
        
        print(f"\n✅ Enriched {len(enriched)} candidate(s)")
        
        # Save enriched data to output folder
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = os.path.join("output", f"enhanced_candidates_{timestamp}.json")
        
        import json
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(enriched, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {json_file}")
        
        return {
            **state,
            "enriched_candidates": enriched,
            "json_file": json_file,
            "status": "enrichment_complete"
        }
        
    except Exception as e:
        print(f"❌ Enrichment failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Enrichment: {str(e)}")
        return {**state, "errors": errors, "status": "enrichment_failed"}


def score_candidates_node(state: RecruitmentState) -> RecruitmentState:
    """Node 4: Score candidates with AI and make selection decision"""
    print("\n" + "="*60)
    print("📊 STEP 4: Candidate Scoring & Selection")
    print("="*60)
    
    try:
        candidates = state.get("enriched_candidates", [])
        
        if not candidates:
            print("⚠️  No candidates to score")
            return {**state, "scored_candidates": [], "status": "no_candidates"}
        
        scorer = CandidateScorer()
        min_score = state.get("min_score_threshold", 6.0)
        
        # Score each candidate individually and categorize
        shortlisted = []
        rejected = []
        
        for candidate in candidates:
            score_result = scorer.score_single_candidate(candidate, DEFAULT_CRITERIA)
            candidate.update(score_result)
            
            name = candidate.get('name', candidate.get('full_name', 'Unknown'))
            score = score_result.get('score', 0)
            
            print(f"📊 {name}: {score}/10")
            
            # Decision logic
            if score >= min_score:
                print(f"   ✅ SHORTLISTED (Score >= {min_score})")
                shortlisted.append(candidate)
            else:
                print(f"   ❌ REJECTED (Score < {min_score})")
                rejected.append(candidate)
        
        print(f"\n✅ Shortlisted: {len(shortlisted)}/{len(candidates)} candidates")
        print(f"❌ Rejected: {len(rejected)}/{len(candidates)} candidates")
        
        return {
            **state,
            "scored_candidates": candidates,
            "shortlisted_candidates": shortlisted,
            "rejected_candidates": rejected,
            "status": "scoring_complete"
        }
        
    except Exception as e:
        print(f"❌ Scoring failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Scoring: {str(e)}")
        return {**state, "errors": errors, "status": "scoring_failed"}


def schedule_interviews_node(state: RecruitmentState) -> RecruitmentState:
    """Node 5: Schedule interviews ONLY for shortlisted candidates"""
    print("\n" + "="*60)
    print("📅 STEP 5: Interview Scheduling (Shortlisted Only)")
    print("="*60)
    
    try:
        shortlisted = state.get("shortlisted_candidates", [])
        
        if not shortlisted:
            print("⚠️  No shortlisted candidates to schedule")
            return {**state, "scheduled_candidates": [], "status": "no_shortlisted"}
        
        print(f"📅 Scheduling interviews for {len(shortlisted)} shortlisted candidate(s)")
        
        scheduler = InterviewScheduler()
        scheduled = scheduler.schedule_interviews(shortlisted, duration_minutes=45)
        
        print(f"✅ Scheduled {len(scheduled)} interview(s)")
        
        return {
            **state,
            "scheduled_candidates": scheduled,
            "status": "scheduling_complete"
        }
        
    except Exception as e:
        print(f"❌ Scheduling failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Scheduling: {str(e)}")
        return {**state, "errors": errors, "status": "scheduling_failed"}


# ============================================================================
# CONDITIONAL ROUTING FUNCTIONS (Decision Logic)
# ============================================================================

def should_schedule_interviews(state: RecruitmentState) -> Literal["schedule_interviews", "skip_scheduling"]:
    """
    Decision node: Check if there are shortlisted candidates
    Returns:
        - "schedule_interviews" if shortlisted candidates exist
        - "skip_scheduling" if no candidates passed threshold
    """
    shortlisted = state.get("shortlisted_candidates", [])
    
    if shortlisted and len(shortlisted) > 0:
        print(f"\n🔀 ROUTING DECISION: {len(shortlisted)} shortlisted → Proceeding to interview scheduling")
        return "schedule_interviews"
    else:
        print(f"\n🔀 ROUTING DECISION: No shortlisted candidates → Skipping scheduling")
        return "skip_scheduling"


def create_all_candidates_sheet_node(state: RecruitmentState) -> RecruitmentState:
    """Node 6a: Create Google Sheet for ALL candidates"""
    print("\n" + "="*60)
    print("� STEP 6A: Create All Candidates Database Sheet")
    print("="*60)
    
    try:
        enriched = state.get("enriched_candidates", [])
        
        if enriched:
            print(f"📊 Creating database sheet with ALL {len(enriched)} candidates...")
            sheets_manager = GoogleSheetsManager()
            sheet_title = f"AI_Recruiter_Database"
            sheets_url = sheets_manager.create_recruiter_sheet(enriched, sheet_title)
            print(f"✅ All candidates sheet: {sheets_url}")
        else:
            sheets_url = None
            print("⚠️ No candidates to export")
        
        return {
            **state,
            "sheets_url": sheets_url,
            "status": "all_candidates_sheet_created"
        }
        
    except Exception as e:
        print(f"❌ All candidates sheet creation failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"All Candidates Sheet: {str(e)}")
        return {**state, "errors": errors, "status": "all_sheet_failed"}


def create_interview_schedule_sheet_node(state: RecruitmentState) -> RecruitmentState:
    """Node 6b: Create Google Sheet for SHORTLISTED candidates with interview schedule"""
    print("\n" + "="*60)
    print("📅 STEP 6B: Create Interview Schedule Sheet (Shortlisted Only)")
    print("="*60)
    
    try:
        scheduled = state.get("scheduled_candidates", [])
        
        if scheduled:
            print(f"📅 Creating interview schedule sheet for {len(scheduled)} shortlisted candidates...")
            agent = RecruitmentAgent()
            interview_sheet_url = agent.create_scheduled_interviews_sheet(scheduled)
            print(f"✅ Interview schedule sheet: {interview_sheet_url}")
            
            # Save CSV
            csv_file = agent.save_to_csv(scheduled)
            print(f"✅ CSV exported: {csv_file}")
            
            # Extract calendar links
            calendar_links = []
            for candidate in scheduled:
                event_data = candidate.get('calendar_event_data', {})
                if event_data and event_data.get('data'):
                    response_data = event_data['data'].get('response_data', {})
                    event_link = response_data.get('htmlLink', '')
                    if event_link:
                        calendar_links.append(event_link)
        else:
            print("⚠️ No interviews scheduled - skipping interview sheet")
            interview_sheet_url = None
            csv_file = None
            calendar_links = []
        
        shortlisted = state.get("shortlisted_candidates", [])
        rejected = state.get("rejected_candidates", [])
        enriched = state.get("enriched_candidates", [])
        
        print(f"\n📊 Summary:")
        print(f"   • Total candidates: {len(enriched)}")
        print(f"   • Shortlisted: {len(shortlisted)}")
        print(f"   • Rejected: {len(rejected)}")
        print(f"   • Interviews scheduled: {len(scheduled)}")
        
        return {
            **state,
            "interview_sheet_url": interview_sheet_url,
            "csv_file": csv_file,
            "calendar_links": calendar_links,
            "status": "export_complete"
        }
        
    except Exception as e:
        print(f"❌ Interview schedule sheet creation failed: {str(e)}")
        errors = state.get("errors", [])
        errors.append(f"Interview Sheet: {str(e)}")
        return {**state, "errors": errors, "status": "interview_sheet_failed"}


def final_report_node(state: RecruitmentState) -> RecruitmentState:
    """Node 7: Generate final report with conditional results"""
    print("\n" + "="*60)
    print("PIPELINE COMPLETE - FINAL REPORT")
    print("="*60)
    
    print(f"\nSummary:")
    print(f"  • Emails checked: {len(state.get('email_messages', []))}")
    print(f"  • Resumes downloaded: {len(state.get('downloaded_files', []))}")
    print(f"  • Candidates extracted: {len(state.get('extracted_candidates', []))}")
    print(f"  • Candidates enriched: {len(state.get('enriched_candidates', []))}")
    print(f"  • Candidates scored: {len(state.get('scored_candidates', []))}")
    print(f"  • ✅ Shortlisted: {len(state.get('shortlisted_candidates', []))}")
    print(f"  • ❌ Rejected: {len(state.get('rejected_candidates', []))}")
    print(f"  • 📅 Interviews scheduled: {len(state.get('scheduled_candidates', []))}")
    
    # Show all output files and links
    print(f"\n" + "="*60)
    print("OUTPUT FILES & LINKS")
    print("="*60)
    
    # 1. JSON File
    if state.get("json_file"):
        print(f"\n1. CANDIDATE DATABASE (JSON):")
        print(f"   File: {state['json_file']}")
        print(f"   Contains: {len(state.get('enriched_candidates', []))} candidates")
    
    # 2. Main Candidate Sheet
    if state.get("sheets_url"):
        enriched = state.get('enriched_candidates', [])
        shortlisted = state.get('shortlisted_candidates', [])
        rejected = state.get('rejected_candidates', [])
        
        print(f"\n2. ALL CANDIDATES APPLIED (Google Sheets):")
        print(f"   Link: {state['sheets_url']}")
        print(f"   Total: {len(enriched)} candidates")
        print(f"   ✅ Shortlisted: {len(shortlisted)}")
        print(f"   ❌ Rejected: {len(rejected)}")
    
    # 3. Interview Schedule Sheet (only if interviews were scheduled)
    if state.get("interview_sheet_url"):
        print(f"\n3. SELECTED CANDIDATES & INTERVIEW SCHEDULE (Google Sheets):")
        print(f"   Link: {state['interview_sheet_url']}")
        print(f"   Contains: {len(state.get('scheduled_candidates', []))} shortlisted candidates")
        print(f"   Interview Dates: Oct 22, 2025")
        
        # 4. CSV Export
        if state.get("csv_file"):
            print(f"\n4. INTERVIEW SCHEDULE (CSV Export):")
            print(f"   File: {state['csv_file']}")
    else:
        print(f"\n3. ⚠️  NO INTERVIEWS SCHEDULED")
        print(f"   Reason: No candidates met the minimum score threshold")
    
    # 5. Calendar Links
    calendar_links = state.get('calendar_links', [])
    if calendar_links:
        print(f"\n5. GOOGLE CALENDAR EVENTS:")
        print(f"   Total Events Created: {len(calendar_links)}")
        print(f"   Main Calendar: https://calendar.google.com")
        
        print(f"\n   Individual Interview Event Links:")
        scheduled = state.get('scheduled_candidates', [])
        for i, (candidate, link) in enumerate(zip(scheduled, calendar_links), 1):
            name = candidate.get('name', candidate.get('full_name', 'Unknown'))
            date = candidate.get('interview_date', 'N/A')
            time = candidate.get('interview_time', 'N/A')
            print(f"   {i}. {name} - {date} at {time}")
            print(f"      {link}")
    
    if state.get("errors"):
        print(f"\nErrors encountered:")
        for error in state["errors"]:
            print(f"  • {error}")
    
    print("\n" + "="*60)
    print("PIPELINE EXECUTION COMPLETE")
    print("="*60)
    
    return {**state, "status": "complete"}


# ============================================================================
# BUILD ADVANCED LANGGRAPH WORKFLOW WITH CONDITIONAL ROUTING
# ============================================================================

def create_recruitment_pipeline() -> StateGraph:
    """Create the advanced LangGraph recruitment pipeline with detailed sub-steps"""
    
    # Initialize the graph
    workflow = StateGraph(RecruitmentState)
    
    # ========== ADD ALL DETAILED NODES ==========
    
    # Step 1: Gmail Monitoring
    workflow.add_node("gmail_monitor", gmail_monitor_node)
    
    # Step 2: Resume Extraction
    workflow.add_node("extract_resumes", extract_resumes_node)
    
    # Step 3: LinkedIn Enrichment (with fallback to LLM)
    workflow.add_node("linkedin_enrich", try_linkedin_enrichment_node)
    
    # Step 4: AI Scoring & Selection
    workflow.add_node("score_candidates", score_candidates_node)
    
    # Step 5: Interview Scheduling (conditional)
    workflow.add_node("schedule_interviews", schedule_interviews_node)
    
    # Step 6a: Create All Candidates Sheet
    workflow.add_node("create_all_candidates_sheet", create_all_candidates_sheet_node)
    
    # Step 6b: Create Interview Schedule Sheet (conditional)
    workflow.add_node("create_interview_sheet", create_interview_schedule_sheet_node)
    
    # Step 7: Final Report
    workflow.add_node("final_report", final_report_node)
    
    # ========== DEFINE WORKFLOW EDGES ==========
    
    # Sequential flow: Gmail → Extract → LinkedIn Enrich → Score
    workflow.set_entry_point("gmail_monitor")
    workflow.add_edge("gmail_monitor", "extract_resumes")
    workflow.add_edge("extract_resumes", "linkedin_enrich")
    workflow.add_edge("linkedin_enrich", "score_candidates")
    
    # CONDITIONAL: After scoring, decide whether to schedule interviews
    workflow.add_conditional_edges(
        "score_candidates",
        should_schedule_interviews,
        {
            "schedule_interviews": "schedule_interviews",  # If shortlisted → schedule
            "skip_scheduling": "create_all_candidates_sheet"  # If none → skip to sheets
        }
    )
    
    # After scheduling → Create all candidates sheet
    workflow.add_edge("schedule_interviews", "create_all_candidates_sheet")
    
    # After all candidates sheet → Create interview schedule sheet
    workflow.add_edge("create_all_candidates_sheet", "create_interview_sheet")
    
    # After interview sheet → Final report
    workflow.add_edge("create_interview_sheet", "final_report")
    
    # End
    workflow.add_edge("final_report", END)
    
    return workflow.compile()


def visualize_pipeline(pipeline, save_path: str = "output/recruitment_pipeline_graph.png"):
    """
    Visualize the LangGraph pipeline and save as image
    
    Args:
        pipeline: Compiled LangGraph workflow
        save_path: Path to save the visualization image
    """
    try:
        print("\n" + "="*60)
        print("[GRAPH] GENERATING PIPELINE VISUALIZATION")
        print("="*60)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Generate the graph image
        graph_image = pipeline.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(save_path, 'wb') as f:
            f.write(graph_image)
        print(f"[OK] Pipeline graph saved to: {save_path}")
        
        # Display inline if in Jupyter/IPython
        if IPYTHON_AVAILABLE:
            try:
                display(Image(graph_image))
                print("[OK] Pipeline graph displayed inline")
            except:
                print("[WARN] Could not display inline (not in Jupyter environment)")
        
        return graph_image
        
    except Exception as e:
        print(f"[WARN] Could not generate visualization: {str(e)}")
        print("   Install pygraphviz for better visualization:")
        print("   pip install pygraphviz")
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_complete_pipeline(
    check_gmail: bool = True,
    max_emails: int = 10,
    min_score_threshold: float = 5.0
) -> Dict:
    """
    Run the complete AI Recruiter pipeline using LangGraph
    
    Args:
        check_gmail: Whether to check Gmail for new resumes
        max_emails: Maximum number of emails to check
        min_score_threshold: Minimum score for candidate shortlisting
    
    Returns:
        Final state dictionary with all results
    """
    print("\n" + "="*60)
    print("AI RECRUITER COPILOT - ADVANCED LANGGRAPH PIPELINE")
    print("="*60)
    print("Complete automation with intelligent decision-making:")
    print("Gmail -> Extract -> Enrich -> Score -> [Conditional] -> Schedule -> Sheets")
    print("="*60)
    
    # Create pipeline
    pipeline = create_recruitment_pipeline()
    
    # Visualize the pipeline graph
    visualize_pipeline(pipeline, save_path="output/recruitment_pipeline_graph.png")
    
    # Initial state
    initial_state = {
        "check_gmail": check_gmail,
        "max_emails": max_emails,
        "min_score_threshold": min_score_threshold,
        "email_messages": [],
        "downloaded_files": [],
        "extracted_candidates": [],
        "enriched_candidates": [],
        "scored_candidates": [],
        "shortlisted_candidates": [],
        "rejected_candidates": [],
        "scheduled_candidates": [],
        "current_candidate": {},
        "linkedin_success": False,
        "sheets_url": "",
        "interview_sheet_url": "",
        "csv_file": "",
        "json_file": "",
        "calendar_links": [],
        "status": "started",
        "errors": []
    }
    
    # Run the pipeline
    try:
        final_state = pipeline.invoke(initial_state)
        return final_state
    except Exception as e:
        print(f"\n❌ Pipeline execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return initial_state


def main():
    """Main execution function"""
    result = run_complete_pipeline(
        check_gmail=True,      # Check Gmail for new resumes
        max_emails=10,         # Check last 10 emails
        min_score_threshold=5.0  # Shortlist candidates with score >= 5.0
    )
    
    print(f"\n✅ Pipeline execution finished with status: {result.get('status')}")
    
    return result


if __name__ == "__main__":
    main()
