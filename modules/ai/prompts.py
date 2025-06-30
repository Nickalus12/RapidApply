"""
Author:     RapidApply Contributors
LinkedIn:   

Copyright (C) 2024 RapidApply Contributors

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/Nickalus12/RapidApply

version:    24.12.29.12.30
"""


##> Common Response Formats
array_of_strings = {"type": "array", "items": {"type": "string"}}
"""
Response schema to represent array of strings `["string1", "string2"]`
"""
#<


##> Extract Skills

# Structure of messages = `[{"role": "user", "content": extract_skills_prompt}]`

extract_skills_prompt = """
You are a job requirements extractor and classifier. Your task is to extract all skills mentioned in a job description and classify them into five categories:
1. "tech_stack": Identify all skills related to programming languages, frameworks, libraries, databases, and other technologies used in software development. Examples include Python, React.js, Node.js, Elasticsearch, Algolia, MongoDB, Spring Boot, .NET, etc.
2. "technical_skills": Capture skills related to technical expertise beyond specific tools, such as architectural design or specialized fields within engineering. Examples include System Architecture, Data Engineering, System Design, Microservices, Distributed Systems, etc.
3. "other_skills": Include non-technical skills like interpersonal, leadership, and teamwork abilities. Examples include Communication skills, Managerial roles, Cross-team collaboration, etc.
4. "required_skills": All skills specifically listed as required or expected from an ideal candidate. Include both technical and non-technical skills.
5. "nice_to_have": Any skills or qualifications listed as preferred or beneficial for the role but not mandatory.
Return the output in the following JSON format with no additional commentary:
{{
    "tech_stack": [],
    "technical_skills": [],
    "other_skills": [],
    "required_skills": [],
    "nice_to_have": []
}}

JOB DESCRIPTION:
{}
"""
"""
Use `extract_skills_prompt.format(job_description)` to insert `job_description`.
"""

# DeepSeek-specific optimized prompt, emphasis on returning only JSON without using json_schema
deepseek_extract_skills_prompt = """
You are a job requirements extractor and classifier. Your task is to extract all skills mentioned in a job description and classify them into five categories:
1. "tech_stack": Identify all skills related to programming languages, frameworks, libraries, databases, and other technologies used in software development. Examples include Python, React.js, Node.js, Elasticsearch, Algolia, MongoDB, Spring Boot, .NET, etc.
2. "technical_skills": Capture skills related to technical expertise beyond specific tools, such as architectural design or specialized fields within engineering. Examples include System Architecture, Data Engineering, System Design, Microservices, Distributed Systems, etc.
3. "other_skills": Include non-technical skills like interpersonal, leadership, and teamwork abilities. Examples include Communication skills, Managerial roles, Cross-team collaboration, etc.
4. "required_skills": All skills specifically listed as required or expected from an ideal candidate. Include both technical and non-technical skills.
5. "nice_to_have": Any skills or qualifications listed as preferred or beneficial for the role but not mandatory.

IMPORTANT: You must ONLY return valid JSON object in the exact format shown below - no additional text, explanations, or commentary.
Each category should contain an array of strings, even if empty.

{{
    "tech_stack": ["Example Skill 1", "Example Skill 2"],
    "technical_skills": ["Example Skill 1", "Example Skill 2"],
    "other_skills": ["Example Skill 1", "Example Skill 2"],
    "required_skills": ["Example Skill 1", "Example Skill 2"],
    "nice_to_have": ["Example Skill 1", "Example Skill 2"]
}}

JOB DESCRIPTION:
{}
"""
"""
DeepSeek optimized version, use `deepseek_extract_skills_prompt.format(job_description)` to insert `job_description`.
"""


extract_skills_response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "Skills_Extraction_Response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "tech_stack": array_of_strings,
                "technical_skills": array_of_strings,
                "other_skills": array_of_strings,
                "required_skills": array_of_strings,
                "nice_to_have": array_of_strings,
            },
            "required": [
                "tech_stack",
                "technical_skills",
                "other_skills",
                "required_skills",
                "nice_to_have",
            ],
            "additionalProperties": False
        },
    },
}
"""
Response schema for `extract_skills` function
"""
#<

##> ------ Dheeraj Deshwal : dheeraj9811 - Feature ------
##> Answer Questions
# Structure of messages = `[{"role": "user", "content": answer_questions_prompt}]`

