"""
Author:     RapidApply Contributors
LinkedIn:   

Copyright (C) 2024 RapidApply Contributors

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/Nickalus12/RapidApply

Feature:    Grok AI Integration for intelligent job application responses
"""

from config.secrets import *
from config.settings import showAiErrorAlerts
from modules.helpers import print_lg, critical_error_log, convert_to_json
from modules.ai.prompts import *

from pyautogui import confirm
from openai import OpenAI
from openai.types.model import Model
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from typing import Iterator, Literal

def grok_create_client() -> OpenAI | None:
    '''
    Creates a Grok client using the OpenAI compatible API.
    * Returns an OpenAI-compatible client configured for xAI's Grok
    '''
    try:
        print_lg("Creating Grok client...")
        if not use_AI:
            raise ValueError("AI is not enabled! Please enable it by setting `use_AI = True` in `secrets.py` in `config` folder.")
        
        base_url = grok_api_url
        
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        
        # Create client with Grok endpoint
        client = OpenAI(base_url=base_url, api_key=grok_api_key)
        
        print_lg("---- SUCCESSFULLY CREATED GROK CLIENT! ----")
        print_lg(f"Using API URL: {base_url}")
        print_lg(f"Using Model: {grok_model}")
        print_lg("Check './config/secrets.py' for more details.\n")
        print_lg("---------------------------------------------")
        
        return client
    except Exception as e:
        error_message = f"Error occurred while creating Grok client. Make sure your API connection details are correct."
        critical_error_log(error_message, e)
        if showAiErrorAlerts:
            if "Pause AI error alerts" == confirm(f"{error_message}\n{str(e)}", "Grok Connection Error", ["Pause AI error alerts", "Okay Continue"]):
                showAiErrorAlerts = False
        return None

def grok_model_supports_temperature(model_name: str) -> bool:
    '''
    Checks if the specified Grok model supports the temperature parameter.
    * Takes in `model_name` of type `str` - The name of the Grok model
    * Returns `bool` - True if the model supports temperature adjustments
    '''
    # All Grok models support temperature
    grok_models = ["grok-2", "grok-2-1212", "grok-2-vision-1212", "grok-2-mini", "grok-beta"]
    return any(model in model_name for model in grok_models)

def grok_completion(client: OpenAI, messages: list[dict], response_format: dict = None, temperature: float = 0.7, stream: bool = stream_output) -> dict | ValueError:
    '''
    Completes a chat using Grok API and formats the results.
    * Takes in `client` of type `OpenAI` - The Grok client
    * Takes in `messages` of type `list[dict]` - The conversation messages
    * Takes in `response_format` of type `dict` for JSON representation (optional)
    * Takes in `temperature` of type `float` for creativity control (default 0.7 for more human-like responses)
    * Takes in `stream` of type `bool` for streaming output (optional)
    * Returns the response as text or JSON
    '''
    if not client: 
        raise ValueError("Grok client is not available!")

    # Set up parameters for the API call
    params = {
        "model": grok_model, 
        "messages": messages, 
        "stream": stream,
        "timeout": 60  # Grok can take longer for complex reasoning
    }
    
    # Add temperature if supported
    if grok_model_supports_temperature(grok_model):
        params["temperature"] = temperature
    
    # Add response format if needed
    if response_format:
        params["response_format"] = response_format

    try:
        # Make the API call
        print_lg(f"Calling Grok API for completion...")
        print_lg(f"Using model: {grok_model}")
        print_lg(f"Message count: {len(messages)}")
        print_lg(f"Temperature: {temperature}")
        completion = client.chat.completions.create(**params)

        result = ""
        
        # Process the response
        if stream:
            print_lg("--STREAMING STARTED")
            for chunk in completion:
                # Check for errors
                if hasattr(chunk, 'model_extra') and chunk.model_extra and chunk.model_extra.get("error"):
                    raise ValueError(f'Error occurred with Grok API: "{chunk.model_extra.get("error")}"')
                
                if chunk.choices and len(chunk.choices) > 0:
                    chunk_message = chunk.choices[0].delta.content
                    if chunk_message is not None:
                        result += chunk_message
                        print_lg(chunk_message, end="", flush=True)
            print_lg("\n--STREAMING COMPLETE")
        else:
            # Check for errors
            if hasattr(completion, 'model_extra') and completion.model_extra and completion.model_extra.get("error"):
                raise ValueError(f'Error occurred with Grok API: "{completion.model_extra.get("error")}"')
            
            result = completion.choices[0].message.content
        
        # Convert to JSON if needed
        if response_format:
            result = convert_to_json(result)
        
        print_lg("\nGrok Answer:\n")
        print_lg(result, pretty=response_format is not None)
        return result
    except Exception as e:
        error_message = f"Grok API error: {str(e)}"
        print_lg(f"Full error details: {e.__class__.__name__}: {str(e)}")
        if hasattr(e, 'response'):
            print_lg(f"Response data: {e.response.text if hasattr(e.response, 'text') else e.response}")
            
        # Provide specific guidance for common errors
        if "Connection" in str(e):
            print_lg("This might be a network issue. Please check your internet connection.")
            print_lg("If you're behind a firewall or proxy, make sure it allows connections to xAI's Grok API.")
        elif "401" in str(e) or "Unauthorized" in str(e):
            print_lg("This appears to be an authentication error. Your API key might be invalid or expired.")
            print_lg("Please check your Grok API key in config/secrets.py")
        elif "404" in str(e):
            print_lg("The requested resource could not be found. The API URL or model name might be incorrect.")
            print_lg("Make sure you're using the correct Grok API endpoint.")
        elif "429" in str(e):
            print_lg("You've exceeded the rate limit. Please wait before making more requests.")
            
        raise ValueError(error_message)

