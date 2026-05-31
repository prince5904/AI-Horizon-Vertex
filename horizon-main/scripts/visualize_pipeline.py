"""
Generate detailed visualization of the AI Recruiter LangGraph Pipeline
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_recruiter_pipeline import create_recruitment_pipeline

def print_detailed_graph():
    """Print ASCII and detailed text representation of the pipeline"""
    
    print("\n" + "="*80)
    print("AI RECRUITER COPILOT - LANGGRAPH WORKFLOW VISUALIZATION")
    print("="*80)
    
    # Create pipeline
    pipeline = create_recruitment_pipeline()
    graph = pipeline.get_graph()
    
    # Print ASCII visualization
    print("\nVISUAL GRAPH (ASCII):")
    print("-" * 80)
    print(graph.draw_ascii())
    
    # Print detailed node information
    print("\n" + "="*80)
    print("DETAILED NODE BREAKDOWN")
    print("="*80)
    
    nodes = [
        {
            "name": "gmail_monitor",
            "title": "1. Gmail Monitoring",
            "description": "Scans Gmail inbox for resume PDF attachments",
            "outputs": "List of downloaded resume files"
        },
        {
            "name": "extract_resumes",
            "title": "📄 Resume Extraction & Parsing",
            "description": "Extracts text from PDFs and parses with AI (Groq LLM)",
            "outputs": "Structured candidate data (name, email, skills, experience)"
        },
        {
            "name": "linkedin_enrich",
            "title": "🔗 LinkedIn API Enrichment",
            "description": "Attempts real LinkedIn API call, falls back to LLM if unavailable",
            "outputs": "Enriched profiles with LinkedIn data or AI-generated insights"
        },
        {
            "name": "score_candidates",
            "title": "📊 AI Scoring & Selection [DECISION POINT]",
            "description": "Scores candidates with Groq LLM, classifies as SHORTLISTED or REJECTED",
            "outputs": "Shortlisted candidates (score >= threshold), Rejected candidates"
        },
        {
            "name": "schedule_interviews",
            "title": "📅 Google Calendar Interview Scheduling [CONDITIONAL]",
            "description": "Creates Google Calendar events ONLY for shortlisted candidates",
            "outputs": "Scheduled interviews with calendar event links",
            "condition": "Only runs if shortlisted_candidates > 0"
        },
        {
            "name": "create_all_candidates_sheet",
            "title": "📊 Create All Candidates Database Sheet",
            "description": "Creates Google Sheet with ALL candidates (shortlisted + rejected)",
            "outputs": "Google Sheets URL with comprehensive candidate data"
        },
        {
            "name": "create_interview_sheet",
            "title": "📅 Create Interview Schedule Sheet [CONDITIONAL OUTPUT]",
            "description": "Creates Google Sheet ONLY for shortlisted candidates with interview times",
            "outputs": "Google Sheets URL, CSV file, Calendar event links"
        },
        {
            "name": "final_report",
            "title": "📋 Final Report Generation",
            "description": "Displays comprehensive summary with all links and statistics",
            "outputs": "Console report with JSON, Sheets, CSV, and Calendar links"
        }
    ]
    
    for i, node in enumerate(nodes, 1):
        print(f"\n{i}. {node['title']}")
        print(f"   Node ID: {node['name']}")
        print(f"   Description: {node['description']}")
        print(f"   Outputs: {node['outputs']}")
        if 'condition' in node:
            print(f"   ⚠️  Condition: {node['condition']}")
    
    # Print conditional routing logic
    print("\n" + "="*80)
    print("🔀 CONDITIONAL ROUTING LOGIC")
    print("="*80)
    
    print("\n1. AFTER SCORING (score_candidates node):")
    print("   ┌─────────────────────────────────────────┐")
    print("   │  Decision: should_schedule_interviews() │")
    print("   └─────────────────────────────────────────┘")
    print("              |                    |")
    print("   IF shortlisted > 0   IF shortlisted == 0")
    print("              |                    |")
    print("              v                    v")
    print("   schedule_interviews    create_all_candidates_sheet")
    print("              |                    |")
    print("              └────────┬───────────┘")
    print("                       v")
    print("         create_all_candidates_sheet")
    
    print("\n2. ALL PATHS CONVERGE:")
    print("   Both conditional paths merge at 'create_all_candidates_sheet'")
    print("   Then proceed sequentially:")
    print("   create_all_candidates_sheet → create_interview_sheet → final_report")
    
    # Print output files
    print("\n" + "="*80)
    print("📁 OUTPUT FILES GENERATED")
    print("="*80)
    
    outputs = [
        {
            "name": "enhanced_candidates_TIMESTAMP.json",
            "description": "All enriched candidate data (JSON format)",
            "always": True
        },
        {
            "name": "Google Sheet: All Candidates Database",
            "description": "Contains ALL candidates with scores, enrichment data",
            "always": True
        },
        {
            "name": "Google Sheet: Interview Schedule",
            "description": "Contains ONLY shortlisted candidates with interview dates/times",
            "always": False,
            "condition": "Only if shortlisted candidates exist"
        },
        {
            "name": "Scheduled_Interviews_TIMESTAMP.csv",
            "description": "CSV export of interview schedule",
            "always": False,
            "condition": "Only if shortlisted candidates exist"
        },
        {
            "name": "Google Calendar Event Links",
            "description": "Individual calendar event URLs for each interview",
            "always": False,
            "condition": "Only if shortlisted candidates exist"
        },
        {
            "name": "recruitment_pipeline_graph.png",
            "description": "Visual diagram of the LangGraph workflow (Mermaid format)",
            "always": True
        }
    ]
    
    print("\n✅ ALWAYS GENERATED:")
    for output in outputs:
        if output['always']:
            print(f"   • {output['name']}")
            print(f"     └─ {output['description']}")
    
    print("\n⚠️  CONDITIONALLY GENERATED:")
    for output in outputs:
        if not output['always']:
            print(f"   • {output['name']}")
            print(f"     └─ {output['description']}")
            print(f"     └─ Condition: {output.get('condition', 'N/A')}")
    
    # Print example execution
    print("\n" + "="*80)
    print("🎯 EXAMPLE EXECUTION FLOW")
    print("="*80)
    
    print("\nScenario: 4 candidates, 3 meet threshold (score >= 5.0), 1 rejected")
    print("\nStep-by-Step:")
    print("1. 📧 Gmail Monitor → Downloads 4 resume PDFs")
    print("2. 📄 Extract Resumes → Parses 4 candidates with AI")
    print("3. 🔗 LinkedIn Enrich → Attempts API for all, falls back to LLM")
    print("4. 📊 Score Candidates → Scores: 8.2, 9.2, 4.2, 9.2")
    print("   └─ Result: 3 SHORTLISTED, 1 REJECTED")
    print("5. 🔀 ROUTING DECISION → shortlisted > 0 → SCHEDULE")
    print("6. 📅 Schedule Interviews → Creates 3 Google Calendar events")
    print("7. 📊 Create All Candidates Sheet → Sheet with all 4 candidates")
    print("8. 📅 Create Interview Sheet → Sheet with 3 shortlisted + times")
    print("9. 📋 Final Report → Displays all links and statistics")
    
    print("\n" + "="*80)
    print("✅ VISUALIZATION COMPLETE")
    print("="*80)
    print("\nThe graph shows:")
    print("  ✅ All 8 nodes (gmail_monitor → ... → final_report)")
    print("  ✅ Sequential edges (solid lines)")
    print("  ✅ Conditional routing (dotted lines from score_candidates)")
    print("  ✅ Decision diamond at score_candidates node")
    print("  ✅ Two paths that converge at create_all_candidates_sheet")
    
    print("\nTo run the pipeline:")
    print("  python ai_recruiter_pipeline.py")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    print_detailed_graph()
