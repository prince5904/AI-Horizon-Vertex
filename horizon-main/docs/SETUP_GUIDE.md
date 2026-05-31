# 🚀 AI Recruiter Copilot - Complete Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Composio Setup](#composio-setup)
3. [API Keys Configuration](#api-keys-configuration)
4. [Testing Your Setup](#testing-your-setup)
5. [Common Issues](#common-issues)

## Prerequisites

### 1. System Requirements
- **Python 3.11+** installed
- **Internet connection** for API calls
- **Gmail account** (for email monitoring)
- **Google account** (same or different, for Sheets/Calendar)

### 2. Required Accounts

| Service | Purpose | Free Tier | Sign Up Link |
|---------|---------|-----------|--------------|
| Composio | App integrations | ✅ Yes | https://app.composio.dev |
| Groq | LLM inference | ✅ Yes (30 req/min) | https://console.groq.com |
| LinkedIn | Profile enrichment | ❌ Limited | linkedin.com |
| Gmail | Resume monitoring | ✅ Yes | gmail.com |

## Composio Setup

### Step 1: Create Composio Account

1. Visit https://app.composio.dev
2. Click "Sign Up" or "Get Started"
3. Complete registration (email verification required)
4. Verify your email address

### Step 2: Get Composio API Key

1. Log in to Composio dashboard
2. Click your profile icon (top right)
3. Select "Settings" from dropdown
4. Navigate to "API Keys" section
5. Click "Create New API Key"
6. Copy the key immediately (won't be shown again!)
7. Save to `.env` file:
   ```bash
   COMPOSIO_API_KEY=your_copied_key_here
   ```

### Step 3: Connect Gmail

**Why needed?** To monitor incoming emails with resume attachments.

1. Go to https://app.composio.dev/apps
2. Search for "Gmail" in the apps list
3. Click the "Gmail" card
4. Click "Connect" button
5. You'll be redirected to Google OAuth:
   - Select your Gmail account
   - Review permissions (Read emails, Send emails)
   - Click "Allow"
6. After authorization, you'll return to Composio
7. Go to https://app.composio.dev/connections
8. Find your Gmail connection (green checkmark)
9. Click "View Details" or expand the connection
10. Copy the following values:
    ```bash
    GMAIL_USER_ID=abc123...         # User identifier
    GMAIL_ACCOUNT_ID=gmail_acc_...  # Account identifier  
    GMAIL_AUTH_CONFIG_ID=config_... # Auth config ID
    ```

**Screenshot locations to find IDs:**
```
Composio Dashboard → Connections → Gmail → Details
┌─────────────────────────────────────────┐
│ Gmail Connection                        │
│ Status: ✅ Connected                    │
│ User ID: abc123                        │ ← Copy this
│ Account ID: gmail_acc_xyz              │ ← Copy this
│ Auth Config ID: config_123             │ ← Copy this
└─────────────────────────────────────────┘
```

### Step 4: Connect Google Sheets

**Why needed?** To export candidate data to organized spreadsheets.

1. Go to https://app.composio.dev/apps
2. Search for "Google Sheets"
3. Click "Connect"
4. OAuth flow (similar to Gmail):
   - Select Google account
   - Review permissions (Create, Read, Edit spreadsheets)
   - Click "Allow"
5. Go to https://app.composio.dev/connections
6. Find Google Sheets connection
7. Copy these values:
    ```bash
    GOOGLE_SHEETS_AUTH_CONFIG_ID=config_sheets_...
    GOOGLE_SHEETS_ACCOUNT_ID=sheets_acc_...
    GOOGLE_SHEETS_USER_ID=abc123  # Usually same as Gmail User ID
    ```

### Step 5: Connect Google Calendar

**Why needed?** To automatically schedule interview slots.

1. Go to https://app.composio.dev/apps
2. Search for "Google Calendar"
3. Click "Connect"
4. OAuth flow:
   - Select Google account (can be same as Sheets)
   - Review permissions (Create events, Read calendar)
   - Click "Allow"
5. Go to https://app.composio.dev/connections
6. Find Google Calendar connection
7. Copy these values:
    ```bash
    GOOGLE_CALENDAR_ACCOUNT_ID=cal_acc_...
    GOOGLE_CALENDAR_USER_ID=abc123  # Usually same as Gmail User ID
    GOOGLE_CALENDAR_AUTH_CONFIG_ID=config_cal_...
    ```

### Step 6: Connect LinkedIn (Optional)

**Why optional?** LinkedIn API has severe limitations. LLM enrichment works great without it.

**Note:** Most users don't have LinkedIn API access. Skip this if:
- You don't have LinkedIn API credentials
- You're okay with LLM-only enrichment (recommended)

If you have access:
1. Go to https://app.composio.dev/apps
2. Search for "LinkedIn"
3. Click "Connect"
4. Follow OAuth flow
5. Copy connection details:
    ```bash
    LINKEDIN_CONNECTED_ACCOUNT_ID=li_acc_...
    LINKEDIN_ENTITY_ID=abc123
    COMPOSIO_LINKEDIN_AUTH=Bearer_token...
    LINKEDIN_API_ENABLED=true  # Only if working properly
    ```

**Leave as `false` if not configured:**
```bash
LINKEDIN_API_ENABLED=false
```

## API Keys Configuration

### Groq API Key (Required)

**Why needed?** Powers all AI enrichment, scoring, and summarization.

1. Visit https://console.groq.com
2. Sign up with GitHub/Google or email
3. Verify email if required
4. Go to "API Keys" section
5. Click "Create API Key"
6. Name it: "AI Recruiter Copilot"
7. Copy the key (starts with `gsk_...`)
8. Add to `.env`:
    ```bash
    GROQ_API_KEY=gsk_your_key_here...
    ```

**Free Tier Limits:**
- 30 requests per minute
- Very fast inference (< 1 second)
- Perfect for this use case

### OpenAI API Key (Optional Backup)

**Why optional?** Only used if Groq fails (rare).

1. Visit https://platform.openai.com
2. Sign up and add payment method
3. Go to API Keys section
4. Create new secret key
5. Copy and add to `.env`:
    ```bash
    OPENAI_API_KEY=sk-proj-...
    ```

**Leave blank if not using:**
```bash
OPENAI_API_KEY=
```

## Complete .env File Example

After all setup steps, your `.env` should look like:

```bash
# Composio
COMPOSIO_API_KEY=composio_abc123xyz789...

# Gmail
GMAIL_USER_ID=user_abc123
GMAIL_ACCOUNT_ID=gmail_acc_xyz789
GMAIL_AUTH_CONFIG_ID=config_gmail_456

# Google Sheets
GOOGLE_SHEETS_AUTH_CONFIG_ID=config_sheets_789
GOOGLE_SHEETS_ACCOUNT_ID=sheets_acc_abc456
GOOGLE_SHEETS_USER_ID=user_abc123

# Google Calendar
GOOGLE_CALENDAR_ACCOUNT_ID=cal_acc_def789
GOOGLE_CALENDAR_USER_ID=user_abc123
GOOGLE_CALENDAR_AUTH_CONFIG_ID=config_cal_012

# LinkedIn (Optional - leave disabled if not configured)
LINKEDIN_CONNECTED_ACCOUNT_ID=
LINKEDIN_ENTITY_ID=
COMPOSIO_LINKEDIN_AUTH=
LINKEDIN_API_ENABLED=false

# Groq (Required)
GROQ_API_KEY=gsk_your_actual_key_here

# OpenAI (Optional)
OPENAI_API_KEY=

# App Settings (Optional)
DEBUG_MODE=false
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

## Testing Your Setup

### Step 1: Validate Configuration

```bash
# Activate virtual environment
.\comp\Scripts\Activate.ps1  # Windows
# source comp/bin/activate    # macOS/Linux

# Validate config
python scripts/validate_config.py
```

**Expected output:**
```
✅ Configuration validated successfully!
✅ COMPOSIO_API_KEY: Set and valid format
✅ GMAIL_USER_ID: Set
✅ GMAIL_ACCOUNT_ID: Set
✅ GROQ_API_KEY: Set and valid format
✅ All required credentials configured
```

**If you see errors:**
```
❌ COMPOSIO_API_KEY: Not set or invalid
```
→ Go back to that service's setup section above.

### Step 2: Run the Full Pipeline

```bash
python ai_recruiter_pipeline.py
```

**Expected output:**
```
🔍 STEP 1: Monitoring Gmail...
✅ Found 3 resumes

📄 STEP 2: Extracting...
✅ Extracted 3 candidates

� STEP 3: Enriching profiles...
✅ Enriched all profiles

🤖 STEP 4: Scoring candidates...
✅ 2 shortlisted, 1 rejected

📅 STEP 5-8: Scheduling & Export...
✅ Pipeline completed successfully!
```

**If you see:**
```
❌ Gmail authentication failed
```
→ Reconnect Gmail in Composio dashboard
→ Update IDs in `.env`

### Step 3: Test Full Pipeline (Dry Run)

```bash
# Send yourself a test email with a PDF resume attached
# Then run:
python ai_recruiter_pipeline.py
```

**Expected output:**
```
=== AI RECRUITER PIPELINE STARTED ===
✅ Step 1: Gmail Monitor - Found 1 email
✅ Step 2: Extract Resumes - Parsed 1 candidate
✅ Step 3: LinkedIn Enrich - Enriched via LLM
✅ Step 4: Scoring - Candidate scored 7.5/10
✅ Step 5: Interview Scheduled
✅ Step 6-7: Google Sheets created
✅ Step 8: CSV exported
=== PIPELINE COMPLETED ===
```

## Common Issues

### Issue 1: "Composio API key invalid"

**Symptoms:**
```
❌ Error: Invalid Composio API key
```

**Solutions:**
1. Check for extra spaces in `.env`:
   ```bash
   # WRONG:
   COMPOSIO_API_KEY= composio_123...  # Extra space!
   
   # CORRECT:
   COMPOSIO_API_KEY=composio_123...
   ```

2. Regenerate API key:
   - Go to Composio Settings
   - Delete old key
   - Create new key
   - Update `.env`

3. Check key hasn't expired:
   - Some keys have expiration dates
   - Create non-expiring key if available

### Issue 2: "Gmail connection not found"

**Symptoms:**
```
❌ Error: Connected account not found for Gmail
```

**Solutions:**
1. Verify connection status:
   - Go to https://app.composio.dev/connections
   - Gmail should have green checkmark
   - If red X, click "Reconnect"

2. Check User ID matches:
   ```bash
   # In .env, these should often be the same:
   GMAIL_USER_ID=user_abc123
   GOOGLE_SHEETS_USER_ID=user_abc123
   GOOGLE_CALENDAR_USER_ID=user_abc123
   ```

3. Connection expired:
   - Google OAuth tokens expire after ~7 days
   - Disconnect and reconnect Gmail

### Issue 3: "No resumes found"

**Symptoms:**
```
✅ Gmail connected
📧 Found 0 emails with attachments
```

**Solutions:**
1. Check email search criteria:
   - Pipeline looks for unread emails
   - From last 7 days
   - With PDF/TXT attachments

2. Send test email:
   ```
   To: yourself@gmail.com
   Subject: Test Resume - John Doe
   Attachment: sample_resume.pdf
   Body: Please review this candidate
   ```

3. Mark email as unread:
   - Pipeline only fetches unread emails
   - In Gmail, mark the test email as unread

### Issue 4: "Groq rate limit exceeded"

**Symptoms:**
```
❌ Groq API error: Rate limit exceeded (30 requests/minute)
```

**Solutions:**
1. Add delays between candidates:
   ```python
   # In ai_recruiter_pipeline.py
   import time
   time.sleep(2)  # 2 seconds between candidates
   ```

2. Reduce batch size:
   - Process fewer candidates per run
   - Run pipeline multiple times

3. Upgrade Groq plan:
   - Paid plans have higher limits
   - Visit https://console.groq.com/billing

### Issue 5: "LinkedIn enrichment failing"

**Expected Behavior!** This is normal.

**Why?** LinkedIn API has severe limitations. The system uses LLM enrichment as primary method.

**Action:** None needed. Verify you see:
```
🔗 Enriching LinkedIn profile for: John Doe
✅ Enriched via LLM (LinkedIn API unavailable)
```

This is the correct behavior. LLM enrichment is often better quality.

### Issue 6: "Google Sheets permission denied"

**Symptoms:**
```
❌ Error: Insufficient permissions to create spreadsheet
```

**Solutions:**
1. Reconnect Google Sheets:
   - Composio Dashboard → Connections
   - Google Sheets → Disconnect
   - Reconnect and re-authorize

2. Grant all permissions:
   - During OAuth, ensure you check:
     - ✅ Create spreadsheets
     - ✅ Edit spreadsheets
     - ✅ Read spreadsheet metadata

3. Use correct Google account:
   - Make sure authorizing with account that has Drive access
   - Check storage quota (need space for sheets)

### Issue 7: "Module not found errors"

**Symptoms:**
```
ModuleNotFoundError: No module named 'composio'
```

**Solutions:**
1. Activate virtual environment:
   ```bash
   # Windows
   .\comp\Scripts\Activate.ps1
   
   # macOS/Linux
   source comp/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements_minimal.txt
   ```

3. Check Python version:
   ```bash
   python --version  # Should be 3.11 or higher
   ```

## Getting Help

### Before Asking for Help

Run diagnostics:
```bash
python scripts/validate_config.py --verbose
```

This will show detailed information about your setup.

### Support Channels

1. **Composio Discord**: https://discord.gg/composio
   - Active community
   - Official support team
   - Response within hours

2. **Composio Docs**: https://docs.composio.dev
   - Comprehensive guides
   - API reference
   - Troubleshooting tips

3. **GitHub Issues**: [Your repo issues page]
   - Bug reports
   - Feature requests
   - Community support

### What to Include in Support Request

```markdown
**Environment:**
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Python: 3.11.5
- Composio version: [from pip show composio]

**Issue:**
[Describe what's happening]

**Expected:**
[What should happen]

**Steps to Reproduce:**
1. Run python ai_recruiter_pipeline.py
2. See error: [paste error]

**Logs:**
```
[Paste relevant log output]
```

**Config (without secrets):**
```bash
COMPOSIO_API_KEY=comp_abc... # (masked)
GMAIL_USER_ID=user_123
# etc.
```
```

## Next Steps

✅ Configuration complete!

**Now you can:**

1. **Run the pipeline:**
   ```bash
   python ai_recruiter_pipeline.py
   ```

2. **Visualize the workflow:**
   ```bash
   python scripts/visualize_pipeline.py
   ```

3. **Customize scoring criteria:**
   - Edit `src/utils/candidate_scorer.py`
   - Adjust weights and requirements in the DEFAULT_CRITERIA dict

4. **Integrate with your workflow:**
   - Schedule automatic runs
   - Customize email filters
   - Add more integrations

---

**🎉 Happy recruiting with AI! 🎉**
