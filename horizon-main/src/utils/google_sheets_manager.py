#!/usr/bin/env python3
"""
📊 GOOGLE SHEETS MANAGER MODULE
Handles Google Sheets creation and data population via Composio
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from composio import ComposioToolSet, Action
from ..config.legacy_config import (
    COMPOSIO_API_KEY, 
    GOOGLE_SHEETS_ACCOUNT_ID, 
    GOOGLE_SHEETS_USER_ID,
    GOOGLE_SHEETS_AUTH_CONFIG_ID
)


class GoogleSheetsManager:
    """Google Sheets Creation and Management Service"""
    
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.working_account_id = GOOGLE_SHEETS_ACCOUNT_ID
        self.entity_id = GOOGLE_SHEETS_USER_ID
        print("📊 Google Sheets Manager initialized")
    
    def create_empty_sheet(self, sheet_title: str) -> Optional[Dict]:
        """Create a new empty Google Sheet"""
        try:
            print(f"📊 Creating Google Sheet: {sheet_title}")
            
            create_result = self.composio_toolset.execute_action(
                action=Action.GOOGLESHEETS_CREATE_GOOGLE_SHEET1,
                params={"title": sheet_title},
                entity_id=self.entity_id
            )
            
            if create_result.get('successful'):
                sheet_data = create_result['data']
                spreadsheet_id = sheet_data['spreadsheetId']
                spreadsheet_url = sheet_data['spreadsheetUrl']
                
                print(f"✅ Sheet created successfully!")
                print(f"🔗 Sheet URL: {spreadsheet_url}")
                
                return {
                    'spreadsheet_id': spreadsheet_id,
                    'spreadsheet_url': spreadsheet_url,
                    'success': True
                }
            else:
                print(f"❌ Failed to create Google Sheet")
                print(f"Error: {create_result}")
                return None
                
        except Exception as e:
            print(f"❌ Sheet creation error: {str(e)}")
            return None
    
    def populate_sheet_with_data(self, spreadsheet_id: str, data: List[List], sheet_name: str = "Sheet1") -> bool:
        """Populate Google Sheet with candidate data"""
        try:
            print(f"📝 Adding {len(data)} rows to Google Sheet...")
            
            update_result = self.composio_toolset.execute_action(
                action=Action.GOOGLESHEETS_BATCH_UPDATE,
                params={
                    "spreadsheet_id": spreadsheet_id,
                    "sheet_name": sheet_name,
                    "values": data,
                    "valueInputOption": "RAW"
                },
                entity_id=self.entity_id
            )
            
            if update_result.get('successful'):
                print(f"✅ Sheet populated successfully!")
                return True
            else:
                print(f"❌ Failed to populate sheet")
                print(f"Error: {update_result}")
                return False
                
        except Exception as e:
            print(f"❌ Sheet population error: {str(e)}")
            return False
    
    def prepare_candidate_data_for_sheets(self, candidates: List[Dict]) -> List[List]:
        """Convert candidate data to Google Sheets format"""
        print(f"🔄 Preparing {len(candidates)} candidates for Google Sheets...")
        
        # Define comprehensive headers for recruiters
        headers = [
            "Name", "Email", "Phone", "Role", "Company", 
            "Experience", "Skills", "Location", "Education", 
            "LinkedIn", "LinkedIn Status", "GitHub", "Portfolio",
            "Professional Summary", "Key Achievements", "Certifications",
            "Projects", "Languages", "Awards", "Data Source"
        ]
        
        sheet_data = [headers]
        
        for candidate in candidates:
            # Extract basic info
            name = str(candidate.get('full_name', '')).strip()
            email = str(candidate.get('email', '')).strip()
            phone = str(candidate.get('phone', '')).strip()
            role = str(candidate.get('current_role', '')).strip()
            company = str(candidate.get('company', '')).strip()
            
            # Experience years
            years = str(candidate.get('years_of_experience', '')).strip()
            if not years:
                exp_count = len(candidate.get('experience', []))
                years = f"{exp_count} roles" if exp_count > 0 else ""
            
            # Skills (top 4 for readability)
            skills = candidate.get('skills', [])
            if isinstance(skills, list) and skills:
                skill_text = ', '.join(str(s) for s in skills[:4])
                if len(skills) > 4:
                    skill_text += f" (+{len(skills)-4})"
            else:
                skill_text = str(candidate.get('key_competencies', ''))[:60]
            
            # Location
            location = str(candidate.get('location', '')).strip()
            
            # Education (first degree with key info)
            education = ""
            edu_list = candidate.get('education', [])
            if edu_list and isinstance(edu_list, list) and len(edu_list) > 0:
                first_edu = edu_list[0]
                if isinstance(first_edu, dict):
                    degree = first_edu.get('degree', '')
                    school = first_edu.get('institution', '')
                    year = first_edu.get('year', '')
                    
                    parts = []
                    if degree: parts.append(degree)
                    if school: parts.append(f"from {school}")
                    if year: parts.append(f"({year})")
                    education = " ".join(parts)
                elif isinstance(first_edu, str):
                    education = first_edu
            
            # URLs and verification
            linkedin = str(candidate.get('linkedin_url', '')).strip()
            
            # LinkedIn status
            if candidate.get('linkedin_verified'):
                linkedin_status = "Verified"
            elif candidate.get('linkedin_has_profile') or linkedin:
                linkedin_status = "Profile Found"
            else:
                linkedin_status = "No Profile"
            
            github = str(candidate.get('github_url', '')).strip()
            portfolio = str(candidate.get('portfolio_url', '')).strip()
            
            # Professional summary (full, no truncation)
            summary_parts = []
            linkedin_summary = candidate.get('linkedin_summary', '')
            original_summary = candidate.get('summary', '')
            professional_value = candidate.get('professional_value', '')
            
            if linkedin_summary:
                summary_parts.append(linkedin_summary)
            if original_summary and original_summary not in linkedin_summary:
                summary_parts.append(original_summary)
            
            full_summary = ' | '.join(filter(None, summary_parts))
            if not full_summary and professional_value:
                full_summary = professional_value
            if not full_summary:
                full_summary = f"{role} professional" if role else "Professional"
            
            # Key achievements
            achievements = []
            experience = candidate.get('experience', [])
            if isinstance(experience, list):
                for exp in experience[:2]:
                    if isinstance(exp, dict) and exp.get('achievements'):
                        exp_achievements = exp['achievements']
                        if isinstance(exp_achievements, list):
                            achievements.extend([str(a) for a in exp_achievements[:2]])
            achievement_text = '; '.join(achievements[:3]) if achievements else ""
            
            # Certifications (top 3)
            certifications = candidate.get('certifications', [])
            if isinstance(certifications, list) and certifications:
                cert_text = ', '.join(str(cert) for cert in certifications[:3])
                if len(certifications) > 3:
                    cert_text += f" (+{len(certifications)-3})"
            else:
                cert_text = str(certifications) if certifications else ""
            
            # Projects (top 2)
            projects = candidate.get('projects', [])
            if isinstance(projects, list) and projects:
                project_names = []
                for p in projects[:2]:
                    if isinstance(p, dict) and p.get('name'):
                        project_names.append(str(p['name']))
                    elif isinstance(p, str):
                        project_names.append(p)
                project_text = ', '.join(project_names)
                if len(projects) > 2:
                    project_text += f" (+{len(projects)-2})"
            else:
                project_text = ""
            
            # Languages
            languages = candidate.get('languages', [])
            if isinstance(languages, list) and languages:
                lang_text = ', '.join(str(lang) for lang in languages[:3])
            else:
                lang_text = str(languages) if languages else ""
            
            # Awards
            awards = candidate.get('awards', [])
            if isinstance(awards, list) and awards:
                award_text = ', '.join(str(award) for award in awards[:2])
            else:
                award_text = str(awards) if awards else ""
            
            # Data source
            source = candidate.get('source', 'Unknown')
            
            # Create row
            row = [
                name, email, phone, role, company, years, skill_text, location, education,
                linkedin, linkedin_status, github, portfolio, full_summary, achievement_text,
                cert_text, project_text, lang_text, award_text, source
            ]
            
            sheet_data.append(row)
        
        print(f"✅ Data prepared: {len(sheet_data)} rows (including header)")
        return sheet_data
    
    def create_recruiter_sheet(self, candidates: List[Dict], sheet_name_prefix: str = "AI_Recruiter") -> Optional[str]:
        """Create complete Google Sheet with candidate data for recruiters"""
        print(f"\n📊 GOOGLE SHEETS MANAGER: Creating sheet for {len(candidates)} candidates")
        print("=" * 60)
        
        if not candidates:
            print("❌ No candidates provided")
            return None
        
        # Generate sheet name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        sheet_title = f"{sheet_name_prefix}_{timestamp}"
        
        # Step 1: Create empty sheet
        sheet_info = self.create_empty_sheet(sheet_title)
        
        if not sheet_info:
            return None
        
        spreadsheet_id = sheet_info['spreadsheet_id']
        spreadsheet_url = sheet_info['spreadsheet_url']
        
        # Step 2: Prepare data
        sheet_data = self.prepare_candidate_data_for_sheets(candidates)
        
        # Step 3: Populate sheet
        success = self.populate_sheet_with_data(spreadsheet_id, sheet_data)
        
        if success:
            print(f"\n🎉 Google Sheet created successfully!")
            print(f"📊 Sheet contains {len(candidates)} candidates with comprehensive data")
            print(f"🔗 Share this link: {spreadsheet_url}")
            return spreadsheet_url
        else:
            print(f"\n⚠️ Sheet created but data population failed")
            print(f"🔗 Empty sheet: {spreadsheet_url}")
            return spreadsheet_url
    
    def get_sheet_summary(self, candidates: List[Dict]) -> Dict:
        """Generate summary of what will be in the Google Sheet"""
        if not candidates:
            return {"total": 0}
        
        summary = {
            "total_candidates": len(candidates),
            "with_linkedin": len([c for c in candidates if c.get('linkedin_url')]),
            "verified_linkedin": len([c for c in candidates if c.get('linkedin_verified')]),
            "with_email": len([c for c in candidates if c.get('email')]),
            "with_phone": len([c for c in candidates if c.get('phone')]),
            "with_skills": len([c for c in candidates if c.get('skills')]),
            "total_skills": sum(len(c.get('skills', [])) for c in candidates),
            "with_experience": len([c for c in candidates if c.get('experience')]),
            "with_education": len([c for c in candidates if c.get('education')]),
            "data_sources": list(set(c.get('source', 'Unknown') for c in candidates))
        }
        
        return summary


def main():
    """Test the Google Sheets Manager independently"""
    print("📊 TESTING GOOGLE SHEETS MANAGER MODULE")
    print("=" * 45)
    
    # Test with sample candidates
    test_candidates = [
        {
            "full_name": "Test User 1",
            "email": "test1@example.com",
            "phone": "+1-555-0001",
            "current_role": "Software Engineer",
            "company": "Tech Corp",
            "skills": ["Python", "JavaScript", "React"],
            "linkedin_url": "https://www.linkedin.com/in/test1",
            "source": "pdf_resume"
        },
        {
            "full_name": "Test User 2", 
            "email": "test2@example.com",
            "current_role": "Data Scientist",
            "company": "Data Inc",
            "skills": ["Python", "SQL", "Machine Learning"],
            "linkedin_verified": True,
            "source": "existing_data"
        }
    ]
    
    sheets_manager = GoogleSheetsManager()
    
    # Show summary
    summary = sheets_manager.get_sheet_summary(test_candidates)
    print(f"\n📋 SHEET SUMMARY:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Create sheet
    sheet_url = sheets_manager.create_recruiter_sheet(test_candidates, "Test_Recruiter")
    
    if sheet_url:
        print(f"\n🎉 Test completed successfully!")
        print(f"🔗 Test sheet: {sheet_url}")


if __name__ == "__main__":
    main()