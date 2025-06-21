# Smart Resume Selection Guide

## Overview

RapidApply now includes an AI-powered Smart Resume Selection feature that automatically selects the best resume for each job application based on the job requirements, company, and required skills.

## How It Works

1. **Job Analysis**: When applying to a job, the system analyzes:
   - Job title and description
   - Company name
   - Required and preferred skills
   - Job level (entry, mid, senior)

2. **Resume Matching**: The AI compares available resumes against job requirements to find the best match

3. **Intelligent Selection**: Uses Grok AI to understand context and make intelligent decisions

4. **Fallback Logic**: If AI is unavailable, uses rule-based matching as backup

## Setup Instructions

### 1. Enable the Feature

In `config/settings.py`, ensure the feature is enabled:

```python
use_smart_resume_selection = True
```

### 2. Organize Your Resumes

Create a `resumes` folder in your RapidApply directory with the following structure:

```
resumes/
├── technical/
│   ├── backend_engineer_resume.pdf
│   ├── frontend_developer_resume.pdf
│   └── fullstack_engineer_resume.pdf
├── management/
│   ├── tech_lead_resume.pdf
│   ├── project_manager_resume.pdf
│   └── engineering_manager_resume.pdf
├── general/
│   └── general_software_engineer_resume.pdf
└── custom/
    └── specialized_ml_engineer_resume.pdf
```

### 3. Resume Naming Convention

Use descriptive names that indicate:
- Role focus (e.g., "backend_engineer", "project_manager")
- Experience level (e.g., "senior_developer", "junior_analyst")
- Specialization (e.g., "ml_engineer", "devops_specialist")

### 4. Resume Formats

- Supported formats: PDF, DOCX
- Keep file sizes reasonable (< 5MB)
- Ensure text is extractable (not scanned images)

## Features

### AI-Powered Selection
- Uses Grok to understand job context
- Matches skills, experience level, and role requirements
- Provides confidence scores and reasoning

### Smart Categorization
- Automatically categorizes resumes by content
- Identifies technical vs management roles
- Detects specializations and focus areas

### Performance Optimization
- Caches resume content for faster processing
- Remembers previous selections
- Tracks selection history for analytics

### Fallback Mechanisms
- Rule-based matching when AI unavailable
- Keyword and skill matching
- Category-based selection

## Configuration Options

### Using Multiple Resume Variants

1. **Technical Roles**: Place programming-focused resumes in `resumes/technical/`
2. **Leadership Roles**: Place management resumes in `resumes/management/`
3. **General Purpose**: Place versatile resumes in `resumes/general/`
4. **Specialized**: Place niche resumes in `resumes/custom/`

### Selection Criteria

The system considers:
- **Skill Match**: How well resume skills match job requirements
- **Experience Level**: Junior/Mid/Senior alignment
- **Role Type**: Technical vs Management vs Hybrid
- **Industry Keywords**: Domain-specific terminology
- **Company Culture**: Startup vs Enterprise preferences

## Monitoring and Analytics

The system tracks:
- Which resumes are selected most often
- Selection confidence scores
- Success rates per resume type

View statistics in `resumes/selection_history.json`

## Troubleshooting

### Resume Not Being Selected
1. Check if file exists in `resumes/` folder
2. Verify file is readable (PDF/DOCX)
3. Ensure descriptive filename
4. Check AI client is initialized

### Wrong Resume Selected
1. Review resume categorization
2. Update resume content to better match intended roles
3. Use more specific filenames
4. Check job description parsing

### Feature Not Working
1. Verify `use_smart_resume_selection = True` in settings
2. Ensure AI is enabled and configured
3. Check `resumes/` folder exists
4. Review error logs

## Best Practices

1. **Maintain 3-5 Resume Variants**: Don't overdo it - quality over quantity
2. **Update Regularly**: Keep resumes current with latest experience
3. **Clear Differentiation**: Each resume should target different role types
4. **Consistent Formatting**: Use similar formats for professional appearance
5. **Keyword Optimization**: Include relevant industry keywords

## Example Scenarios

### Scenario 1: Backend Engineer Position
- Job requires: Python, Django, PostgreSQL, AWS
- System selects: `technical/backend_engineer_resume.pdf`
- Confidence: 0.92
- Reason: "Strong match on Python and backend technologies"

### Scenario 2: Tech Lead Position
- Job requires: Leadership, Architecture, Team Management
- System selects: `management/tech_lead_resume.pdf`
- Confidence: 0.88
- Reason: "Combines technical expertise with leadership experience"

### Scenario 3: Startup Full-Stack Role
- Job requires: React, Node.js, Agile, Fast-paced
- System selects: `technical/fullstack_engineer_resume.pdf`
- Confidence: 0.85
- Reason: "Full-stack experience matches startup needs"

## Future Enhancements

- Resume content customization per application
- A/B testing different resume versions
- Success rate tracking and optimization
- Dynamic resume generation based on job requirements

---

For more information or to report issues, visit the [RapidApply GitHub repository](https://github.com/Nickalus12/RapidApply).