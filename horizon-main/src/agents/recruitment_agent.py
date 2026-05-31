"""
🎯 RECRUITMENT AGENT - Complete Candidate Selection & Scheduling Pipeline
Combines: Scoring → Selection → Calendar Scheduling → Google Sheets Export

This module orchestrates:
1. Score candidates using AI (candidate_scorer.py)
2. Schedule interviews in Google Calendar (interview_scheduler.py)  
3. Create Google Sheet with scheduled interviews
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import our modular components
from ..utils.candidate_scorer import CandidateScorer, DEFAULT_CRITERIA
from ..utils.interview_scheduler import InterviewScheduler
from composio import ComposioToolSet, Action
from ..config.legacy_config import (
    COMPOSIO_API_KEY, 
    GROQ_API_KEY, 
    GOOGLE_SHEETS_USER_ID,
    GOOGLE_CALENDAR_USER_ID
)


class RecruitmentAgent:
    """
    Complete recruitment agent for candidate scoring, scheduling, and tracking
    Uses ComposioToolSet for Google Calendar and Google Sheets integration
    """
    
    def __init__(self, composio_api_key: str = None, groq_api_key: str = None, entity_id: str = None):
        """
        Initialize the recruitment agent
        
        Args:
            composio_api_key: Composio API key (defaults to config)
            groq_api_key: Groq API key (defaults to config)
            entity_id: Entity ID for Composio actions (defaults to GOOGLE_SHEETS_USER_ID)
        """
        # Load environment variables
        load_dotenv()
        
        self.composio_api_key = composio_api_key or COMPOSIO_API_KEY
        self.groq_api_key = groq_api_key or GROQ_API_KEY
        self.entity_id = entity_id or GOOGLE_SHEETS_USER_ID
        
        # Initialize ComposioToolSet
        self.toolset = ComposioToolSet(api_key=self.composio_api_key)
        
        # Initialize modules
        self.scorer = CandidateScorer(groq_api_key=self.groq_api_key)
        # Use calendar-specific entity_id for scheduler
        self.scheduler = InterviewScheduler(
            composio_api_key=self.composio_api_key, 
            entity_id=GOOGLE_CALENDAR_USER_ID
        )
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("🎯 RECRUITMENT AGENT INITIALIZED")
        print("=" * 60)
        print("📊 Candidate Scorer: Ready")
        print("📅 Interview Scheduler: Ready")
        print("📑 Google Sheets Manager: Ready")
        print("=" * 60)
    
    def load_candidates(self, json_file: str = None) -> List[Dict]:
        """
        Load candidates from JSON file
        
        Args:
            json_file: Path to JSON file with candidates (defaults to latest enriched file)
            
        Returns:
            List of candidate dictionaries
        """
        if not json_file:
            # Find latest enriched candidates file
            import glob
            pattern = "enhanced_candidates_*.json"
            files = glob.glob(pattern)
            if files:
                json_file = max(files)  # Get latest file
                print(f"📂 Loading candidates from: {json_file}")
            else:
                print("❌ No candidate files found!")
                return []
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                candidates = data
            elif isinstance(data, dict) and 'candidates' in data:
                candidates = data['candidates']
            else:
                candidates = [data]
            
            print(f"✅ Loaded {len(candidates)} candidates")
            return candidates
            
        except Exception as e:
            print(f"❌ Error loading candidates: {str(e)}")
            return []
    
    def score_and_select(
        self, 
        candidates: List[Dict], 
        criteria: Dict = None, 
        min_score: float = 6.0
    ) -> List[Dict]:
        """
        Score candidates and select top performers
        
        Args:
            candidates: List of candidate dictionaries
            criteria: Scoring criteria (defaults to DEFAULT_CRITERIA)
            min_score: Minimum score threshold
            
        Returns:
            List of shortlisted candidates with scores
        """
        print(f"\n📊 STEP 1: CANDIDATE SCORING & SELECTION")
        print("-" * 60)
        print(f"🎯 Minimum Score Threshold: {min_score}/10")
        print(f"📋 Total Candidates to Evaluate: {len(candidates)}")
        print()
        
        if not criteria:
            criteria = DEFAULT_CRITERIA
            print(f"📌 Using Default Criteria:")
            print(f"   Role: {criteria['role']}")
            print(f"   Required Skills: {', '.join(criteria['required_skills'][:3])}...")
            print(f"   Min Experience: {criteria['min_experience_years']} years")
            print()
        
        # Score all candidates
        shortlisted = self.scorer.score_candidates(candidates, criteria, min_score)
        
        print(f"\n✅ Scoring Complete!")
        print(f"🎯 Shortlisted: {len(shortlisted)}/{len(candidates)} candidates")
        
        return shortlisted
    
    def schedule_interviews(
        self, 
        shortlisted: List[Dict],
        duration_minutes: int = 45
    ) -> List[Dict]:
        """
        Schedule interviews for shortlisted candidates
        
        Args:
            shortlisted: List of shortlisted candidate dictionaries
            duration_minutes: Interview duration
            
        Returns:
            List of candidates with schedule information
        """
        print(f"\n📅 STEP 2: INTERVIEW SCHEDULING")
        print("-" * 60)
        
        if not shortlisted:
            print("ℹ️  No candidates to schedule")
            return []
        
        # Schedule interviews
        scheduled = self.scheduler.schedule_interviews(
            shortlisted_candidates=shortlisted,
            duration_minutes=duration_minutes
        )
        
        return scheduled
    
    def create_scheduled_interviews_sheet(self, scheduled_candidates: List[Dict]) -> Optional[str]:
        """
        Create Google Sheet with scheduled interview details
        
        Args:
            scheduled_candidates: List of candidates with schedule info
            
        Returns:
            Google Sheets URL or None
        """
        print(f"\n📑 STEP 3: CREATING GOOGLE SHEET")
        print("-" * 60)
        
        if not scheduled_candidates:
            print("ℹ️  No scheduled candidates to export")
            return None
        
        try:
            # Prepare sheet data
            sheet_name = f"Scheduled_Interviews_{self.timestamp}"
            
            # Headers
            headers = [
                "Candidate Name", "Email", "Score", "Interview Date", 
                "Interview Time", "Duration (min)", "Calendar Event Created",
                "Rationale", "Skills", "Experience", "Current Role"
            ]
            
            # Prepare rows
            rows = [headers]
            for candidate in scheduled_candidates:
                # Extract data
                name = candidate.get("name", candidate.get("full_name", "Unknown"))
                email = candidate.get("email", "")
                score = candidate.get("score", "N/A")
                interview_date = candidate.get("interview_date", "Not scheduled")
                interview_time = candidate.get("interview_time", "Not scheduled")
                duration = candidate.get("duration_minutes", 45)
                calendar_created = "✅ Yes" if candidate.get("calendar_event_created") else "❌ No"
                rationale = candidate.get("rationale", "")
                
                # Get original data
                original = candidate.get("original_data", candidate)
                skills = ", ".join(original.get("skills", [])[:5])
                experience_count = len(original.get("experience", []))
                current_role = original.get("current_role", "")
                
                row = [
                    name, email, score, interview_date, interview_time,
                    duration, calendar_created, rationale, skills, 
                    f"{experience_count} roles", current_role
                ]
                rows.append(row)
            
            # Create sheet using ComposioToolSet
            print(f"📝 Creating sheet: {sheet_name}")
            
            # Step 1: Create empty sheet
            create_result = self.toolset.execute_action(
                action="GOOGLESHEETS_CREATE_GOOGLE_SHEET1",
                params={"title": sheet_name},
                entity_id=self.entity_id
            )
            
            if not create_result.get("successful"):
                print(f"❌ Failed to create sheet: {create_result}")
                return None
            
            sheet_data = create_result.get("data", {})
            spreadsheet_id = sheet_data.get("spreadsheetId")
            spreadsheet_url = sheet_data.get("spreadsheetUrl")
            
            print(f"✅ Sheet created: {spreadsheet_url}")
            
            # Step 2: Populate with data
            print("📝 Populating sheet with interview data...")
            
            update_result = self.toolset.execute_action(
                action=Action.GOOGLESHEETS_BATCH_UPDATE,
                params={
                    "spreadsheet_id": spreadsheet_id,
                    "sheet_name": "Sheet1",
                    "values": rows,
                    "range": "A1"
                },
                entity_id=self.entity_id
            )
            
            if update_result.get("successful"):
                print(f"✅ Sheet populated with {len(rows)-1} candidates")
                print(f"🔗 Sheet URL: {spreadsheet_url}")
                return spreadsheet_url
            else:
                print(f"⚠️  Sheet created but population failed: {update_result}")
                return spreadsheet_url
                
        except Exception as e:
            print(f"❌ Error creating Google Sheet: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_to_csv(self, scheduled_candidates: List[Dict], filename: str = None) -> str:
        """
        Save scheduled interviews to CSV
        
        Args:
            scheduled_candidates: List of candidates with schedule info
            filename: Output filename (optional)
            
        Returns:
            Filename of created CSV
        """
        if not filename:
            filename = f"Scheduled_Interviews_{self.timestamp}.csv"
        
        # Ensure output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Full path with output directory
        filepath = os.path.join(output_dir, filename)
        
        print(f"\n💾 Saving to CSV: {filepath}")
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Headers
                headers = [
                    "Name", "Email", "Score", "Interview Date", "Interview Time",
                    "Duration (min)", "Calendar Event", "Rationale"
                ]
                writer.writerow(headers)
                
                # Data rows
                for candidate in scheduled_candidates:
                    name = candidate.get("name", candidate.get("full_name", "Unknown"))
                    email = candidate.get("email", "")
                    score = candidate.get("score", "N/A")
                    interview_date = candidate.get("interview_date", "Not scheduled")
                    interview_time = candidate.get("interview_time", "Not scheduled")
                    duration = candidate.get("duration_minutes", 45)
                    calendar_created = "Yes" if candidate.get("calendar_event_created") else "No"
                    rationale = candidate.get("rationale", "")
                    
                    writer.writerow([
                        name, email, score, interview_date, interview_time,
                        duration, calendar_created, rationale
                    ])
            
            print(f"✅ CSV saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving CSV: {str(e)}")
            return None
    
    def run_complete_pipeline(
        self,
        candidates_file: str = None,
        criteria: Dict = None,
        min_score: float = 6.0,
        duration_minutes: int = 45
    ) -> Dict:
        """
        Run the complete recruitment pipeline
        
        Args:
            candidates_file: Path to candidates JSON file
            criteria: Scoring criteria
            min_score: Minimum score threshold
            duration_minutes: Interview duration
            
        Returns:
            Results dictionary
        """
        print("\n" + "=" * 60)
        print("🎯 RECRUITMENT AGENT - COMPLETE PIPELINE")
        print("=" * 60)
        
        results = {
            "success": False,
            "total_candidates": 0,
            "shortlisted": 0,
            "scheduled": 0,
            "sheets_url": None,
            "csv_file": None
        }
        
        try:
            # Load candidates
            candidates = self.load_candidates(candidates_file)
            if not candidates:
                print("❌ No candidates to process")
                return results
            
            results["total_candidates"] = len(candidates)
            
            # Score and select
            shortlisted = self.score_and_select(candidates, criteria, min_score)
            results["shortlisted"] = len(shortlisted)
            
            if not shortlisted:
                print("\n⚠️  No candidates met the minimum score threshold")
                return results
            
            # Schedule interviews
            scheduled = self.schedule_interviews(shortlisted, duration_minutes)
            results["scheduled"] = len(scheduled)
            
            # Create Google Sheet
            sheets_url = self.create_scheduled_interviews_sheet(scheduled)
            results["sheets_url"] = sheets_url
            
            # Save to CSV
            csv_file = self.save_to_csv(scheduled)
            results["csv_file"] = csv_file
            
            # Final summary
            print("\n" + "=" * 60)
            print("🎉 RECRUITMENT PIPELINE COMPLETE!")
            print("=" * 60)
            print(f"📊 Total Candidates Evaluated: {results['total_candidates']}")
            print(f"✅ Shortlisted: {results['shortlisted']}")
            print(f"📅 Interviews Scheduled: {results['scheduled']}")
            if sheets_url:
                print(f"🔗 Google Sheet: {sheets_url}")
            if csv_file:
                print(f"💾 CSV Export: {csv_file}")
            print("=" * 60)
            
            results["success"] = True
            return results
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return results


def main():
    """Main execution function for testing"""
    print("🚀 RECRUITMENT AGENT - STANDALONE TEST")
    print("=" * 60)
    
    # Initialize agent
    agent = RecruitmentAgent()
    
    # Run complete pipeline
    results = agent.run_complete_pipeline(
        min_score=5.0,  # Adjust threshold as needed
        duration_minutes=45
    )
    
    if results["success"]:
        print("\n✅ Test complete! Check the Google Sheet and CSV output.")
    else:
        print("\n❌ Test failed. Please check the errors above.")
    
    return results


if __name__ == "__main__":
    main()
