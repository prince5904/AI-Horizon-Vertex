# 🧪 Testing Guide - AI Recruiter Copilot

## Quick Test Commands

```bash
# Activate virtual environment first
.\comp\Scripts\Activate.ps1  # Windows
# source comp/bin/activate    # macOS/Linux

# Test 1: Configuration validation
python scripts/validate_config.py

# Test 2: Full pipeline (tests all components)
python ai_recruiter_pipeline.py

# Test 3: Workflow visualization
python scripts/visualize_pipeline.py
```

## Testing Approach

This project uses **end-to-end testing** through the main pipeline rather than unit tests. Each component is tested when you run the pipeline.

### Why No Unit Tests?

For a hackathon project, we prioritize:
- ✅ **Working pipeline** - Prove the concept works end-to-end
- ✅ **Configuration validation** - Ensure setup is correct
- ✅ **Sample data** - Examples for testing enrichment
- ✅ **Error handling** - Graceful failures with clear messages

**Future Enhancement**: Unit tests can be added in the `tests/` directory structure for production use.

## Integration Tests

### Test 1: Configuration Validation

**Purpose**: Verify all API keys and configurations are valid

**Command**:
```bash
python ai_recruiter_pipeline.py
```

**Expected Output**:
```
🔍 STEP 1: Monitoring Gmail...
✅ Gmail connection successful
📧 Found 3 unread emails with resumes

� STEP 2: Extracting resumes...
✅ Extracted 3 candidate profiles

🔗 STEP 3: Enriching profiles...
✅ Enriched 3 profiles (LinkedIn API + LLM fallback)

🤖 STEP 4: Scoring candidates...
✅ Candidate 1: 8.5/10 - SHORTLISTED
✅ Candidate 2: 7.2/10 - SHORTLISTED
❌ Candidate 3: 4.1/10 - REJECTED

📅 STEP 5: Scheduling interviews...
✅ 2 interviews scheduled in Google Calendar

📊 STEP 6-8: Exporting data...
✅ All candidates sheet created
✅ Interview schedule sheet created
✅ CSV exported to output/
```

**If it fails**:
1. Check `.env` for all required credentials
2. Run `python scripts/validate_config.py` to diagnose
3. Reconnect apps in Composio dashboard if needed

### Test 2: Configuration Validation

**Purpose**: Verify all API keys and configurations

**Command**:
```bash
python scripts/validate_config.py
```

**Expected Output**:
```
✅ Composio API Key: Valid
✅ Groq API Key: Valid
✅ Gmail Configuration: Complete
✅ Google Calendar Configuration: Complete
✅ Google Sheets Configuration: Complete
⚠️  LinkedIn Configuration: Optional (not configured)

All required configurations are valid!
```

### Test 3: Workflow Visualization

**Purpose**: Generate workflow diagram

**Command**:
```bash
python scripts/visualize_pipeline.py
```

**Expected Output**:
```
✅ Workflow diagram generated
📊 Saved to: output/recruitment_pipeline_graph.png
```

**Expected Output**:
```
=== AI RECRUITER PIPELINE (SAMPLE MODE) ===
✅ Step 1: Loaded 3 sample candidates
✅ Step 2: Enrichment complete
✅ Step 3: Scoring complete (2 shortlisted)
✅ Step 4: Interviews scheduled
✅ Step 5-6: Google Sheets created
✅ Step 7: Export complete
=== PIPELINE COMPLETED ===
```

## Manual Test Scenarios

### Scenario 1: Process Real Resumes

**Steps**:
1. Send email to yourself with resume PDF attached
2. Subject: "Resume - [Candidate Name]"
3. Mark as unread
4. Run: `python ai_recruiter_pipeline.py`
5. Verify candidate appears in Google Sheets

**Success Criteria**:
- ✅ Email detected
- ✅ PDF extracted
- ✅ Profile enriched
- ✅ Candidate scored
- ✅ Sheet updated
- ✅ CSV exported

### Scenario 2: Multiple Candidates

**Steps**:
1. Send 5 emails with different resumes
2. Run pipeline
3. Verify all candidates processed

**Success Criteria**:
- ✅ All 5 candidates extracted
- ✅ All enriched (LinkedIn or LLM)
- ✅ Scored appropriately
- ✅ Shortlisted candidates get calendar events
- ✅ All appear in "All Candidates" sheet
- ✅ Only shortlisted in "Interview Schedule" sheet

### Scenario 3: Error Handling

**Test graceful failures**:

1. **Invalid PDF**:
   - Send email with corrupted PDF
   - Expected: Skipped with error message

2. **Rate Limit**:
   - Process 40+ candidates quickly
   - Expected: Retry with delays

3. **Missing Credentials**:
   - Remove one API key from `.env`
   - Expected: Clear error message

## Performance Tests

### Test Throughput

```bash
# Time the pipeline with different loads
time python ai_recruiter_pipeline.py
```

**Benchmarks** (on average hardware):
- 1 candidate: ~8-12 seconds
- 5 candidates: ~35-50 seconds
- 10 candidates: ~70-100 seconds

