"""
Interview Scheduler Module
Schedules interviews in Google Calendar using Composio
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from composio import ComposioToolSet, Action
from ..config.legacy_config import (
    COMPOSIO_API_KEY, 
    GOOGLE_CALENDAR_USER_ID, 
    GOOGLE_CALENDAR_ACCOUNT_ID,
    GOOGLE_CALENDAR_AUTH_CONFIG_ID
)


class InterviewScheduler:
    """Schedule interviews using Composio Google Calendar integration"""
    
    def __init__(self, composio_api_key: str = None, entity_id: str = None):
        """
        Initialize the scheduler
        
        Args:
            composio_api_key: Composio API key (defaults to config)
            entity_id: Entity ID for Composio actions (defaults to GOOGLE_CALENDAR_USER_ID)
        """
        self.api_key = composio_api_key or COMPOSIO_API_KEY
        self.entity_id = entity_id or GOOGLE_CALENDAR_USER_ID
        self.connected_account_id = GOOGLE_CALENDAR_ACCOUNT_ID
        self.auth_config_id = GOOGLE_CALENDAR_AUTH_CONFIG_ID
        self.toolset = ComposioToolSet(api_key=self.api_key)
        
        print("📅 Interview Scheduler initialized with ComposioToolSet")
        print(f"   Entity ID: {self.entity_id}")
        print(f"   Account ID: {self.connected_account_id}")
        
    def _generate_time_slots(
        self, 
        num_slots: int,
        start_date: datetime = None,
        start_hour: int = 9,
        duration_minutes: int = 45,
        skip_weekends: bool = True
    ) -> List[datetime]:
        """
        Generate interview time slots
        
        Args:
            num_slots: Number of slots needed
            start_date: Starting date (defaults to tomorrow)
            start_hour: Starting hour (9 AM by default)
            duration_minutes: Duration of each interview
            skip_weekends: Whether to skip Saturdays and Sundays
            
        Returns:
            List of datetime objects for each slot
        """
        if start_date is None:
            start_date = datetime.now() + timedelta(days=1)
            start_date = start_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        
        slots = []
        current_slot = start_date
        
        while len(slots) < num_slots:
            # Skip weekends if requested
            if skip_weekends and current_slot.weekday() >= 5:  # 5=Saturday, 6=Sunday
                # Move to next Monday at start_hour
                days_ahead = 7 - current_slot.weekday()
                current_slot = current_slot + timedelta(days=days_ahead)
                current_slot = current_slot.replace(hour=start_hour, minute=0)
                continue
            
            # Check if within business hours (9 AM - 6 PM)
            if current_slot.hour < 9 or current_slot.hour >= 18:
                # Move to next day at start_hour
                current_slot = current_slot + timedelta(days=1)
                current_slot = current_slot.replace(hour=start_hour, minute=0)
                continue
            
            slots.append(current_slot)
            current_slot = current_slot + timedelta(minutes=duration_minutes)
        
        return slots

    def create_calendar_event(
        self,
        candidate: Dict,
        interview_datetime: datetime,
        duration_minutes: int = 45,
        meeting_link: str = None
    ) -> Optional[Dict]:
        """
        Create a Google Calendar event for an interview
        
        Args:
            candidate: Candidate dictionary with name, email, score, rationale
            interview_datetime: When the interview should be scheduled
            duration_minutes: Duration of the interview
            meeting_link: Optional meeting link (Zoom, Meet, etc.)
            
        Returns:
            Result dictionary from Composio action
        """
        try:
            name = candidate.get("name", candidate.get("full_name", "Candidate"))
            email = candidate.get("email")
            score = candidate.get("score", "N/A")
            rationale = candidate.get("rationale", "")
            
            # Calculate end time
            end_datetime = interview_datetime + timedelta(minutes=duration_minutes)
            
            # Format times for Google Calendar API (RFC3339)
            start_time = interview_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Build event summary and description
            summary = f"Interview: {name} (Score: {score})"
            
            description_parts = [
                f"🎯 Candidate Interview",
                f"",
                f"👤 Name: {name}",
                f"📧 Email: {email}" if email else "",
                f"⭐ Score: {score}/10",
                f"",
                f"📝 Evaluation Rationale:",
                rationale,
                f"",
                f"🔗 Meeting Link: {meeting_link}" if meeting_link else "ℹ️ Meeting link to be added",
            ]
            description = "\n".join([p for p in description_parts if p])
            
            # Prepare attendees
            attendees = []
            if email:
                attendees.append({"email": email})
            
            # Create event using Composio
            print(f"📅 Creating calendar event for {name} at {interview_datetime.strftime('%Y-%m-%d %I:%M %p')}")
            
            # Prepare event data for Composio GOOGLECALENDAR_CREATE_EVENT
            event_params = {
                "summary": summary,
                "description": description,
                "start_datetime": start_time,
                "end_datetime": end_time,
                "attendees": [email] if email else []  # List of email addresses
            }
            
            result = self.toolset.execute_action(
                action=Action.GOOGLECALENDAR_CREATE_EVENT,
                params=event_params,
                entity_id=self.entity_id
            )
            
            if result.get("successful") or result.get("success"):
                print(f"   ✅ Event created successfully")
                return result
            else:
                error_msg = result.get('error', result.get('data', 'Unknown error'))
                print(f"   ❌ Failed to create event: {error_msg}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating calendar event for {candidate.get('name', 'Unknown')}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def schedule_interviews(
        self,
        shortlisted_candidates: List[Dict],
        start_date: datetime = None,
        duration_minutes: int = 45,
        meeting_link: str = None
    ) -> List[Dict]:
        """
        Schedule interviews for all shortlisted candidates
        
        Args:
            shortlisted_candidates: List of candidate dictionaries
            start_date: Starting date for scheduling (defaults to tomorrow)
            duration_minutes: Duration of each interview
            meeting_link: Optional meeting link for all interviews
            
        Returns:
            List of candidates with added schedule information
        """
        if not shortlisted_candidates:
            print("ℹ️  No candidates to schedule")
            return []
        
        # Generate time slots
        num_candidates = len(shortlisted_candidates)
        time_slots = self._generate_time_slots(
            num_slots=num_candidates,
            start_date=start_date,
            duration_minutes=duration_minutes
        )
        
        scheduled_candidates = []
        
        for candidate, slot in zip(shortlisted_candidates, time_slots):
            # Create calendar event
            result = self.create_calendar_event(
                candidate=candidate,
                interview_datetime=slot,
                duration_minutes=duration_minutes,
                meeting_link=meeting_link
            )
            
            # Add schedule info to candidate
            candidate_with_schedule = candidate.copy()
            candidate_with_schedule.update({
                "interview_date": slot.strftime("%Y-%m-%d"),
                "interview_time": slot.strftime("%I:%M %p"),
                "interview_datetime": slot.isoformat(),
                "duration_minutes": duration_minutes,
                "calendar_event_created": result is not None,
                "calendar_event_data": result
            })
            
            scheduled_candidates.append(candidate_with_schedule)
        
        print(f"\n✅ Scheduled {len(scheduled_candidates)} interview(s)")
        return scheduled_candidates


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    scheduler = InterviewScheduler()
    
    # Test candidate
    test_candidates = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "score": 8.5,
            "rationale": "Excellent skills in AI and leadership with 5 years experience."
        }
    ]
    
    scheduled = scheduler.schedule_interviews(test_candidates)
    print(f"\n📅 Scheduled interviews: {len(scheduled)}")
    for candidate in scheduled:
        print(f"   - {candidate['name']}: {candidate['interview_date']} at {candidate['interview_time']}")
