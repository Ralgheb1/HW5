#!/usr/bin/env python3
"""
Therapist AI Agent with Suicide Ideation Detection Skill
"""

import openai
import subprocess
import sys
import json
import os

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
conversation_history = []

def run_suicide_detection(text):
    script_path = ".agents/skills/suicide-ideation-markers/scripts/detect_si_markers.py"
    try:
        result = subprocess.run(["python3", script_path], input=text, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    
    risk_keywords = ['suicide', 'kill myself', 'end it all', 'ending it', 'no reason to live', 
                     'better off dead', 'wish i was dead', 'want to die', 'end my life', 
                     'take my life', 'ending my life', 'no reason to keep going', 'end it']
    
    has_risk_language = any(keyword in user_message.lower() for keyword in risk_keywords)
    
    system_prompt = """You are an empathetic therapist AI. Be warm, caring, and supportive."""
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}] + conversation_history
    )
    
    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    if has_risk_language:
        patient_text = "\n".join([msg["content"] for msg in conversation_history if msg["role"] == "user"])
        analysis = run_suicide_detection(patient_text)
        try:
            # Find the JSON block (multi-line)
            if "JSON OUTPUT:" in analysis:
                json_start = analysis.find('{', analysis.find('JSON OUTPUT:'))
                # Find matching closing brace by counting braces
                brace_count = 0
                json_end = json_start
                for i in range(json_start, len(analysis)):
                    if analysis[i] == '{':
                        brace_count += 1
                    elif analysis[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                json_str = analysis[json_start:json_end]
                json_data = json.loads(json_str)
                severity = json_data.get('severity', 0)
            else:
                severity = 0
        except Exception as e:
            print(f"[DEBUG: Parse error - {e}]")
            severity = 0

        print(f"\nTherapist: I hear how much pain you're in right now.\n")
        
        if severity >= 4:
            print("=" * 60)
            print("🚨 I'm very concerned about your immediate safety.")
            print("=" * 60)
            print("\nYou need support right now that I cannot provide through chat.")
            print("Please reach out for help IMMEDIATELY:\n")
            print("📞 CALL 988 - Suicide & Crisis Lifeline")
            print("   Available 24/7, free, confidential\n")
            print("📱 TEXT 'HELLO' to 741741 - Crisis Text Line\n")
            print("🏥 Go to your nearest Emergency Room\n")
            print("🚨 Call 911 - If you're in immediate danger\n")
            print("=" * 60)
            print("\nYour life matters. Please get help right now.")
            print("I'm ending our session so you can connect with crisis support.")
            print("=" * 60 + "\n")
            sys.exit(0)
            
        elif severity >= 2:
            print("=" * 60)
            print("⚠️  What you're sharing is very serious.")
            print("=" * 60)
            print("\nThese resources are available RIGHT NOW:\n")
            print("📞 988 - Suicide & Crisis Lifeline (24/7)")
            print("📱 Text 'HELLO' to 741741 - Crisis Text Line\n")
            print("Please contact them now rather than continuing our chat.")
            print("=" * 60 + "\n")
            
        elif severity >= 1:
            print("I want to make sure you have support.\n")
            print("📞 988 - Suicide & Crisis Lifeline (24/7)")
            print("📱 Text 'HELLO' to 741741 - Crisis Text Line\n")
        
        return None
    
    return assistant_message

def main():
    print("=" * 60)
    print("THERAPIST AI AGENT")
    print("With Automatic Suicide Risk Detection")
    print("=" * 60)
    print("\nTherapist: Hello, I'm here to listen. How are you feeling today?")
    print("\nType 'quit' to end session")
    print("=" * 60)
    print()
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("\nTherapist: Thank you for sharing today. Take care.")
            break
        
        response = chat(user_input)
        if response:
            print(f"\nTherapist: {response}\n")

if __name__ == "__main__":
    main()