**Bottlenecks**:
- LLM API calls (2-5 sec each)
- Google Sheets API (1-3 sec each)
- LinkedIn API attempts (3-5 sec timeouts)

### Test Concurrent Processing

```python
# Run multiple pipelines simultaneously
# From different terminals:

# Terminal 1
python ai_recruiter_pipeline.py

# Terminal 2
python ai_recruiter_pipeline.py

# Both should complete without conflicts
```

## Sample Data Tests

### Using Provided Samples

```bash
# Test with examples/sample_candidates.json
python -c "
import json
from src.workflows.recruitment_pipeline import RecruitmentPipeline

# Load sample data
with open('examples/sample_candidates.json') as f:
    data = json.load(f)
    
# Process with pipeline
pipeline = RecruitmentPipeline()
results = pipeline.process_candidates(data['candidates'])

print(f'✅ Processed {len(results)} candidates')
"
```

## Validation Tests

### Test 1: Configuration Validation

```bash
python scripts/validate_config.py --verbose
```

**Checks**:
- ✅ All required env vars set
- ✅ API keys valid format
- ✅ Composio connection active
- ✅ Groq API accessible

### Test 2: Data Validation

```python
# Validate enriched output schema
from pydantic import BaseModel, ValidationError
import json

class EnrichedCandidate(BaseModel):
    name: str
    email: str
    enriched_data: dict
    scoring: dict
    
# Load and validate
with open('examples/sample_enriched_output.json') as f:
    data = json.load(f)
    candidate = EnrichedCandidate(**data)
    print("✅ Output schema valid")
```

## Debugging Tests

### Enable Debug Mode

```bash
# In .env file
DEBUG_MODE=true

# Then run pipeline
python ai_recruiter_pipeline.py
```

**Output includes**:
- Detailed API request/response logs
- State transitions in LangGraph
- Token usage per LLM call
- Timing for each node

### Inspect State

```python
# Add breakpoint in ai_recruiter_pipeline.py
from langgraph.graph import StateGraph

def linkedin_enrich(state):
    import pdb; pdb.set_trace()  # Add breakpoint
    # Inspect state variables
    print(f"Current state: {state}")
    return state
```

## Load Tests

### Stress Test

```bash
# Process many candidates
python ai_recruiter_pipeline.py --batch-size 50
```

**Monitor**:
- CPU usage (should stay < 80%)
- Memory usage (should stay < 2GB)
- API rate limits
- Error rates

### Reliability Test

```bash
# Run pipeline repeatedly
for i in {1..10}; do
    echo "Run $i"
    python ai_recruiter_pipeline.py
    sleep 60
done
```

**Success Criteria**:
- ✅ All runs complete successfully
- ✅ No memory leaks
- ✅ No connection errors
- ✅ Consistent performance

## Troubleshooting

### Common Issues

#### 1. "Composio connection failed"

**Cause**: API keys expired or invalid

**Fix**:
```bash
# Regenerate Composio API key
# Update .env
python scripts/validate_config.py
```

#### 2. "Groq rate limit exceeded"

**Cause**: Too many API calls

**Fix**:
- Wait a few minutes before retrying
- Reduce `max_emails` parameter in `ai_recruiter_pipeline.py`
- Consider upgrading Groq plan

#### 3. "Google Sheets quota exceeded"

**Cause**: Too many API calls to Google Sheets

**Fix**:
- Wait before creating new sheets
- Reuse existing sheets instead of creating new ones
- Use batch operations where possible

#### 4. "No resumes found in Gmail"

**Cause**: No unread emails with attachments

**Fix**:
- Check Gmail inbox for unread emails
- Ensure emails have PDF or TXT attachments
- Try manually marking an email as unread

## Testing Checklist

Before deploying or demoing, ensure all work:

- [ ] Configuration validation passes (`scripts/validate_config.py`)
- [ ] Full pipeline runs successfully (`ai_recruiter_pipeline.py`)
- [ ] Gmail connection works (downloads resumes)
- [ ] PDF extraction works (parses candidate data)
- [ ] LinkedIn/LLM enrichment works (adds profile details)
- [ ] Candidate scoring works (AI evaluation)
- [ ] Conditional routing works (threshold filtering)
- [ ] Interview scheduling works (Google Calendar events)
- [ ] Google Sheets creation works (2 sheets generated)
- [ ] CSV export works (saved to `output/`)
- [ ] Workflow visualization works (`scripts/visualize_pipeline.py`)
- [ ] Error handling works gracefully
- [ ] Performance acceptable (< 15 sec per candidate)
- [ ] No hardcoded secrets in code
- [ ] Documentation up to date

## Future Enhancements

For production use, consider adding:
- ✨ **Unit Tests**: pytest tests for each utility module
- ✨ **Integration Tests**: Mock API calls for faster testing
- ✨ **CI/CD Pipeline**: Automated testing on GitHub Actions
- ✨ **Test Coverage**: Coverage reports for code quality
- ✨ **Pre-commit Hooks**: Automatic linting and formatting

---

**✅ All tests passing? Ready to deploy! 🚀**
