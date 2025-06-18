"""
Test script for Smart Resume Selection feature
Tests the resume selector independently
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.resumes.smart_selector import SmartResumeSelector
from modules.ai.grokConnections import grok_create_client
from config.secrets import use_AI, ai_provider, use_grok_for_openai

def test_smart_resume_selection():
    """Test the smart resume selector"""
    print("=== Testing Smart Resume Selection ===\n")
    
    # Initialize AI client
    ai_client = None
    if use_AI and (ai_provider.lower() == "grok" or use_grok_for_openai):
        print("Initializing Grok AI client...")
        ai_client = grok_create_client()
        if ai_client:
            print("✓ Grok client initialized successfully\n")
        else:
            print("✗ Failed to initialize Grok client\n")
            return
    else:
        print("AI not configured or not using Grok. Testing without AI...\n")
    
    # Initialize resume selector
    print("Initializing Smart Resume Selector...")
    selector = SmartResumeSelector(ai_client=ai_client)
    print("✓ Resume selector initialized\n")
    
    # Load available resumes
    print("Loading available resumes...")
    resumes = selector.load_available_resumes()
    print(f"✓ Found {len(resumes)} resumes:\n")
    for name, data in resumes.items():
        print(f"  - {name} ({data['category']})")
    print()
    
    # Test cases
    test_jobs = [
        {
            'title': 'Senior Backend Engineer',
            'company': 'Tech Corp',
            'description': 'We are looking for a Senior Backend Engineer with expertise in Python, Django, PostgreSQL, and AWS. You will be building scalable microservices and APIs.',
            'skills': ['Python', 'Django', 'PostgreSQL', 'AWS', 'Docker']
        },
        {
            'title': 'Frontend Developer',
            'company': 'StartupXYZ',
            'description': 'Seeking a Frontend Developer proficient in React, TypeScript, and modern CSS. Experience with Next.js is a plus.',
            'skills': ['React', 'TypeScript', 'CSS', 'JavaScript', 'Next.js']
        },
        {
            'title': 'Engineering Manager',
            'company': 'Enterprise Inc',
            'description': 'Looking for an Engineering Manager to lead a team of 10 developers. Must have strong technical background and leadership experience.',
            'skills': ['Leadership', 'Agile', 'Architecture', 'Team Management']
        }
    ]
    
    # Test selection for each job
    for i, job in enumerate(test_jobs, 1):
        print(f"\n--- Test Case {i}: {job['title']} at {job['company']} ---")
        print(f"Required Skills: {', '.join(job['skills'])}")
        
        try:
            resume_path, selection_info = selector.select_best_resume(
                job_description=job['description'],
                company_name=job['company'],
                job_title=job['title'],
                required_skills=job['skills']
            )
            
            print(f"\n✓ Selected Resume: {selection_info['selected_resume']}")
            print(f"  Confidence: {selection_info['confidence']:.2%}")
            print(f"  Method: {selection_info['method']}")
            print(f"  Reason: {selection_info['reason']}")
            print(f"  Path: {resume_path}")
            
        except Exception as e:
            print(f"\n✗ Selection failed: {str(e)}")
    
    # Display statistics
    print("\n\n=== Selection Statistics ===")
    stats = selector.get_selection_stats()
    if stats:
        print(f"Total Selections: {stats.get('total_selections', 0)}")
        print(f"Average Confidence: {stats.get('average_confidence', 0):.2%}")
        print("\nResume Usage:")
        for resume, count in stats.get('resume_usage', {}).items():
            print(f"  - {resume}: {count} times")
        print("\nMethod Distribution:")
        for method, count in stats.get('method_distribution', {}).items():
            print(f"  - {method}: {count} times")

if __name__ == "__main__":
    test_smart_resume_selection()
    print("\n\nTest completed!")