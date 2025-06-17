"""
Test script for Grok API integration
"""

import sys
sys.path.append('.')

from config.secrets import grok_api_key, grok_model, grok_personal_style, use_grok_for_openai, ai_provider
from modules.ai.grokConnections import grok_create_client, grok_extract_skills, grok_answer_question
from modules.ai.openaiConnections import ai_create_openai_client, ai_extract_skills, ai_answer_question

def test_grok_integration():
    print("Testing Grok API Integration...")
    print(f"Using model: {grok_model}")
    print("-" * 50)
    
    # Create client
    print("1. Creating Grok client...")
    client = grok_create_client()
    if not client:
        print("Failed to create client. Please check your API key and configuration.")
        return
    
    print("✓ Client created successfully!")
    print("-" * 50)
    
    # Test skill extraction
    print("\n2. Testing skill extraction...")
    job_description = """
    We are looking for a Senior Software Engineer with expertise in Python, React, and AWS.
    The ideal candidate should have experience with microservices architecture, CI/CD pipelines,
    and strong problem-solving skills. Experience with machine learning is a plus.
    Must have excellent communication skills and ability to work in a team.
    """
    
    skills = grok_extract_skills(client, job_description, stream=False)
    print("Extracted skills:")
    print(skills)
    print("-" * 50)
    
    # Test question answering
    print("\n3. Testing question answering...")
    
    # Test different question types
    questions = [
        ("How many years of Python experience do you have?", "text"),
        ("Why are you interested in this position?", "textarea"),
        ("Are you authorized to work in the United States?", "text"),
        ("Describe a challenging technical problem you solved.", "textarea")
    ]
    
    user_info = """
    Name: Test User
    Experience: 5 years in software development
    Skills: Python, JavaScript, React, AWS, Docker
    Education: BS in Computer Science
    Current Role: Software Engineer at TechCorp
    """
    
    for question, q_type in questions:
        print(f"\nQuestion: {question}")
        print(f"Type: {q_type}")
        answer = grok_answer_question(
            client, 
            question, 
            question_type=q_type,
            user_information_all=user_info,
            personal_style=grok_personal_style,
            stream=False
        )
        print(f"Answer: {answer}")
    
    print("\n" + "-" * 50)
    print("✓ All tests completed successfully!")
    
def test_grok_redirect():
    print("\n" + "=" * 50)
    print("Testing Grok Redirect Feature...")
    print(f"use_grok_for_openai: {use_grok_for_openai}")
    print(f"ai_provider: {ai_provider}")
    print("-" * 50)
    
    if use_grok_for_openai:
        print("\n1. Testing OpenAI client creation with Grok redirect...")
        client = ai_create_openai_client()
        if not client:
            print("Failed to create client.")
            return
        print("✓ Client created successfully (should be using Grok)")
        
        print("\n2. Testing OpenAI skill extraction with Grok redirect...")
        job_desc = "Looking for a Python developer with 5 years experience"
        skills = ai_extract_skills(client, job_desc, stream=False)
        print(f"Skills extracted: {skills}")
        
        print("\n3. Testing OpenAI question answering with Grok redirect...")
        answer = ai_answer_question(
            client,
            "What makes you a good fit for this role?",
            question_type="text",
            stream=False
        )
        print(f"Answer: {answer}")
        
        print("\n✓ Grok redirect tests completed!")
    else:
        print("use_grok_for_openai is False - redirect not active")

if __name__ == "__main__":
    test_grok_integration()
    test_grok_redirect()