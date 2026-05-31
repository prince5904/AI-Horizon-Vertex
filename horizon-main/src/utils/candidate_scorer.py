"""
Candidate Scoring Module
Evaluates candidates based on company criteria using Groq AI
Simple scoring logic - no Composio needed
"""

import os
import json
import time
from typing import Tuple, Dict, List
from groq import Groq


class CandidateScorer:
    """Score candidates based on company-defined criteria"""
    
    def __init__(self, groq_api_key: str = None, model: str = "llama-3.1-8b-instant"):
        """
        Initialize the scorer
        
        Args:
            groq_api_key: Groq API key (defaults to env var)
            model: Groq model to use for scoring
        """
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        if not self.client:
            print("⚠️  Warning: GROQ_API_KEY not found, will use heuristic scoring only")
        
    def _make_scoring_prompt(self, candidate: Dict, criteria: Dict) -> str:
        """Create the prompt for AI scoring"""
        return f"""You are an expert technical recruiter at a top company.
Evaluate the candidate strictly according to the following company criteria:
{json.dumps(criteria, indent=2)}

Candidate Details:
{json.dumps(candidate, indent=2)}

Provide a JSON output with:
- score: number between 1 and 10 (can include decimals like 8.5)
- rationale: one-paragraph explanation why the candidate deserves that score, highlighting strengths and gaps

Return only JSON. Example: {{"score": 8.7, "rationale": "Excellent skills in AI and leadership with 5 years experience. Minor gap in cloud computing."}}
"""

    def _heuristic_score(self, candidate: Dict, criteria: Dict) -> Tuple[float, str]:
        """
        Fallback heuristic scoring if AI is unavailable
        
        Scoring logic:
        - Each required skill match: +1.5 points
        - Each preferred skill match: +0.8 points
        - Each year of experience: +0.5 points
        - Max score: 10.0
        """
        skills = set(s.lower() for s in candidate.get("skills", []))
        required = set(s.lower() for s in criteria.get("required_skills", []))
        preferred = set(s.lower() for s in criteria.get("preferred_skills", []))
        
        required_matches = skills & required
        preferred_matches = skills & preferred
        experience_count = len(candidate.get("experience", []))
        
        # Calculate score
        skill_points = len(required_matches) * 1.5 + len(preferred_matches) * 0.8
        exp_points = experience_count * 0.5
        score = min(10.0, round(skill_points + exp_points, 1))
        
        rationale = (
            f"Matched {len(required_matches)}/{len(required)} required skills "
            f"({', '.join(required_matches) if required_matches else 'none'}), "
            f"{len(preferred_matches)}/{len(preferred)} preferred skills "
            f"({', '.join(preferred_matches) if preferred_matches else 'none'}), "
            f"with {experience_count} job experience(s)."
        )
        
        return score, rationale

    def score_candidate(self, candidate: Dict, criteria: Dict) -> Tuple[float, str]:
        """
        Score a candidate using AI or heuristic fallback
        
        Args:
            candidate: Candidate data dictionary
            criteria: Company criteria dictionary
            
        Returns:
            Tuple of (score, rationale)
        """
        # Try AI scoring first
        if self.client and self.api_key:
            try:
                prompt = self._make_scoring_prompt(candidate, criteria)
                
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0.3,
                )
                
                content = response.choices[0].message.content.strip()
                
                # Clean up markdown code blocks if present
                if content.startswith("```"):
                    lines = content.splitlines()
                    content = "\n".join(lines[1:-1]).strip()
                
                # Extract JSON
                start = content.find("{")
                end = content.rfind("}") + 1
                
                if start != -1 and end > start:
                    parsed = json.loads(content[start:end])
                    score = float(parsed.get("score", 0))
                    rationale = parsed.get("rationale", "")
                    
                    # Validate score range
                    score = max(0.0, min(10.0, score))
                    
                    return score, rationale
                    
            except Exception as e:
                print(f"⚠️  AI scoring failed ({str(e)}), falling back to heuristic...")
                time.sleep(0.2)
        
        # Fallback to heuristic
        return self._heuristic_score(candidate, criteria)

    def score_candidates(self, candidates: List[Dict], criteria: Dict, 
                        min_score: float = 4.0) -> List[Dict]:
        """
        Score multiple candidates and filter by minimum score
        
        Args:
            candidates: List of candidate dictionaries
            criteria: Company criteria dictionary
            min_score: Minimum score threshold for shortlisting
            
        Returns:
            List of shortlisted candidates with scores and rationale
        """
        shortlisted = []
        
        for candidate in candidates:
            name = candidate.get("full_name", candidate.get("name", "Unknown"))
            email = candidate.get("email", "")
            
            print(f"📊 Evaluating {name}...")
            
            score, rationale = self.score_candidate(candidate, criteria)
            
            print(f"   → Score: {score}/10")
            print(f"   → Rationale: {rationale[:100]}...")
            
            if score >= min_score:
                shortlisted.append({
                    "name": name,
                    "full_name": name,
                    "email": email,
                    "score": score,
                    "rationale": rationale,
                    "original_data": candidate  # Keep original for reference
                })
                print(f"   ✅ SHORTLISTED")
            else:
                print(f"   ❌ Below threshold ({min_score})")
        
        return shortlisted
    
    def score_single_candidate(self, candidate: Dict, criteria: Dict) -> Dict:
        """
        Score a single candidate and return enriched candidate dict with score
        
        Args:
            candidate: Candidate dictionary
            criteria: Company criteria dictionary
            
        Returns:
            Dict with 'score' and 'rationale' keys
        """
        score, rationale = self.score_candidate(candidate, criteria)
        return {
            "score": score,
            "rationale": rationale
        }


# Default company criteria (can be overridden)
DEFAULT_CRITERIA = {
    "role": "AI/Software Professional",
    "required_skills": [
        "python", "machine learning", "ai", "data science", 
        "software engineering", "algorithms"
    ],
    "preferred_skills": [
        "react", "node.js", "leadership", "cloud computing", 
        "project management", "deep learning", "nlp", "computer vision"
    ],
    "min_experience_years": 2,
    "values": ["innovation", "impact", "collaboration", "continuous learning"]
}


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    scorer = CandidateScorer()
    
    # Test candidate
    test_candidate = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "Machine Learning", "Deep Learning", "Leadership"],
        "experience": [
            {"title": "ML Engineer", "company": "TechCorp", "duration": "2 years"},
            {"title": "Data Scientist", "company": "DataInc", "duration": "3 years"}
        ]
    }
    
    score, rationale = scorer.score_candidate(test_candidate, DEFAULT_CRITERIA)
    print(f"\n🎯 Final Score: {score}/10")
    print(f"📝 Rationale: {rationale}")
