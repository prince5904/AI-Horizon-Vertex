#!/usr/bin/env python3
"""
🔗 LINKEDIN ENRICHER MODULE
Handles LinkedIn profile enrichment via Composio API
"""

import json
from typing import Dict, Optional
from composio import ComposioToolSet, Action
from ..config.legacy_config import (
    COMPOSIO_API_KEY, 
    GROQ_API_KEY, 
    GROQ_MODEL,
    LINKEDIN_CONNECTED_ACCOUNT_ID,
    LINKEDIN_ENTITY_ID
)
from groq import Groq


class LinkedInEnricher:
    """
    LinkedIn Profile Enrichment Service
    
    Strategy:
    1. Try LinkedIn API (if properly configured with Composio)
    2. Fallback to LLM enrichment (always works, generates professional insights)
    
    Note: LinkedIn API integration in Composio requires proper OAuth connection
    and may have limited actions. LLM enrichment provides reliable results.
    """
    
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        print("🔗 LinkedIn Enricher initialized")
        print("   Strategy: LinkedIn API attempt → LLM enrichment fallback")
    
    def fetch_real_linkedin_data(self, linkedin_url: str) -> Dict:
        """
        Fetch real LinkedIn data via Composio API
        
        Note: LinkedIn API in Composio typically requires:
        1. LINKEDIN_GET_PROFILE action to get any profile by URL
        2. LINKEDIN_GET_MY_INFO to get your own authenticated profile
        
        Since we want to enrich candidate profiles, we'd use GET_PROFILE
        """
        try:
            entity_id = LINKEDIN_ENTITY_ID
            
            print(f"🔍 Attempting LinkedIn API call for: {linkedin_url}")
            
            # Method 1: Try to get profile by URL (if action exists)
            try:
                # LinkedIn profile enrichment usually requires the profile URL
                result = self.composio_toolset.execute_action(
                    action=Action.LINKEDIN_GET_PROFILE,  # Action to get OTHER people's profiles
                    params={"profile_url": linkedin_url},
                    entity_id=entity_id
                )
                
                if result.get('successful'):
                    data = result.get('data', {})
                    data['is_connected_account'] = True
                    print(f"✅ LinkedIn profile data fetched via GET_PROFILE")
                    return data
            except AttributeError:
                # Action doesn't exist, try alternative
                print(f"⚠️ LINKEDIN_GET_PROFILE action not available")
            except Exception as e:
                print(f"⚠️ GET_PROFILE failed: {str(e)[:100]}")
            
            # Method 2: Try getting your own info (limited usefulness for candidate enrichment)
            try:
                result = self.composio_toolset.execute_action(
                    action=Action.LINKEDIN_GET_MY_INFO,  # Gets YOUR profile, not the candidate's
                    params={},
                    entity_id=entity_id
                )
                
                if result.get('successful'):
                    print(f"⚠️ Got authenticated user's profile (not candidate's)")
                    print(f"   This won't match the candidate unless they're the authenticated user")
                    return {}  # Don't use this data as it's not the candidate's
            except Exception as e:
                print(f"⚠️ GET_MY_INFO also failed: {str(e)[:100]}")
            
            print(f"❌ All LinkedIn API methods failed")
            print(f"💡 Tip: Ensure LinkedIn account is properly connected in Composio dashboard")
            print(f"   Entity ID: {entity_id[:20]}..." if len(entity_id) > 20 else f"   Entity ID: {entity_id}")
            return {}
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ LinkedIn fetch error: {error_msg}")
            
            # Provide helpful troubleshooting tips
            if "Invalid connected account ID format" in error_msg:
                print(f"💡 Fix: The connected account ID format is invalid")
                print(f"   Current ID: {LINKEDIN_CONNECTED_ACCOUNT_ID}")
                print(f"   Solution: Go to Composio dashboard and get a valid LinkedIn connection")
                print(f"   URL: https://app.composio.dev/your_app/connections")
            elif "not found" in error_msg.lower():
                print(f"💡 Fix: LinkedIn account not connected")
                print(f"   Solution: Connect your LinkedIn account in Composio dashboard")
            
            return {}
    
    def generate_linkedin_fields_with_ai(self, candidate: Dict) -> Dict:
        """Generate LinkedIn-style professional fields using AI"""
        try:
            name = candidate.get('full_name', '')
            role = candidate.get('current_role', '')
            company = candidate.get('company', '')
            skills = candidate.get('skills', [])
            experience = candidate.get('experience', [])
            
            prompt = f"""
            Generate professional LinkedIn profile fields for this candidate. Return ONLY JSON:
            
            {{
                "linkedin_title": "Professional headline with key skills and role",
                "linkedin_industry": "Industry category",
                "linkedin_summary": "Professional summary 2-3 sentences highlighting achievements and value",
                "experience_highlights": "3-4 bullet points of key career achievements",
                "key_competencies": "Top 8-10 skills relevant to role",
                "career_level": "Junior/Mid-level/Senior/Executive based on experience",
                "professional_value": "Value proposition - what they bring to organizations"
            }}
            
            Candidate: {name}
            Current Role: {role}
            Company: {company}
            Skills: {', '.join(skills[:5]) if skills else 'General professional skills'}
            Experience: {len(experience)} roles in background
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                temperature=0.3,
                max_tokens=1000
            )
            
            ai_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                return json.loads(ai_text)
            except json.JSONDecodeError:
                # Extract from code block if needed
                if "```json" in ai_text:
                    json_start = ai_text.find("```json") + 7
                    json_end = ai_text.find("```", json_start)
                    return json.loads(ai_text[json_start:json_end].strip())
                else:
                    print("⚠️ AI response parsing failed")
                    return {}
                    
        except Exception as e:
            print(f"❌ AI field generation error: {str(e)}")
            return {}
    
    def enrich_candidate_profile(self, candidate: Dict) -> Dict:
        """Complete LinkedIn enrichment for a single candidate"""
        name = candidate.get('full_name', 'Unknown')
        print(f"\n🔗 Enriching LinkedIn profile for: {name}")
        
        enriched_candidate = candidate.copy()
        
        # Check for LinkedIn URL
        linkedin_url = candidate.get('linkedin_url', '')
        
        if linkedin_url and 'linkedin.com' in linkedin_url:
            print(f"📡 Attempting to fetch REAL LinkedIn data via API...")
            try:
                linkedin_data = self.fetch_real_linkedin_data(linkedin_url)
            except Exception as api_error:
                print(f"⚠️ LinkedIn API error: {str(api_error)[:100]}")
                print(f"   Falling back to LLM enrichment...")
                linkedin_data = {}
            
            # Check if we got valid LinkedIn data
            if linkedin_data and (linkedin_data.get('response_dict') or linkedin_data.get('data')):
                # Extract profile data
                profile = linkedin_data.get('response_dict') or linkedin_data.get('data', {})
                
                # Verify if this matches the candidate's email
                candidate_email = candidate.get('email', '').lower()
                linkedin_email = profile.get('email', '').lower()
                
                if candidate_email and linkedin_email and candidate_email == linkedin_email:
                    enriched_candidate['linkedin_email'] = profile.get('email', '')
                    enriched_candidate['linkedin_verified'] = True
                    enriched_candidate['linkedin_name'] = profile.get('name', '')
                    enriched_candidate['linkedin_picture'] = profile.get('picture', '')
                    enriched_candidate['linkedin_source'] = 'api_verified'
                    print("✅ LinkedIn profile verified via API (email match)")
                else:
                    enriched_candidate['linkedin_verified'] = False
                    enriched_candidate['linkedin_has_profile'] = True
                    enriched_candidate['linkedin_source'] = 'api_unverified'
                    print("✅ LinkedIn profile found via API (different account)")
            else:
                print("⚠️ LinkedIn API unavailable - will use LLM enrichment only")
                enriched_candidate['linkedin_source'] = 'llm_fallback'
        
        # Generate AI-powered LinkedIn fields
        print("🤖 Generating AI-enhanced LinkedIn fields...")
        ai_fields = self.generate_linkedin_fields_with_ai(enriched_candidate)
        
        if ai_fields:
            enriched_candidate.update(ai_fields)
            print("✅ AI LinkedIn fields generated successfully")
        else:
            print("⚠️ AI field generation failed")
        
        return enriched_candidate
    
    def enrich_multiple_candidates(self, candidates: list) -> list:
        """Enrich multiple candidates with LinkedIn data"""
        print(f"\n🔗 LINKEDIN ENRICHER: Processing {len(candidates)} candidates")
        print("=" * 50)
        
        enriched_candidates = []
        
        for i, candidate in enumerate(candidates, 1):
            print(f"[{i}/{len(candidates)}] Processing candidate...")
            
            try:
                enriched = self.enrich_candidate_profile(candidate)
                enriched_candidates.append(enriched)
                print(f"✅ Successfully enriched")
            except Exception as e:
                print(f"❌ Enrichment failed: {str(e)}")
                enriched_candidates.append(candidate)  # Keep original
        
        print(f"\n✅ LinkedIn enrichment complete: {len(enriched_candidates)} candidates processed")
        return enriched_candidates


def main():
    """Test the LinkedIn Enricher independently"""
    print("🔗 TESTING LINKEDIN ENRICHER MODULE")
    print("=" * 40)
    
    # Test with sample candidate
    test_candidate = {
        "full_name": "Test User",
        "email": "test@example.com",
        "current_role": "Software Engineer",
        "company": "Tech Corp",
        "skills": ["Python", "JavaScript", "React"],
        "linkedin_url": "https://www.linkedin.com/in/test-user"
    }
    
    enricher = LinkedInEnricher()
    result = enricher.enrich_candidate_profile(test_candidate)
    
    print("\n📊 Enrichment Result:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()