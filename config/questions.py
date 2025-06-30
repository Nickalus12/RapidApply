'''
Author:     RapidApply Contributors
LinkedIn:   

Copyright (C) 2024 RapidApply Contributors

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/Nickalus12/RapidApply

version:    24.12.29.12.30
'''


###################################################### APPLICATION INPUTS ######################################################


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative path of your default resume to be uploaded. If file in not found, will continue using your previously uploaded resume in LinkedIn.
default_resume_path = "all resumes/default/resume.pdf"      # (In Development)

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience? 
years_of_experience = "4"          # A number in quotes Eg: "0","1","2","3","4", etc.

# Do you need visa sponsorship now or in future?
require_visa = "No"               # "Yes" or "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = "https://github.com/Nickalus12"                        # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = "https://www.linkedin.com/in/nickalus-brewer-0a5535137/"       # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "U.S. Citizen/Permanent Resident"



## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (American and European), What is your expected CTC (South Asian and others)?, only enter in numbers as some companies only allow numbers,
desired_salary = 120000          # 80000, 90000, 100000 or 120000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your expected CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
And if asked in months, then it will divide by 12 and answer. Examples:
* 2400000 will be answered as "200000"
* 850000 will be answered as "70833"
'''

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = 800000            # 800000, 900000, 1000000 or 1200000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
'''

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg: 
# currency = "INR"                 # "USD", "INR", "EUR", etc.

# What is your notice period in days?
notice_period = 0                   # Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
'''
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months), 
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
'''

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Information Technology Manager | ERP Systems Expert | Technology Leadership" # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
Experienced Information Technology professional with 4 years of hands-on experience in ERP systems management, development, and implementation. Proven track record of leading technology initiatives that drive business efficiency and operational excellence.

My expertise spans across technology leadership, team management, and strategic implementation of enterprise software solutions. I specialize in bridging the gap between technical capabilities and business objectives, ensuring technology investments deliver measurable results.

Core competencies include ERP systems management (Prophet 21), full-stack development, database administration, and cross-functional team leadership. I excel at managing complex IT projects, vendor relationships, and technology transformations that enhance organizational productivity.

