# 🎨 How to View the LangGraph Visualization

## Quick Start

### **See the Complete Graph with All Details:**

```bash
# Activate virtual environment
.\comp\Scripts\Activate.ps1

# Run the visualization script
python visualize_pipeline.py
```

This will display:
- ✅ ASCII graph with all 8 nodes
- ✅ Detailed breakdown of each node
- ✅ Conditional routing logic
- ✅ Output files explanation
- ✅ Example execution flow

---

## What You'll See in the Graph

### **8 Separate Nodes:**

1. **gmail_monitor** - Downloads resumes from Gmail
2. **extract_resumes** - Parses PDFs with AI
3. **linkedin_enrich** - Tries LinkedIn API, falls back to LLM
4. **score_candidates** - AI scoring with decision point
5. **schedule_interviews** - Creates calendar events (conditional)
6. **create_all_candidates_sheet** - Sheet for ALL candidates
7. **create_interview_sheet** - Sheet for SHORTLISTED only
8. **final_report** - Displays all links

### **Special Features Visible:**

- **Dotted lines** = Conditional routing (may skip scheduling)
- **Solid lines** = Sequential flow (always executes)
- **Decision diamond** = Score threshold check at `score_candidates`
- **Two paths merge** = Both routes converge at `create_all_candidates_sheet`

---

## Graph Output Example

```
                     +-----------+
                     | __start__ |
                     +-----------+
                            *
                   +---------------+
                   | gmail_monitor |
                   +---------------+
                            *
                  +-----------------+
                  | extract_resumes |
                  +-----------------+
                            *
                  +-----------------+
                  | linkedin_enrich |  ← Shows enrichment!
                  +-----------------+
                            *
                  +------------------+
                  | score_candidates |  ← Decision point!
                  +------------------+
                   ..              ...
                ...                   ..
              ..                        ...
+---------------------+                    ..
| schedule_interviews |                 ...  ← Conditional!
+---------------------+               ..
                   **              ...
                     ***        ...
                        **    ..
            +-----------------------------+
            | create_all_candidates_sheet |  ← All 4 candidates!
            +-----------------------------+
                            *
              +------------------------+
              | create_interview_sheet |  ← Selected 3!
              +------------------------+
                            *
                    +--------------+
                    | final_report |
                    +--------------+
```

---

## Key Things the Graph Shows

### ✅ **LinkedIn Enrichment is Visible**
- Separate `linkedin_enrich` node
- Shows it's a distinct operation
- Internally tries API first, then LLM fallback

### ✅ **Two Separate Sheets**
- `create_all_candidates_sheet` - Database of all applicants
- `create_interview_sheet` - Schedule for shortlisted only

### ✅ **Calendar Integration**
- `schedule_interviews` node is conditional
- Only runs if candidates meet score threshold
- Creates Google Calendar events with invitations

### ✅ **Conditional Routing**
- Dotted lines from `score_candidates` show decision point
- Two possible paths based on shortlisted count
- Paths merge at `create_all_candidates_sheet`

---

## Files Generated

### **Documentation:**
- `GRAPH_VISUALIZATION_GUIDE.md` - Complete breakdown
- `ADVANCED_LANGGRAPH_PIPELINE.md` - Technical details
- `visualize_pipeline.py` - Interactive graph viewer

### **Graph Images:**
- `recruitment_pipeline_graph.png` - Mermaid diagram (if API available)
- ASCII output in console

---

## Run the Full Pipeline

To execute the entire workflow and see it in action:

```bash
python ai_recruiter_pipeline.py
```

This will:
1. Generate the graph visualization
2. Run all 8 nodes
3. Show conditional routing decisions
4. Display all output links

---

## Troubleshooting

### **Graph image not generating?**
- Mermaid API might be unavailable
- Use ASCII visualization instead: `python visualize_pipeline.py`

### **Want to see the graph programmatically?**
```python
from ai_recruiter_pipeline import create_recruitment_pipeline

pipeline = create_recruitment_pipeline()
print(pipeline.get_graph().draw_ascii())
```

---

## 🎯 Summary

The graph now shows **every detail** you requested:

✅ LinkedIn enrichment (with API → LLM fallback strategy)
✅ All candidates sheet creation
✅ Selected candidates sheet creation (separate)
✅ Calendar event generation
✅ Conditional routing logic
✅ 8 separate nodes (not just 7!)

**This is exactly what you asked for** - the graph image shows everything happening in the pipeline, with all sub-operations visible as separate nodes! 🚀
