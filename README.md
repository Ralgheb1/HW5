# Suicide Ideation Language Markers - AI Skill

## What this skill does
Detects and scores suicide ideation language patterns in therapy conversations using the Columbia Suicide Severity Rating Scale (C-SSRS) framework. The skill automatically analyzes patient language, assigns a clinical severity score (0-5), and provides appropriate crisis intervention based on risk level.

## Why I chose this
Regular AI assistants cannot reliably:
- Count linguistic patterns accurately (they hallucinate numbers)
- Apply consistent clinical thresholds
- Detect all variations of risk language (regex catches patterns AI misses)
- Provide deterministic scoring required for medical decisions

**The script is genuinely load-bearing because:**
- 30+ regex patterns catch language variations AI would miss
- Exact counting prevents hallucinated frequencies  
- C-SSRS severity calculation follows strict clinical protocols
- Deterministic output ensures consistency across sessions

## Skill structure
.agents/skills/suicide-ideation-markers/
├── SKILL.md              # Instructions for when/how to use the skill
├── scripts/
│   └── detect_si_markers.py   # Core detection script
└── references/           # (optional) C-SSRS documentation

## How to use

### With the therapist agent:
```bash
python3 therapist_agent.py
```
The agent automatically detects risk language and runs the skill.

### Manual testing:
```bash
python3 .agents/skills/suicide-ideation-markers/scripts/detect_si_markers.py <transcript_file>
```

## What the script does
1. **Scans text** with 30+ regex patterns across 6 C-SSRS categories:
   - Wish to die (passive ideation)
   - Suicidal ideation (active thoughts)
   - Intent to act
   - Method mentioned
   - Timeline specified
   - Means acquisition

2. **Calculates severity** (0-5) using C-SSRS decision tree:
   - 0: No ideation
   - 1: Passive wish to die
   - 2: Non-specific active ideation
   - 3: Active ideation with method
   - 4: Intent without plan
   - 5: Intent with specific plan

3. **Formats output** with:
   - Severity score
   - Matched phrases with context
   - Clinical risk flags
   - Appropriate recommendations

## Test results

### Test 1: Normal case (High severity)
**Input:** "I'm going to end it tonight. I have pills ready."

**Result:** ✅ Severity 5 detected
- Session ended immediately
- Crisis resources provided (988, Crisis Text Line)
- Appropriate for imminent risk

### Test 2: Edge case (False positive)
**Input:** "I'm writing a research paper on suicide prevention methods."

**Result:** ⚠️ Triggered detection despite academic context
- **Limitation identified:** Cannot distinguish academic discussion from personal ideation
- Demonstrates need for human clinical review
- Shows skill boundaries

### Test 3: Cautious response (Moderate severity)
**Input:** "Sometimes life isn't worth it. I don't want to die, but I don't want to be alive."

**Result:** ✅ Severity 2 detected
- Resources provided
- Session allowed to continue (not force-ended)
- Appropriate for passive ideation without plan

## What worked well
- ✅ Accurate pattern detection across severity levels
- ✅ Appropriate crisis intervention based on score
- ✅ Clear severity thresholds prevent over/under-reaction
- ✅ Automatic activation when risk language detected
- ✅ Patient never sees technical assessment (only gets help)

## Limitations
- **Context blindness:** Cannot distinguish "I want to die" (patient) from "my friend said she wants to die" (discussing others)
- **Academic false positives:** Triggers on research discussions about suicide
- **Language variations:** May miss implied ideation without explicit keywords
- **No session memory:** Cannot track changes over multiple sessions
- **Requires human review:** Tool supports, not replaces, clinical judgment

## Clinical safety notes
- This is a **screening tool only** - not diagnostic
- All positive detections require professional clinical evaluation
- Never use as sole basis for clinical decisions
- Results must be interpreted by licensed mental health professionals
- Session termination at severity ≥4 prioritizes immediate safety

## Technical requirements
- Python 3.x
- OpenAI API key (for the agent)
- Packages: `openai`, `subprocess`, `json`, `re`

## Video demonstration
[INSERT YOUR VIDEO LINK HERE AFTER RECORDING]

---

**Assignment:** CIS 4xx - Week 5: Reusable AI Skills  
**Skill name:** suicide-ideation-markers  
**Category:** Clinical language analysis with deterministic scoring