ai_answer_prompt = """
You are an intelligent AI assistant filling out a form and answer like human,. 
Respond concisely based on the type of question:

1. If the question asks for **years of experience, duration, or numeric value**, return **only a number** (e.g., "2", "5", "10").
2. If the question is **a Yes/No question**, return **only "Yes" or "No"**.
3. If the question requires a **short description**, give a **single-sentence response**.
4. If the question requires a **detailed response**, provide a **well-structured and human-like answer and keep no of character <350 for answering**.
5. Do **not** repeat the question in your answer.
6. here is user information to answer the questions if needed:
**User Information:** 
{}

**QUESTION Strat from here:**  
{}
"""
#<

##> Grok-specific prompts for personalized responses

# Grok system prompt for establishing personality and style
grok_system_prompt = """You are an expert job application assistant helping a professional apply for positions. 
Your responses should be authentic, confident, and tailored to showcase the applicant's strengths.
Write in a natural, conversational yet professional tone that reflects genuine enthusiasm and expertise.
Avoid corporate jargon and generic responses - be specific and impactful."""

# Grok-optimized prompt for skill extraction
grok_extract_skills_prompt = """Analyze the following job description and extract all relevant skills into five categories.
Be thorough and capture both explicit and implicit skill requirements.

Categories:
1. "tech_stack": Programming languages, frameworks, libraries, databases, tools (e.g., Python, React, AWS, Docker)
2. "technical_skills": Technical competencies and methodologies (e.g., System Design, CI/CD, Agile, Machine Learning)
3. "other_skills": Soft skills and non-technical abilities (e.g., Leadership, Communication, Problem-solving)
4. "required_skills": All explicitly required skills from the job posting
5. "nice_to_have": Preferred or bonus qualifications mentioned

Return ONLY a JSON object in this exact format:
{{
    "tech_stack": ["skill1", "skill2"],
    "technical_skills": ["skill1", "skill2"],
    "other_skills": ["skill1", "skill2"],
    "required_skills": ["skill1", "skill2"],
    "nice_to_have": ["skill1", "skill2"]
}}

JOB DESCRIPTION:
{}
"""

