#!/usr/bin/env python3
"""
Suicide Ideation Language Marker Detector
Based on Columbia Suicide Severity Rating Scale (C-SSRS) linguistic patterns
"""

import re
import sys
import json
from collections import defaultdict

# C-SSRS-based linguistic marker patterns
MARKERS = {
    'wish_to_die': [
        r'\b(wish|wished|wishing)\s+(I|i)\s+(was|were|would be)\s+dead\b',
        r'\b(better off|everyone would be better)\s+.*\s+(dead|without me)\b',
        r'\b(wish|hope)\s+(I|i)\s+(wouldn\'?t|would not|didn\'?t|did not)\s+wake up\b',
        r'\b(no|not any)\s+reason to (live|be alive|keep living|go on)\b',
        r'\b(don\'?t|do not)\s+want to (live|be alive|exist|be here)\s+anymore\b',
        r'\b(life|living)\s+(isn\'?t|is not|\'?s not)\s+worth\b',
    ],
    
    'suicidal_ideation': [
        r'\b(thought about|think about|thinking about|considered)\s+(killing|ending)\s+(myself|my life|it all)\b',
        r'\b(thought about|think about|thinking about)\s+suicide\b',
        r'\b(end|ending)\s+(it all|everything|my life)\b',
        r'\b(kill|killing)\s+myself\b',
        r'\btake my (own )?life\b',
        r'\b(want to|going to|plan to)\s+die\b',
    ],
    
    'intent': [
        r'\b(I\'?m going to|I will|I plan to)\s+(kill myself|end it|do it)\b',
        r'\b(decided|made up my mind)\s+to\s+(die|kill myself|end it)\b',
        r'\b(can\'?t|cannot)\s+stop\s+(myself|these thoughts)\b',
        r'\b(have to|need to)\s+(end it|die|kill myself)\b',
        r'\b(will|going to)\s+kill myself\b',
    ],
    
    'plan_method': [
        r'\b(pills|overdose|medication)\b',
        r'\b(gun|firearm|shoot|shot)\b',
        r'\b(hang|hanging|rope|noose)\b',
        r'\b(jump|jumping)\s+(off|from)\b',
        r'\b(cut|cutting|blade|knife)\b',
        r'\b(drown|drowning)\b',
        r'\bcarbon monoxide\b',
    ],
    
    'plan_timing': [
        r'\b(tonight|today|tomorrow|this week|soon)\b.*\b(do it|end it|kill myself)\b',
        r'\b(when|after|once)\s+.{1,30}\s+(then )?I\'?ll\s+(do it|end it)\b',
        r'\b(already|have)\s+(planned|decided when)\b',
    ],
    
    'means_acquisition': [
        r'\b(got|obtained|have|bought|purchased)\s+(a )?(gun|pills|rope|knife)\b',
        r'\b(know where|found out where|figured out how)\b',
        r'\b(have access to|can get)\b.*\b(pills|gun|knife)\b',
        r'\b(saving|saved|collecting)\s+(pills|medication)\b',
    ]
}

def detect_markers(text):
    """Detect suicide ideation markers in text"""
    results = defaultdict(list)
    
    text_lower = text.lower()
    
    for category, patterns in MARKERS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                
                results[category].append({
                    'matched_text': match.group(),
                    'context': context
                })
    
    return results

def calculate_severity(results):
    """Calculate C-SSRS severity score (0-5)"""
    
    if not any(results.values()):
        return 0
    
    if results['intent'] and (results['plan_method'] or results['plan_timing'] or results['means_acquisition']):
        return 5
    
    if results['intent']:
        return 4
    
    if results['suicidal_ideation'] and results['plan_method']:
        return 3
    
    if results['suicidal_ideation']:
        return 2
    
    if results['wish_to_die']:
        return 1
    
    return 0

def format_output(results, severity):
    """Format results as clinical report"""
    
    severity_labels = {
        0: "No Ideation Detected",
        1: "Wish to Die (Passive)",
        2: "Non-Specific Active Suicidal Thoughts",
        3: "Active Ideation with Method",
        4: "Suicidal Intent Without Plan",
        5: "Suicidal Intent With Specific Plan"
    }
    
    output = []
    output.append("=" * 50)
    output.append("SUICIDE IDEATION RISK ASSESSMENT")
    output.append("=" * 50)
    output.append("")
    output.append(f"Severity Score: {severity}/5 ({severity_labels[severity]})")
    output.append("")
    
    if severity == 0:
        output.append("No suicide ideation markers detected in text.")
        output.append("")
        output.append("=" * 50)
        return "\n".join(output)
    
    output.append("DETECTED MARKERS:")
    output.append("")
    
    category_labels = {
        'wish_to_die': 'Wish to Die',
        'suicidal_ideation': 'Suicidal Ideation',
        'intent': 'Intent to Act',
        'plan_method': 'Method Mentioned',
        'plan_timing': 'Timing Specified',
        'means_acquisition': 'Means Acquisition'
    }
    
    for category, label in category_labels.items():
        if results[category]:
            output.append(f"- {label}: {len(results[category])} instance(s)")
            for item in results[category][:3]:
                output.append(f'  • "...{item["context"]}..."')
            output.append("")
    
    output.append("RISK FLAGS:")
    if severity >= 3:
        output.append("⚠️  ACTIVE SUICIDAL IDEATION DETECTED")
    if results['plan_method']:
        output.append("⚠️  SPECIFIC METHOD MENTIONED")
    if results['intent']:
        output.append("⚠️  INTENT TO ACT EXPRESSED")
    if results['plan_timing']:
        output.append("⚠️  TIMELINE SPECIFIED")
    if results['means_acquisition']:
        output.append("⚠️  MEANS ACQUISITION INDICATED")
    
    output.append("")
    output.append("RECOMMENDATION:")
    if severity >= 3:
        output.append("🚨 IMMEDIATE clinical evaluation required.")
        output.append("   Consider safety planning and emergency protocols.")
    elif severity >= 1:
        output.append("⚠️  Clinical follow-up recommended within 24-48 hours.")
    
    output.append("")
    output.append("=" * 50)
    output.append("Note: This is a screening tool. Clinical judgment required.")
    output.append("=" * 50)
    
    return "\n".join(output)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    results = detect_markers(text)
    severity = calculate_severity(results)
    report = format_output(results, severity)
    print(report)
    
    json_output = {
        'severity': severity,
        'severity_label': ['No Ideation', 'Wish to Die', 'Non-Specific Ideation', 
                          'Active Ideation with Method', 'Intent Without Plan', 
                          'Intent With Plan'][severity],
        'markers': {k: len(v) for k, v in results.items()},
        'total_markers': sum(len(v) for v in results.values())
    }
    
    print("\nJSON OUTPUT:")
    print(json.dumps(json_output, indent=2))

if __name__ == "__main__":
    main()
