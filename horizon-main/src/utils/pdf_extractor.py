#!/usr/bin/env python3
"""
📄 PDF EXTRACTOR MODULE  
Handles PDF and text resume processing with comprehensive data extraction
"""

import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Optional
from groq import Groq
from ..config.legacy_config import GROQ_API_KEY, GROQ_MODEL


class PDFExtractor:
    """PDF and Text Resume Processing Service"""
    
    def __init__(self):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.input_dir = Path("./incoming_resumes")
        self.output_dir = Path("./processed_candidates")
        self.output_dir.mkdir(exist_ok=True)
        print("📄 PDF Extractor initialized")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            print(f"📖 Extracting text from PDF: {pdf_path.name}")
            doc = fitz.open(pdf_path)
            text = ""
            page_count = doc.page_count
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                text += page_text
                
            doc.close()
            
            print(f"✅ Extracted {len(text)} characters from {page_count} pages")
            return text.strip()
            
        except Exception as e:
            print(f"❌ PDF extraction error for {pdf_path}: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, txt_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            print(f"📝 Reading text file: {txt_path.name}")
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            print(f"✅ Extracted {len(text)} characters")
            return text
            
        except Exception as e:
            print(f"❌ TXT extraction error for {txt_path}: {str(e)}")
            return ""
    
    def parse_resume_with_ai(self, text: str, filename: str) -> Optional[Dict]:
        """Parse resume text using advanced AI prompting for comprehensive extraction"""
        try:
            print(f"🤖 Processing with AI: {filename}")
            
            prompt = f"""
            You are an expert resume parser. Extract ALL available information from this resume and return ONLY a JSON object.
            
            REQUIRED JSON STRUCTURE:
            {{
                "full_name": "Full candidate name",
                "email": "email@domain.com",
                "phone": "Phone number with country code",
                "location": "City, State/Country",
                "current_role": "Most recent job title",
                "company": "Current/most recent company",
                "summary": "Professional summary if present",
                "years_of_experience": "Total years or estimate",
                "skills": ["technical skills", "languages", "frameworks", "tools", "certifications"],
                "experience": [
                    {{
                        "title": "Job Title",
                        "company": "Company Name", 
                        "duration": "Start - End dates",
                        "location": "City, State",
                        "description": "Key responsibilities and achievements",
                        "achievements": ["Quantified achievement 1", "Achievement 2"]
                    }}
                ],
                "education": [
                    {{
                        "degree": "Full degree name",
                        "field": "Field of study",
                        "institution": "University/College name",
                        "year": "Graduation year",
                        "gpa": "GPA if mentioned",
                        "location": "City, State"
                    }}
                ],
                "certifications": ["Certification 1", "License 1"],
                "projects": [
                    {{
                        "name": "Project Name",
                        "description": "Brief description",
                        "technologies": ["tech1", "tech2"],
                        "duration": "Project timeframe"
                    }}
                ],
                "languages": ["Language (proficiency)"],
                "linkedin_url": "LinkedIn URL if found",
                "github_url": "GitHub URL if found", 
                "portfolio_url": "Portfolio URL if found",
                "awards": ["Award 1", "Achievement 1"],
                "publications": ["Publication 1"],
                "volunteer_experience": ["Organization - Role"],
                "salary_expectation": "Salary info if mentioned",
                "availability": "Start date if mentioned",
                "visa_status": "Work authorization if mentioned",
                "preferred_roles": ["Preferred role types"],
                "industry_preference": "Preferred industry"
            }}
            
            EXTRACTION RULES:
            1. Extract ALL contact info (email, phone, LinkedIn, GitHub, portfolio)
            2. Get complete work history with quantified achievements  
            3. Extract ALL skills (technical + soft skills + tools)
            4. Get full education (degree, school, GPA, honors)
            5. Find certifications, licenses, courses
            6. Extract projects with technologies
            7. Look for awards, publications, volunteer work
            8. Find salary expectations, availability, visa status
            9. If info missing, use empty string or empty array
            10. BE THOROUGH - this is for detailed recruiter screening
            
            Resume Text:
            {text}
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                temperature=0.1,
                max_tokens=2500
            )
            
            ai_text = response.choices[0].message.content.strip()
            print(f"🧠 AI response received ({len(ai_text)} characters)")
            
            # Parse JSON response
            try:
                parsed_data = json.loads(ai_text)
                print("✅ JSON parsed successfully")
                return parsed_data
            except json.JSONDecodeError:
                # Try to extract JSON from code block
                if "```json" in ai_text:
                    json_start = ai_text.find("```json") + 7
                    json_end = ai_text.find("```", json_start)
                    json_text = ai_text[json_start:json_end].strip()
                    parsed_data = json.loads(json_text)
                    print("✅ JSON extracted from code block")
                    return parsed_data
                else:
                    print("❌ Failed to parse AI response as JSON")
                    return None
                    
        except Exception as e:
            print(f"❌ AI parsing error for {filename}: {str(e)}")
            return None
    
    def process_single_file(self, file_path: Path) -> Optional[Dict]:
        """Process a single resume file (PDF or TXT)"""
        print(f"\n📄 Processing: {file_path.name}")
        print("-" * 40)
        
        try:
            # Extract text based on file type
            if file_path.suffix.lower() == '.pdf':
                text = self.extract_text_from_pdf(file_path)
            elif file_path.suffix.lower() in ['.txt', '.text']:
                text = self.extract_text_from_txt(file_path)
            else:
                print(f"❌ Unsupported file type: {file_path.suffix}")
                return None
            
            if not text:
                print(f"❌ No text extracted from {file_path.name}")
                return None
            
            # Parse with AI
            candidate_data = self.parse_resume_with_ai(text, file_path.name)
            
            if not candidate_data:
                print(f"❌ Failed to parse {file_path.name}")
                return None
            
            # Add metadata
            candidate_data['source'] = 'pdf_resume'
            candidate_data['source_file'] = str(file_path.name)
            candidate_data['extraction_timestamp'] = str(Path().resolve())
            
            # Save individual candidate file
            timestamp = Path().resolve().name.split('_')[-1] if '_' in str(Path().resolve()) else "unknown"
            output_file = self.output_dir / f"{file_path.stem}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(candidate_data, f, indent=2, ensure_ascii=False)
            
            name = candidate_data.get('full_name', 'Unknown')
            email = candidate_data.get('email', 'No email')
            print(f"✅ Successfully processed: {name} ({email})")
            print(f"💾 Saved to: {output_file}")
            
            return candidate_data
            
        except Exception as e:
            print(f"❌ Processing error for {file_path.name}: {str(e)}")
            return None
    
    def extract_from_directory(self, input_dir: Path = None) -> List[Dict]:
        """Process all PDF and TXT files from input directory"""
        if input_dir is None:
            input_dir = self.input_dir
            
        print(f"\n📄 PDF EXTRACTOR: Processing files from {input_dir}")
        print("=" * 55)
        
        if not input_dir.exists():
            print(f"❌ Directory {input_dir} not found")
            return []
        
        # Find all supported files
        supported_files = []
        for ext in ['*.pdf', '*.txt', '*.text']:
            supported_files.extend(list(input_dir.glob(ext)))
        
        if not supported_files:
            print(f"❌ No PDF or TXT files found in {input_dir}")
            return []
        
        print(f"📋 Found {len(supported_files)} files to process")
        
        processed_candidates = []
        
        for i, file_path in enumerate(supported_files, 1):
            print(f"\n[{i}/{len(supported_files)}] Processing file...")
            
            candidate_data = self.process_single_file(file_path)
            
            if candidate_data:
                processed_candidates.append(candidate_data)
            else:
                print(f"⚠️ Skipped {file_path.name} due to processing errors")
        
        print(f"\n✅ PDF extraction complete: {len(processed_candidates)}/{len(supported_files)} files processed successfully")
        
        return processed_candidates
    
    def get_processing_summary(self, candidates: List[Dict]) -> Dict:
        """Generate processing summary statistics"""
        if not candidates:
            return {"total": 0, "with_email": 0, "with_linkedin": 0, "with_skills": 0}
        
        summary = {
            "total": len(candidates),
            "with_email": len([c for c in candidates if c.get('email')]),
            "with_linkedin": len([c for c in candidates if c.get('linkedin_url')]),
            "with_skills": len([c for c in candidates if c.get('skills')]),
            "with_experience": len([c for c in candidates if c.get('experience')]),
            "with_education": len([c for c in candidates if c.get('education')]),
            "avg_skills_per_candidate": sum(len(c.get('skills', [])) for c in candidates) / len(candidates)
        }
        
        return summary


def main():
    """Test the PDF Extractor independently"""
    print("📄 TESTING PDF EXTRACTOR MODULE")
    print("=" * 40)
    
    extractor = PDFExtractor()
    
    # Process all files in directory
    candidates = extractor.extract_from_directory()
    
    # Show summary
    summary = extractor.get_processing_summary(candidates)
    print(f"\n📊 PROCESSING SUMMARY:")
    print(f"   Total candidates: {summary['total']}")
    print(f"   With email: {summary['with_email']}")
    print(f"   With LinkedIn: {summary['with_linkedin']}")
    print(f"   With skills: {summary['with_skills']}")
    print(f"   Avg skills per candidate: {summary['avg_skills_per_candidate']:.1f}")
    
    if candidates:
        print(f"\n📋 Sample candidate:")
        sample = candidates[0]
        print(f"   Name: {sample.get('full_name')}")
        print(f"   Email: {sample.get('email')}")
        print(f"   Skills: {len(sample.get('skills', []))} extracted")


if __name__ == "__main__":
    main()