"""
Enhanced Grok Prompt Templates for All Question Types
Provides specialized prompts for maximum accuracy and zero intervention

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

# Specialized prompt templates for each question category
GROK_QUESTION_PROMPTS = {
    'salary': """
TASK: Answer salary expectation question
CRITICAL: Return ONLY the numeric value, no currency symbols or text

USER PROFILE:
{user_info}

CURRENT MARKET DATA:
- Years of Experience: {experience_years}
- Location: {location}
- Industry Standards: Consider typical ranges for this experience level

QUESTION: {question}

RULES:
1. Return ONLY the number (e.g., "120000", "85000", "75000")
2. NO currency symbols ($, €, £), NO commas, NO text
3. If asking for hourly rate, calculate based on annual/2080
4. If asking for monthly, divide annual by 12
5. If question mentions "lakhs", format as "12.5" (with decimal)

ANSWER:""",

    'experience_numeric': """
TASK: Provide years of experience as a number

USER BACKGROUND: {user_info}
QUESTION: {question}

CRITICAL RULES:
1. Return ONLY the number (examples: "5", "2.5", "8", "10")
2. For "How long" questions about specific tech, base on user's background
3. If less than 1 year, use decimals: "0.5" for 6 months
4. Maximum should not exceed total years of experience
5. For LLMs/AI: realistic range is 0.5-3 years as of 2024

ANSWER:""",

    'visa_sponsorship': """
TASK: Answer visa/work authorization question

USER STATUS: {citizenship_status}
QUESTION: {question}

Return one of:
- "Yes" (if sponsorship needed)
- "No" (if authorized to work)

Based on citizenship status, provide appropriate answer.

ANSWER:""",

    'boolean_yesno': """
TASK: Answer Yes/No question professionally

USER CONTEXT: {user_info}
QUESTION: {question}

RULES:
1. Default to "Yes" for positive/agreeable questions
2. Consider user's actual status from profile
3. Return ONLY "Yes" or "No"
4. When in doubt, "Yes" is safer for opportunities

ANSWER:""",

    'location_relocation': """
TASK: Answer location/relocation question

USER LOCATION: {current_location}
JOB LOCATION: {job_location}
QUESTION: {question}

For relocation willingness:
- If remote job: "Yes, and I'm set up for remote work"
- If same city: "Yes, I'm already in {job_location}"
- If different city: "Yes, I'm open to relocating to {job_location}"

Keep under 100 characters.

ANSWER:""",

    'availability_start': """
TASK: Answer availability/start date question

NOTICE PERIOD: {notice_period} days
QUESTION: {question}

Standard responses:
- 0 days notice: "Immediately" or "Within 1-2 weeks"
- 15 days: "2 weeks notice" or "Within 2-3 weeks"
- 30 days: "30 days notice" or "Within 4-6 weeks"
- 60+ days: "60 days notice" or "2-3 months"

Keep it brief and professional.

ANSWER:""",

    'skills_rating': """
TASK: Rate skill level on a scale

QUESTION: {question}
USER EXPERTISE: {user_info}

Extract the scale (e.g., 1-10, 1-5) from the question.
Return ONLY the number.

Guidelines:
- Never rate yourself 10/10 (seems arrogant)
- 7-8 out of 10 shows strong competence
- 4-5 out of 5 is professional
- For core skills: 70-80% of max
- For secondary skills: 60-70% of max

ANSWER:""",

    'education_degree': """
TASK: Answer education verification question

USER EDUCATION: {education_level}
QUESTION: {question}

If asking about specific degree:
- Bachelor's: Return "Yes" if user has Bachelor's or higher
- Master's: Return "Yes" only if user has Master's or PhD
- Specific field: Match to user's actual education

Return "Yes" or "No" only.

ANSWER:""",

    'complex_screening': """
ROLE: Professional Job Applicant
TASK: Answer screening question thoughtfully

CONTEXT:
- Job Title: {job_title}
- Company: {company_name}
- Your Background: {user_info}

QUESTION: {question}

CRITICAL INSTRUCTIONS:
1. Answer as the job applicant (use "I" statements)
2. Keep response under 200 characters for text fields
3. Under 500 characters for text areas
4. Be specific and relevant to the job
5. Show enthusiasm without being excessive
6. Include a relevant achievement or metric when possible

RESPONSE:""",

    'portfolio_website': """
TASK: Provide portfolio/website URL

USER WEBSITES:
- LinkedIn: {linkedin_url}
- Portfolio: {portfolio_url}
- GitHub: {github_url}

QUESTION: {question}

Rules:
1. Return ONLY the URL, no additional text
2. For "portfolio": prefer portfolio > GitHub > LinkedIn
3. For "LinkedIn": always return LinkedIn URL
4. For "GitHub": return GitHub if available, else portfolio
5. Must be a valid URL starting with https://

ANSWER:""",

    'diversity_questions': """
TASK: Answer diversity/demographic question

USER INFO:
- Gender: {gender}
- Ethnicity: {ethnicity}
- Veteran Status: {veteran_status}
- Disability: {disability_status}

QUESTION: {question}
OPTIONS: {options}

Select the most appropriate option from the provided list.
If "Prefer not to disclose" is available and no clear match, use that.

ANSWER:""",

    'technical_assessment': """
TASK: Answer technical screening question

USER TECHNICAL BACKGROUND:
{technical_skills}

QUESTION: {question}

For Yes/No: Base on actual skills
For descriptions: Be specific but concise (under 200 chars)
For years: Return only number

Examples of good responses:
- "Yes, 5 years of React including Redux and Next.js"
- "Built 3 production Python APIs serving 1M+ requests/day"
- "Led migration from monolith to microservices architecture"

