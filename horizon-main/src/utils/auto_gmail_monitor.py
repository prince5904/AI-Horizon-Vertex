#!/usr/bin/env python3
"""
📧 AUTO GMAIL MONITOR
Automatically fetches message IDs and attachment IDs from Gmail
Downloads all resume PDFs automatically - no manual IDs needed!
"""

import os
import base64
from pathlib import Path
from typing import List, Dict, Optional
from composio import ComposioToolSet
from composio.client.enums import Action
from ..config.legacy_config import (
    COMPOSIO_API_KEY,
    GMAIL_ACCOUNT_ID,
    GMAIL_USER_ID,
    GMAIL_AUTH_CONFIG_ID
)

class AutoGmailMonitor:
    """Automatically monitors Gmail and downloads all resume PDFs"""
    
    def __init__(self):
        """Initialize with your Gmail credentials"""
        self.composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        
        # Your Gmail account details from environment variables
        self.gmail_account_id = GMAIL_ACCOUNT_ID
        self.user_id = GMAIL_USER_ID
        self.auth_config_id = GMAIL_AUTH_CONFIG_ID
        
        # Setup folders
        self.incoming_folder = Path("incoming_resumes")
        self.incoming_folder.mkdir(exist_ok=True)
        
        print("📧 Auto Gmail Monitor initialized")
        print(f"📁 Downloads folder: {self.incoming_folder.absolute()}")
    
    def list_recent_messages(self, max_results: int = 20) -> List[str]:
        """Get list of recent message IDs from Gmail that have PDF attachments"""
        try:
            print(f"📧 Fetching recent {max_results} emails from Gmail...")
            
            # Use GMAIL_FETCH_EMAILS to get recent messages with attachments
            response = self.composio_toolset.execute_action(
                action="GMAIL_FETCH_EMAILS",
                params={
                    "max_results": max_results,
                    "query": "has:attachment"  # Get all emails with attachments
                },
                entity_id=self.user_id
            )
            
            if response.get('successful'):
                messages = response.get('data', {}).get('messages', [])
                
                # Filter only messages that have PDF attachments
                pdf_message_ids = []
                for msg in messages:
                    message_id = msg.get('messageId')
                    if not message_id:
                        continue
                        
                    # Check if this message has PDF attachments
                    attachment_list = msg.get('attachmentList', [])
                    has_pdf = any(
                        att.get('filename', '').lower().endswith('.pdf') 
                        for att in attachment_list
                    )
                    
                    if has_pdf:
                        pdf_message_ids.append(message_id)
                
                print(f"✅ Found {len(pdf_message_ids)} emails with PDF attachments")
                return pdf_message_ids
            else:
                print(f"❌ Failed to fetch messages: {response.get('error', 'Unknown error')}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching messages: {str(e)}")
            return []
    
    def get_message_details(self, message_id: str) -> Optional[Dict]:
        """Get full message details including attachments using GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID"""
        try:
            print(f"📄 Getting details for message: {message_id}")
            
            response = self.composio_toolset.execute_action(
                action="GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID",
                params={
                    "message_id": message_id
                },
                entity_id=self.user_id
            )
            
            if response.get('successful'):
                return response.get('data')
            else:
                print(f"❌ Failed to get message details: {response.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting message details: {str(e)}")
            return None
    
    def extract_pdf_attachments(self, message_data: Dict) -> List[Dict]:
        """Extract PDF attachment info from message data"""
        attachments = []
        
        try:
            # Get email subject and sender for context
            headers = message_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
            
            print(f"📧 Email: '{subject}' from {sender}")
            
            def find_attachments_in_parts(parts, level=0):
                """Recursively find PDF attachments in email parts"""
                found_attachments = []
                
                for part in parts:
                    # Check if this part has a PDF attachment
                    filename = part.get('filename', '')
                    if filename and filename.lower().endswith('.pdf'):
                        attachment_id = part.get('body', {}).get('attachmentId')
                        size = part.get('body', {}).get('size', 0)
                        
                        if attachment_id:
                            found_attachments.append({
                                'filename': filename,
                                'attachment_id': attachment_id,
                                'size': size,
                                'subject': subject,
                                'sender': sender
                            })
                            print(f"📎 Found PDF: {filename} ({size} bytes)")
                    
                    # Check nested parts (multipart emails)
                    if 'parts' in part:
                        nested_attachments = find_attachments_in_parts(part['parts'], level + 1)
                        found_attachments.extend(nested_attachments)
                
                return found_attachments
            
            # Start searching from the main payload
            payload = message_data.get('payload', {})
            
            # Check if main payload is a PDF
            main_filename = payload.get('filename', '')
            if main_filename and main_filename.lower().endswith('.pdf'):
                attachment_id = payload.get('body', {}).get('attachmentId')
                size = payload.get('body', {}).get('size', 0)
                
                if attachment_id:
                    attachments.append({
                        'filename': main_filename,
                        'attachment_id': attachment_id,
                        'size': size,
                        'subject': subject,
                        'sender': sender
                    })
                    print(f"📎 Found PDF: {main_filename} ({size} bytes)")
            
            # Search in parts
            parts = payload.get('parts', [])
            if parts:
                part_attachments = find_attachments_in_parts(parts)
                attachments.extend(part_attachments)
            
            return attachments
            
        except Exception as e:
            print(f"❌ Error extracting attachments: {str(e)}")
            return []
    
    def download_pdf_attachment(self, message_id: str, attachment_id: str, filename: str) -> bool:
        """Download PDF attachment using GMAIL_GET_ATTACHMENT"""
        try:
            print(f"📥 Downloading: {filename}")
            
            # Check if file already exists
            file_path = self.incoming_folder / filename
            if file_path.exists():
                print(f"⚠️ File already exists, skipping: {filename}")
                return True
            
            response = self.composio_toolset.execute_action(
                action="GMAIL_GET_ATTACHMENT",
                params={
                    "message_id": message_id,
                    "attachment_id": attachment_id,
                    "file_name": filename
                },
                entity_id=self.user_id
            )
            
            if response.get('successful'):
                attachment_data = response.get('data', {})
                
                # Check if we got a file path (Composio downloaded it)
                downloaded_file_path = attachment_data.get('file', '')
                if downloaded_file_path and os.path.exists(downloaded_file_path):
                    # Move the file to our incoming folder
                    import shutil
                    shutil.move(downloaded_file_path, file_path)
                    print(f"✅ Downloaded: {filename}")
                    return True
                
                # Fallback: check for base64 data
                file_data = attachment_data.get('data', '')
                if file_data:
                    # Decode base64 data and save
                    decoded_data = base64.b64decode(file_data)
                    
                    with open(file_path, 'wb') as f:
                        f.write(decoded_data)
                    
                    print(f"✅ Downloaded: {filename} ({len(decoded_data)} bytes)")
                    return True
                
                print(f"❌ No file data received for {filename}")
                return False
            else:
                error_msg = response.get('error', 'Unknown error')
                print(f"❌ Download failed: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ Download error: {str(e)}")
            return False
    
    def auto_monitor_and_download(self, max_emails: int = 20) -> List[str]:
        """Automatically monitor Gmail and download all resume PDFs"""
        print("\n📧 AUTO GMAIL MONITOR: Scanning for resume PDFs")
        print("=" * 60)
        
        downloaded_files = []
        
        try:
            # Step 1: Get recent messages with PDF attachments directly  
            print(f"📧 Fetching recent {max_emails} emails from Gmail...")
            
            response = self.composio_toolset.execute_action(
                action="GMAIL_FETCH_EMAILS",
                params={
                    "max_results": max_emails,
                    "query": "has:attachment"
                },
                entity_id=self.user_id
            )
            
            if not response.get('successful'):
                print(f"❌ Failed to fetch messages: {response.get('error', 'Unknown error')}")
                return downloaded_files
            
            messages = response.get('data', {}).get('messages', [])
            print(f"🔍 Found {len(messages)} messages with attachments")
            
            # Step 2: Process each message that has PDF attachments
            pdf_count = 0
            for i, message in enumerate(messages, 1):
                message_id = message.get('messageId')
                if not message_id:
                    continue
                    
                # Check for PDF attachments in this message
                attachment_list = message.get('attachmentList', [])
                pdf_attachments = [
                    att for att in attachment_list 
                    if att.get('filename', '').lower().endswith('.pdf')
                ]
                
                if not pdf_attachments:
                    continue
                    
                pdf_count += len(pdf_attachments)
                subject = message.get('subject', 'No Subject')
                sender = message.get('sender', 'Unknown Sender')
                
                print(f"\n[{i}/{len(messages)}] Processing: '{subject}' from {sender}")
                print(f"📎 Found {len(pdf_attachments)} PDF attachment(s)")
                
                # Download each PDF attachment
                for attachment in pdf_attachments:
                    filename = attachment['filename']
                    attachment_id = attachment['attachmentId']
                    
                    success = self.download_pdf_attachment(message_id, attachment_id, filename)
                    
                    if success:
                        downloaded_files.append(filename)
            
            print(f"\n🎉 Auto monitoring complete!")
            print(f"📊 Found {pdf_count} total PDF attachments in {len(messages)} messages")
            print(f"📁 Downloaded {len(downloaded_files)} new resume files")
            
            if downloaded_files:
                print("� New resume files:")
                for file in downloaded_files:
                    print(f"   📄 {file}")
            else:
                print("📭 No new resume files were found")
            
            return downloaded_files
            
        except Exception as e:
            print(f"❌ Auto monitoring error: {str(e)}")
            return downloaded_files
    
    def get_folder_summary(self) -> Dict:
        """Get summary of incoming_resumes folder"""
        try:
            pdf_files = list(self.incoming_folder.glob("*.pdf"))
            txt_files = list(self.incoming_folder.glob("*.txt"))
            
            return {
                "folder_path": str(self.incoming_folder.absolute()),
                "pdf_count": len(pdf_files),
                "txt_count": len(txt_files),
                "total_files": len(pdf_files) + len(txt_files),
                "files": [f.name for f in pdf_files + txt_files]
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function to run auto Gmail monitoring"""
    print("📧 AUTO GMAIL MONITOR - Automatic Resume Detection")
    print("=" * 60)
    
    # Initialize auto monitor
    monitor = AutoGmailMonitor()
    
    # Show current folder status
    status = monitor.get_folder_summary()
    print(f"\n📁 Current incoming_resumes folder:")
    print(f"   PDF files: {status.get('pdf_count', 0)}")
    print(f"   TXT files: {status.get('txt_count', 0)}")
    print(f"   Total: {status.get('total_files', 0)} files")
    
    # Automatically scan Gmail and download resume PDFs
    new_files = monitor.auto_monitor_and_download(max_emails=10)
    
    # Show updated status
    updated_status = monitor.get_folder_summary()
    print(f"\n📊 Updated status:")
    print(f"   Total files now: {updated_status.get('total_files', 0)}")
    
    if new_files:
        print(f"\n🚀 Next step: Run the main pipeline to process new resumes:")
        print(f"   python ultimate_ai_recruiter_pipeline.py")
    else:
        print(f"\n💡 No new files downloaded. Current files can be processed with:")
        print(f"   python ultimate_ai_recruiter_pipeline.py")


if __name__ == "__main__":
    main()