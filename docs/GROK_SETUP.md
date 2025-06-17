# 🤖 Grok AI Integration Guide for RapidApply

## Overview

RapidApply now supports xAI's Grok models for intelligent job application responses. Grok provides advanced language understanding with a focus on authentic, personalized responses that match your communication style.

## Features

- **Personalized Responses**: Grok adapts to your personal writing style
- **Context-Aware Answers**: Utilizes job descriptions and company information
- **Smart Skill Extraction**: Accurately identifies required and preferred skills
- **Multiple Model Support**: Choose from Grok-2, Grok-2-mini, or Grok-3

## Setup Instructions

### 1. Get Your Grok API Key

1. Visit [x.ai](https://x.ai) 
2. Sign up or log in to your account
3. Navigate to the API section
4. Generate your API key

### 2. Configure RapidApply

Edit `config/secrets.py`:

```python
# Select Grok as your AI provider
ai_provider = "grok"

# Grok Configuration
grok_api_url = "https://api.x.ai/v1"
grok_api_key = "your-api-key-here"  # Replace with your actual API key
grok_model = "grok-2-latest"       # Options: grok-2-latest, grok-2-mini, grok-3-latest

# Customize your personal style
grok_personal_style = """
Professional yet conversational tone. 
Show enthusiasm for technology and problem-solving.
Use concrete examples from experience when relevant.
Be confident but not arrogant.
"""
```

### 3. Personalize Your Style

The `grok_personal_style` setting is crucial for authentic responses. Customize it to match how you communicate:

```python
# Example for a more casual style:
grok_personal_style = """
Friendly and approachable communication style.
Use simple, clear language without jargon.
Show genuine curiosity and eagerness to learn.
Be humble about achievements.
"""

# Example for a more formal style:
grok_personal_style = """
Formal and professional communication.
Emphasize leadership and strategic thinking.
Use industry-specific terminology appropriately.
Highlight quantifiable achievements.
"""
```

### 4. Test Your Configuration

Run the test script to verify everything is working:

```bash
python test_grok.py
```

## Model Selection Guide

### Grok-2-latest (Recommended)
- Best overall performance
- Excellent for complex questions
- Most human-like responses

### Grok-2-mini
- Faster response times
- Lower cost per request
- Good for simple questions

### Grok-3-latest
- Cutting-edge capabilities
- Best reasoning abilities
- Premium option

## Usage Tips

### 1. Optimize Your Personal Information

In `config/personals.py`, provide detailed information:
- List all relevant skills
- Include years of experience
- Mention key achievements
- Add relevant certifications

### 2. Answer Quality

Grok will generate responses that:
- Match the job requirements
- Sound authentic to your style
- Include relevant examples
- Show appropriate enthusiasm

### 3. Response Types

- **Numeric Questions**: Returns just the number (e.g., "5" for years of experience)
- **Yes/No Questions**: Simple "Yes" or "No" responses
- **Short Answers**: Concise, impactful single sentences
- **Long Answers**: Detailed responses under 350 characters

## Troubleshooting

### API Key Issues
```
Error: 401 Unauthorized
```
- Verify your API key is correct
- Check if your API key has proper permissions
- Ensure you've activated the API in your x.ai account

### Rate Limiting
```
Error: 429 Too Many Requests
```
- Grok has rate limits to prevent abuse
- Wait a few minutes before retrying
- Consider upgrading your API plan

### Connection Issues
- Check your internet connection
- Verify the API URL is correct
- Ensure no firewall is blocking the connection

## Cost Considerations

Grok API pricing varies by model:
- Check current pricing at [x.ai/pricing](https://x.ai)
- Monitor your usage in the x.ai dashboard
- Consider using grok-2-mini for cost savings

## Advanced Configuration

### Custom Prompts

You can modify Grok prompts in `modules/ai/prompts.py`:
- `grok_system_prompt`: Base personality
- `grok_answer_prompt`: Question answering format
- `grok_extract_skills_prompt`: Skill extraction logic

### Stream Output

Enable streaming for real-time responses:
```python
stream_output = True  # In config/secrets.py
```

## Support

For issues specific to Grok integration:
- Check the [RapidApply Issues](https://github.com/Nickalus12/RapidApply/issues)
- Review x.ai documentation
- Contact Discord: **Nickalus**

---

Happy job hunting with Grok-powered intelligence! 🚀