ANSWER:""",

    'motivation_why': """
TASK: Answer "Why are you interested" question

COMPANY: {company_name}
ROLE: {job_title}
COMPANY INFO: {company_description}
YOUR BACKGROUND: {user_summary}

QUESTION: {question}

Structure (keep under 300 characters):
1. Specific interest in company/role
2. How your skills align
3. What you can contribute

Use enthusiastic but professional tone.

ANSWER:""",

    'achievements_impact': """
TASK: Describe a relevant achievement

JOB REQUIREMENTS: {job_description}
YOUR EXPERIENCE: {user_info}

QUESTION: {question}

Format: [Action] + [Impact] + [Relevance]

Example: "Developed automated testing framework that reduced QA time by 60%, similar to the efficiency improvements you're seeking"

Keep under 250 characters.

ANSWER:""",

    'gap_explanation': """
TASK: Explain any gaps or transitions

QUESTION: {question}
CONTEXT: {user_info}

Provide brief, positive explanation:
- Focus on growth/learning
- Mention any relevant activities
- Keep under 150 characters
- End on forward-looking note

ANSWER:""",

    'reference_check': """
TASK: Answer reference-related question

QUESTION: {question}

Standard responses:
- "Do you have references?": "Yes"
- "Can we contact references?": "Yes, upon mutual interest"
- "How many references?": "3"
- "Reference contact?": "Available upon request"

ANSWER:""",

    'emergency_fallback': """
CRITICAL: Provide a safe, professional response

QUESTION: {question}
FIELD TYPE: {field_type}
OPTIONS: {options}

Rules:
1. For Yes/No: Default to "Yes"
2. For numeric: Return "{default_years}"
3. For select: Choose first non-placeholder option
4. For text: "I am interested in this opportunity"
5. Keep it brief and safe

ANSWER:"""
}

# Context-aware response optimization
RESPONSE_OPTIMIZATION_PROMPT = """
TASK: Optimize response for specific job and company

ORIGINAL RESPONSE: {original_response}
JOB CONTEXT:
- Company: {company_name}
- Role: {job_title}
- Key Requirements: {key_requirements}

Adjust the response to:
1. Include company-specific keywords
2. Align with role requirements
3. Maintain original meaning
4. Stay within character limits

OPTIMIZED RESPONSE:"""

# Intelligent option selection for dropdowns/radios
OPTION_SELECTION_PROMPT = """
TASK: Select best option from list

QUESTION: {question}
AVAILABLE OPTIONS:
{options_list}

USER CONTEXT: {user_info}

Rules:
1. Avoid placeholders (Select..., Choose..., --)
2. Prefer positive options (Yes, Agree, Authorized)
3. Match user's actual status when possible
4. When uncertain, pick safe middle ground
5. Return EXACT text of one option

SELECTED OPTION:"""

# Multi-attempt response refinement
RESPONSE_REFINEMENT_PROMPT = """
Previous response was invalid. Generate alternative.

QUESTION: {question}
INVALID RESPONSE: {previous_response}
REASON: {error_reason}
CONSTRAINTS: {constraints}

Provide a different valid response following all constraints.

NEW RESPONSE:"""

# Dynamic prompt builder function
def build_dynamic_prompt(question_type: str, context: dict) -> str:
    """
    Builds a dynamic prompt based on question type and context
    
    Args:
        question_type: Type of question being asked
        context: Dictionary with all relevant context
        
    Returns:
        Formatted prompt string
    """
    # Select base template
    template = GROK_QUESTION_PROMPTS.get(question_type, GROK_QUESTION_PROMPTS['emergency_fallback'])
    
    # Prepare context with safe defaults
    safe_context = {
        'question': context.get('question', ''),
        'user_info': context.get('user_info', ''),
        'experience_years': context.get('experience_years', '5'),
        'location': context.get('location', 'United States'),
        'citizenship_status': context.get('citizenship_status', 'Authorized to work'),
        'current_location': context.get('current_location', 'Remote'),
        'job_location': context.get('job_location', 'Remote'),
        'notice_period': context.get('notice_period', '0'),
        'education_level': context.get('education_level', "Bachelor's Degree"),
        'job_title': context.get('job_title', 'Position'),
        'company_name': context.get('company_name', 'the company'),
        'linkedin_url': context.get('linkedin_url', ''),
        'portfolio_url': context.get('portfolio_url', ''),
        'github_url': context.get('github_url', ''),
        'gender': context.get('gender', 'Prefer not to disclose'),
        'ethnicity': context.get('ethnicity', 'Prefer not to disclose'),
        'veteran_status': context.get('veteran_status', 'No'),
        'disability_status': context.get('disability_status', 'No'),
        'technical_skills': context.get('technical_skills', ''),
        'user_summary': context.get('user_summary', ''),
        'company_description': context.get('company_description', ''),
        'job_description': context.get('job_description', ''),
        'options': context.get('options', ''),
        'field_type': context.get('field_type', 'text'),
        'default_years': context.get('default_years', '5'),
        'options_list': '\n'.join(f"- {opt}" for opt in (context.get('options', []) or []))
    }
    
    # Format template with context
    try:
        return template.format(**safe_context)
    except KeyError as e:
        print(f"Missing context key: {e}")
        # Return emergency fallback
        return GROK_QUESTION_PROMPTS['emergency_fallback'].format(**safe_context)

# Export
__all__ = ['GROK_QUESTION_PROMPTS', 'build_dynamic_prompt', 
          'RESPONSE_OPTIMIZATION_PROMPT', 'OPTION_SELECTION_PROMPT', 
          'RESPONSE_REFINEMENT_PROMPT']