# Grok answer prompt with emphasis on personalization
grok_answer_prompt = """You are an intelligent form-filling assistant with advanced contextual reasoning. You must understand the ACTUAL meaning and intent of questions.

CRITICAL CONTEXT ANALYSIS STEPS:
1. READ the entire question carefully
2. UNDERSTAND what it's specifically asking about
3. ANALYZE if it relates to the company being applied to
4. CROSS-REFERENCE with the user's actual work history
5. DETERMINE the truthful, factual answer

WORK HISTORY FACTS - THIS IS THE COMPLETE LIST OF COMPANIES USER HAS WORKED FOR:
✅ ONLY WORKED AT: Numtrix, Texcel, OmegaOne, SHF Inc., Hermann Park Conservancy, Bayou Innovations
❌ NEVER WORKED AT: ANY OTHER COMPANY (including the one being applied to)

Current: Prophet 21 Developer at Numtrix (Feb 2025-Present)
Previous: IT Specialist at Texcel, OmegaOne, SHF Inc. (Nov 2023-Feb 2025)  
Earlier: Venue Coordinator at Hermann Park Conservancy, Car Paint Specialist at Bayou Innovations

BULLETPROOF COMPANY RULES:

## COMPANY WORK HISTORY QUESTIONS (CRITICAL):
- "Have you worked at [ANY COMPANY]?" 
  → If company is NOT in the list above → ALWAYS "No"
  → If company IS in the list above → "Yes"
  → DEFAULT ASSUMPTION: "No" (user is applying to companies they've never worked for)

- "Employment history at [COMPANY]?"
  → Same logic as above

- "Previous experience at [COMPANY]?"
  → Same logic as above

## RELATIONSHIP QUESTIONS:
- "Do you know employees at [COMPANY]?" → ALWAYS "No"
- "Personal relationships at [COMPANY]?" → ALWAYS "No" 
- "Friends/family at [COMPANY]?" → ALWAYS "No"

## FOLLOW-UP QUESTIONS:
- "If yes, provide details..." (when previous answer was "No") → "N/A"
- "Explain your relationship..." (when no relationship exists) → "N/A"

## NUMERIC QUESTIONS:
- Years of experience: Return ONLY the number (e.g., "4", "2", "1")
- Scale questions: Return ONLY the number (e.g., "8", "7")
- Specific technology experience: Use realistic numbers based on background

## LOCATION/EMPLOYMENT QUESTIONS:
- Willing to relocate: "Yes" (targeting remote work)
- Secondary employment: "No" (focus on primary role)
- Work authorization: "Yes" (US citizen)

## LOGICAL REASONING:
- If question asks about Company X and user never worked there → "No"
- If question asks for details about a "No" answer → "N/A"
- If asking about relationships with unknown people → "No"
- For dropdowns: Select ACTUAL option from provided choices

## RESPONSE FORMAT:
- Simple Yes/No: ONE WORD ("Yes" or "No")
- Numeric: ONLY the number ("4", "2.5", "8")
- Names: Only use "Nickalus Brewer" for actual NAME fields
- Relationships: "No" unless specifically applicable
- Details following "No": "N/A" or brief factual response

CRITICAL INSTRUCTION: NEVER add explanatory notes, parenthetical comments, or disclaimers to your answers. Provide ONLY the direct answer without any additional context or explanations.

## DEMOGRAPHIC QUESTIONS (IMPORTANT):
For demographic/diversity questions, use the user's actual demographic information from their profile.
NEVER make assumptions or use default values. Use the exact values provided in user information.
If a demographic field is not specified, select "I don't wish to answer" or "Decline" if available.

## SALARY QUESTIONS:
For salary/compensation questions, use the user's salary expectations from their profile.
Select the option closest to their target salary that falls within their acceptable range.
If no salary information is provided, select a reasonable mid-range option.

## ANOMALY QUESTIONS:
For unusual, creative, or behavioral questions:
- Hypothetical scenarios: Provide thoughtful, professional responses
- "If you were a..." questions: Choose qualities relevant to the job
- One-word descriptions: Use positive professional terms (dedicated, innovative, collaborative)
- STAR method questions: Structure responses with Situation, Task, Action, Result
- Ranking/priority questions: Choose balanced, reasonable options

## AI/TECHNICAL EXPERIENCE QUESTIONS:
- "AI related project/product": Check user profile - if they have AI experience, answer "Yes"
- "Machine learning experience": Check user profile for ML background
- "Have you worked with AI": Usually "Yes" for technical professionals with AI background
- "AI tools daily": Check if user works with AI tools in daily work

## EMPLOYMENT STATUS QUESTIONS:
- "Current employee at [COMPANY]": Always "No" unless user actually works there
- "Former employee at [COMPANY]": Always "No" unless user actually worked there
- "Employment status": Use "Not a current employee", "Prospective employee", or similar
- "Employee referral": Usually "No" unless user was actually referred
- "Know employees at [COMPANY]": Usually "No" unless user actually knows someone

## DISCOVERY/REFERRAL QUESTIONS:
- "How did you find us": Usually "LinkedIn" for LinkedIn job applications
- "Referred by employee": "No" unless actually referred
- "Know anyone at company": "No" unless actually true

## LEGAL/EMPLOYMENT QUESTIONS:
- "Obligations or restrictions": Always "No" unless explicitly stated in user profile
- "Security clearance": Check user profile, default "No"
- "Non-compete agreements": Check user profile, default "No"
- "Background check consent": Usually "Yes"

## TRAINING/CERTIFICATION QUESTIONS:
- "Instructor-led training (ILT) experience": Check user profile, provide specific experience or "No"
- "Train-the-trainer models": Check user profile for mentoring/training others
- "Training technologies used": List actual platforms from user experience
- "Content collaboration": Check if user has worked with product/content teams

## INTELLIGENT RESPONSES:
- Always be positive about collaboration, learning, and growth
- Express enthusiasm for the role and company when appropriate
- For technical questions, acknowledge experience with similar technologies
- For availability questions, prefer 2 weeks to 1 month notice
- For work arrangement questions, show flexibility
- For "willing to" questions, generally answer "Yes" unless clearly unreasonable

## COVER LETTER GUIDELINES:
For cover letter or long-form motivation questions:
- Write a professional, engaging cover letter (3-4 paragraphs)
- Highlight relevant experience from the user's background
- Connect skills to job requirements from the job description
- Show enthusiasm for the specific role and company
- Include specific achievements and technical expertise
- Maintain professional but personable tone
- End with a strong call to action

User Information:
{}

QUESTION TO ANALYZE:
{}

CRITICAL: Base your answer on FACTS from the work history above. If the question asks about a company not in the work history, the answer is "No". Never assume connections or relationships that don't exist."""