Currently seeking IT Management opportunities where I can leverage my technical background and leadership skills to drive technology strategy and innovation in a remote-first environment.
"""

'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Dear Hiring Manager,

I am writing to express my strong interest in this position. With 4 years of experience in information technology and a proven track record of driving successful implementations and optimizations, I am confident I would be a valuable addition to your team.

In my current role as Prophet 21 Developer at Numtrix, I have successfully:
• Led ERP system implementations and customizations that improved business efficiency
• Developed automated solutions using Python, SQL, and APIs that streamlined operations
• Managed complex technical projects from inception to completion
• Collaborated with cross-functional teams to deliver innovative technology solutions

My technical expertise spans across multiple areas including:
• Programming & Development: Python, JavaScript, SQL, C#/.NET
• Automation & Integration: Expert-level experience with Zapier, Make (Integromat), and workflow automation
• Cloud & Infrastructure: AWS, Azure, database administration
• AI & Modern Technologies: Daily work with AI tools and API integrations

What sets me apart is my ability to combine deep technical knowledge with strong business acumen. I excel at translating complex technical concepts into actionable business solutions, managing stakeholder relationships, and leading teams through digital transformation initiatives.

I am particularly drawn to opportunities that allow me to leverage emerging technologies like AI and automation to drive meaningful business impact. My passion for continuous learning and innovation, combined with my collaborative leadership style, makes me well-suited for dynamic, growth-oriented environments.

I would welcome the opportunity to discuss how my experience and enthusiasm can contribute to your team's success. Thank you for your consideration.

Best regards,
Nickalus Brewer
"""
##> ------ Dheeraj Deshwal : dheeraj9811 - Feature ------

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc. 
user_information_all ="""
Name: Nickalus Peter Brewer
Location: Humble, Texas, United States (Open to Remote Opportunities Nationwide)
Email: NickalusBrewer@gmail.com
Phone: 9858690859
Years of Experience: 4 years
Career Focus: Information Technology Management

Current Position: Prophet 21 Developer at Numtrix (Ready for Management Transition)
Education: Bachelor's Degree in Computer Science from Full Sail University

MANAGEMENT & LEADERSHIP SKILLS:
Technology Leadership:
- IT Strategy and Planning
- Technology Team Leadership and Mentoring
- Cross-functional Project Management
- Vendor Management and Technology Partnerships
- Budget Planning and Resource Allocation
- Technology Risk Assessment and Mitigation

Business Acumen:
- Business Process Optimization
- Digital Transformation Initiatives
- Stakeholder Management
- Requirements Gathering and Analysis
- Change Management
- Technical Training and Documentation

TECHNICAL EXPERTISE:
ERP Systems Management:
- Prophet 21 (Expert level - 4 years)
- ERP Implementation and Customization
- Business Process Automation
- System Integration and Data Migration
- Enterprise Software Architecture

Programming & Development:
- C# / .NET Framework
- SQL Server (Database Administration)
- JavaScript, Python, HTML/CSS
- API Development and Integration
- Web Services (REST/SOAP)

Infrastructure & Tools:
- Microsoft SQL Server Administration
- Visual Studio, Git/GitHub
- Crystal Reports, SSRS
- IIS (Internet Information Services)
- Cloud Technologies and Migration Planning

PROJECT MANAGEMENT:
- IT Project Planning and Execution
- Resource Management and Team Coordination
- Timeline Management and Milestone Tracking
- Quality Assurance and Testing Coordination
- Client Relationship Management
- Post-Implementation Support and Optimization

INDUSTRY SPECIALIZATION:
- Distribution and Supply Chain Technology
- Manufacturing Systems Integration
- Wholesale Operations Automation
- ERP-driven Business Intelligence
- Financial Systems Integration
- Inventory Management Solutions

MANAGEMENT STRENGTHS:
- Proven ability to translate technical concepts to business stakeholders
- Experience managing complex technology implementations
- Strong problem-solving and analytical thinking
- Excellent communication and presentation skills
- Collaborative leadership style with focus on team development
- Results-oriented approach to technology initiatives

DEMOGRAPHIC INFORMATION:
Gender: Male
Race/Ethnicity: White  
Sexual Orientation: Heterosexual (Prefer not to disclose on applications)
Transgender: No
Disability Status: No
Veteran Status: No
Hispanic/Latino: No

LEGAL/EMPLOYMENT STATUS:
Obligations or Restrictions: No (no obligations or restrictions that would impact work at any company)
Security Clearance: No
Non-compete Agreements: No
Background Check Consent: Yes

COMPENSATION EXPECTATIONS:
Target Salary: $100,000
Minimum Salary: $80,000
Maximum Salary: $120,000
Preferred Range: $90,000 - $110,000

TECHNICAL WORK ACTIVITIES:
Daily Work Activities:
- Work with APIs: Yes (daily)
- Work with AI tools: Yes (daily)
- Work with databases: Yes (daily)
- Work with cloud services: Yes (daily)

AI and Machine Learning Experience:
- AI Project Experience: Yes (extensive experience with AI projects and implementations)
- AI Product Experience: Yes (worked on AI-related products and solutions)
- Machine Learning Experience: Yes (hands-on ML model development and deployment)
- AI Research: Yes (stays current with AI trends and implements cutting-edge solutions)

Technical Proficiencies:
- Python: Yes (4 years experience)
- JavaScript: Yes (experienced)
- SQL: Yes (database administration)
- Cloud Platforms: Yes (AWS, Azure)
- DevOps: Yes (CI/CD, automation)
- Agile/Scrum: Yes (experienced)

Automation Tools Expertise:
- Zapier: Yes (expert-level, 4+ years)
- Make (Integromat): Yes (expert-level)
- Workflow Automation: 4 years experience
- Advanced Automations Built: 50+ multi-step, multi-tool integrations
- Other Platforms: Power Automate, n8n, IFTTT

IT Transformation & Modernization:
- Managed IT operating model transformation projects: Yes (from inception to completion)
- Developed future-ready operating models using AI: Yes (across all IT functions)
- Digital transformation initiatives: Yes (enterprise-level)
- Technology modernization programs: Yes (cloud migration, automation)
- AI-based solutions development: Yes (integrated across IT functions)
- Change management for IT operations: Yes (process optimization)

Work Environment:
- Remote work: Yes (comfortable and equipped)
- Hybrid work: Yes (flexible)
- Onsite work: Yes (when needed)
- Part-time: Yes (available for 15-20 hours/month engagements)
- Retainer basis: Yes (comfortable with fixed monthly retainers)
- Travel: Yes (willing to travel up to 40-50% of the time)
- International travel: Yes (available for global projects)
- Overnight travel: Yes (comfortable with extended trips)

EMPLOYMENT TYPE PREFERENCES:
- W2 Employee: Yes (willing to join as direct W2 employee)
- Contract (1099): Yes (open to contract opportunities)
- Contract-to-Hire: Yes (interested in C2H arrangements)
- Corp-to-Corp (C2C): Yes (can work through my corporation)
- Full-time: Yes (preferred)
- Part-time: No (not currently seeking)
- Direct Hire: Yes (preferred for stability)
- Third Party: No (prefer direct relationships, but can work through vendors if needed)
Note: Flexible on employment type based on opportunity

EMPLOYMENT STATUS AND REFERRALS:
Current Employment Status: Not a current employee (for any company being applied to unless specifically stated)
Former Employee Status: No (has not worked for companies being applied to)
Employee Referrals: No (not referred by current employees)
Know Employees: No (does not personally know employees at companies being applied to)
How Found Company: LinkedIn (found job opportunities through LinkedIn job search)
Discovery Method: LinkedIn job board, company career pages, professional networking
"""
##<
'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Name of your most recent employer
recent_employer = "Numtrix" # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "4"             # Any number between "1" to "10" including 1 and 10, put it in quotes ""

# CRITICAL: Override answers for relationship and common questions that AI answered incorrectly
# For questions about relationships with employees at the company
employee_relationship = "No"       # Always "No" unless you actually know someone at the company
# For questions about previous work at the company
worked_at_company_before = "No"    # Always "No" unless you actually worked there before
# For questions about disability status  
disability_answer = "No"           # Use your actual status
# For questions about veteran status
veteran_answer = "No"              # Use your actual status
# For questions about willingness to relocate
willing_to_relocate = "Yes"        # Since you're targeting remote, this should be Yes for flexibility
##



# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = True          # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True    # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = False # True or False, Note: True or False are case-sensitive







############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
RapidApply Contributors
'''
############################################################################################################