def grok_extract_skills(client: OpenAI, job_description: str, stream: bool = stream_output) -> dict | ValueError:
    '''
    Function to extract skills from job description using Grok API.
    * Takes in `client` of type `OpenAI` - The Grok client
    * Takes in `job_description` of type `str` - The job description text
    * Takes in `stream` of type `bool` to indicate if it's a streaming call
    * Returns a `dict` object representing JSON response
    '''
    try:
        print_lg("Extracting skills from job description using Grok...")
        
        # Using Grok-optimized prompt for skill extraction
        prompt = grok_extract_skills_prompt.format(job_description)
        messages = [{"role": "user", "content": prompt}]
        
        # Grok supports json_object response format
        custom_response_format = {"type": "json_object"}
        
        # Call Grok completion with lower temperature for accuracy
        result = grok_completion(
            client=client,
            messages=messages,
            response_format=custom_response_format,
            temperature=0.3,  # Lower temperature for more factual extraction
            stream=stream
        )
        
        # Ensure the result is a dictionary
        if isinstance(result, str):
            result = convert_to_json(result)
            
        return result
    except Exception as e:
        critical_error_log("Error occurred while extracting skills with Grok!", e)
        return {"error": str(e)}

def grok_answer_question(
    client: OpenAI, 
    question: str, options: list[str] | None = None, 
    question_type: Literal['text', 'textarea', 'single_select', 'multiple_select'] = 'text', 
    job_description: str = None, about_company: str = None, user_information_all: str = None,
    personal_style: str = None, stream: bool = stream_output
) -> dict | ValueError:
    '''
    Function to answer a question using Grok AI with personalized style.
    * Takes in `client` of type `OpenAI` - The Grok client
    * Takes in `question` of type `str` - The question to answer
    * Takes in `options` of type `list[str] | None` - Options for select questions
    * Takes in `question_type` - Type of question (text, textarea, single_select, multiple_select)
    * Takes in optional context parameters - job_description, about_company, user_information_all
    * Takes in `personal_style` of type `str` - Personal writing style preferences
    * Takes in `stream` of type `bool` - Whether to stream the output
    * Returns the AI's answer
    '''
    try:
        print_lg(f"Answering question using Grok AI: {question}")
        
        # Prepare user information
        user_info = user_information_all or ""
        
        # Use Grok-specific prompt that emphasizes personalization
        system_message = grok_system_prompt
        if personal_style:
            system_message += f"\n\nPersonal Style Guidelines:\n{personal_style}"
        
        # Prepare the main prompt
        prompt = grok_answer_prompt.format(user_info, question)
        
        # Add options to the prompt if available
        if options and (question_type in ['single_select', 'multiple_select']):
            options_str = "OPTIONS:\n" + "\n".join([f"- {option}" for option in options])
            prompt += f"\n\n{options_str}"
            
            if question_type == 'single_select':
                prompt += "\n\nPlease select exactly ONE option from the list above that best matches the user's profile and the job requirements."
            else:
                prompt += "\n\nYou may select MULTIPLE options from the list above if they accurately represent the user's qualifications."
        
        # Add contextual information for better answers
        context_added = False
        if job_description:
            prompt += f"\n\nJOB DESCRIPTION:\n{job_description}"
            context_added = True
        
        if about_company:
            prompt += f"\n\nABOUT COMPANY:\n{about_company}"
            context_added = True
            
        if context_added:
            prompt += "\n\nUse the job description and company information to tailor your response appropriately."
        
        # Adjust response style based on question type
        if question_type == 'textarea':
            prompt += "\n\nThis is a long-form response. Write a compelling, professional answer that showcases relevant experience and enthusiasm."
        elif question_type == 'text':
            prompt += "\n\nKeep your response concise but impactful."
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # Adjust temperature based on question type
        temperature = 0.7  # Default for creative, human-like responses
        if question_type in ['single_select', 'multiple_select']:
            temperature = 0.3  # Lower for factual selections
        elif "years" in question.lower() or "experience" in question.lower():
            temperature = 0.1  # Very low for numeric responses
        
        # Call Grok completion
        result = grok_completion(
            client=client,
            messages=messages,
            temperature=temperature,
            stream=stream
        )
        
        return result
    except Exception as e:
        critical_error_log("Error occurred while answering question with Grok!", e)
        return {"error": str(e)}