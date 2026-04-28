---
name: suicide-ideation-markers
description: Detects and scores suicide ideation language patterns based on Columbia Suicide Severity Rating Scale (C-SSRS) linguistic markers. Use when analyzing therapy transcripts, clinical notes, or patient communications for suicide risk assessment. Produces severity scores (0-5) and flags high-risk phrases.
---

# Suicide Ideation Language Markers

## When to use this skill
Use this skill when:
- Analyzing therapy session transcripts for suicide risk
- Reviewing clinical notes or patient communications
- Monitoring language changes over time in high-risk patients
- The user asks to assess, detect, or track suicide-related language

## When NOT to use this skill
Do not use this skill for:
- Real-time crisis intervention (this is retrospective analysis only)
- Non-clinical text analysis
- General sentiment analysis
- Creative writing or fictional content

## Expected inputs
- Therapy session transcript (text file or pasted text)
- Patient communication logs
- Clinical notes containing patient statements

## How this skill works

### Step 1: Receive the text to analyze
Accept the transcript or text from the user.

### Step 2: Run the detection script
Execute: `python scripts/detect_si_markers.py <input_file>`

Or pipe text: `echo "transcript text" | python scripts/detect_si_markers.py`

### Step 3: Script analyzes six categories
1. **Wish to Die** - passive death wishes
2. **Suicidal Ideation** - active thoughts about suicide
3. **Intent** - statements indicating intention to act
4. **Plan Method** - specific methods mentioned
5. **Plan Timing** - when they plan to act
6. **Means Acquisition** - obtaining means to act

### Step 4: Severity scoring (0-5)
- **0:** No ideation detected
- **1:** Wish to be dead (passive)
- **2:** Non-specific active suicidal thoughts
- **3:** Active ideation with method mentioned
- **4:** Suicidal intent without specific plan
- **5:** Suicidal intent WITH specific plan

### Step 5: Present the report
Show severity score, detected phrases, risk flags, and clinical recommendations.

## Important limitations
- **Screening tool only** - not diagnostic
- **Requires clinical judgment** - never use alone for decisions
- **Context matters** - script cannot understand full clinical picture
- **Always recommend professional evaluation** for any positive detection

## Safety protocols
- Severity ≥3 requires immediate clinical review
- Any plan/means detection = high-priority flag
- Results must be interpreted by licensed professionals only

## Expected output format
```
========================================
SUICIDE IDEATION RISK ASSESSMENT
========================================

Severity Score: 3/5 (Active Ideation with Method)

DETECTED MARKERS:

- Suicidal Ideation: 2 instance(s)
  • "...thought about ending it..."
  • "...no reason to keep going..."

- Method Mentioned: 1 instance(s)
  • [context shown]

RISK FLAGS:
⚠️  ACTIVE SUICIDAL IDEATION DETECTED
⚠️  SPECIFIC METHOD MENTIONED

RECOMMENDATION:
🚨 IMMEDIATE clinical evaluation required.

========================================
```
