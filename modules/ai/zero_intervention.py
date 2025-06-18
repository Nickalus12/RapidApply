"""
Zero-Intervention Question Handler for RapidApply
Ensures 100% automation with intelligent fallbacks and no manual pauses

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

from typing import Any, Dict, List, Optional, Union
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import re

from modules.helpers import print_lg, critical_error_log
from modules.ai.question_handler import QuestionClassifier, IntelligentResponseGenerator
from modules.ai.grokConnections import grok_answer_question
from config.secrets import use_AI, ai_provider, grok_personal_style
from config.questions import *
from config.personals import *

class ZeroInterventionHandler:
    """
    Handles all question types with guaranteed responses - never pauses execution
    Implements multi-layer fallback system for 100% automation
    """
    
    def __init__(self, ai_client=None, user_profile: Dict[str, Any] = None):
        self.ai_client = ai_client
        self.classifier = QuestionClassifier()
        self.user_profile = user_profile or self._build_user_profile()
        self.response_generator = IntelligentResponseGenerator(self.user_profile)
        self.response_cache = {}
        self.failed_attempts = {}
        
    def _build_user_profile(self) -> Dict[str, Any]:
        """Builds comprehensive user profile from config"""
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'location': f"{city}, {state}, {country}",
            'years_experience': years_of_experience,
            'current_employer': recent_employer,
            'linkedin': linkedIn,
            'website': website,
            'headline': linkedin_headline,
            'summary': linkedin_summary,
            'desired_salary': desired_salary,
            'notice_period': notice_period,
            'visa_status': require_visa,
            'citizenship': us_citizenship,
            'clearance': security_clearance,
            'education': 'Bachelor\'s Degree' if not did_masters else 'Master\'s Degree'
        }
    
    def handle_question(self, 
                       question_element: WebElement,
                       question_text: str,
                       field_type: str = 'text',
                       options: List[str] = None,
                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for handling any question with zero manual intervention
        
        Args:
            question_element: Selenium WebElement for the input field
            question_text: The question being asked
            field_type: Type of input (text, textarea, select, radio, checkbox)
            options: Available options for select/radio fields
            context: Additional context (job description, company info)
            
        Returns:
            Dict with response details and success status
        """
        print_lg(f"[Zero-Intervention] Processing question: {question_text[:100]}...")
        
        # Initialize context
        context = context or {}
        context['question_text'] = question_text
        context['field_type'] = field_type
        context['options'] = options
        
        # Try multiple strategies in order
        strategies = [
            self._try_ai_response,
            self._try_pattern_matching,
            self._try_intelligent_default,
            self._try_emergency_fallback
        ]
        
        for strategy_num, strategy in enumerate(strategies, 1):
            try:
                print_lg(f"[Zero-Intervention] Attempting strategy {strategy_num}: {strategy.__name__}")
                result = strategy(question_element, question_text, field_type, options, context)
                
                if result and result.get('success'):
                    print_lg(f"[Zero-Intervention] Success with strategy {strategy_num}!")
                    return result
                    
            except Exception as e:
                print_lg(f"[Zero-Intervention] Strategy {strategy_num} failed: {str(e)}")
                continue
        
        # This should never happen, but if it does, use absolute fallback
        print_lg("[Zero-Intervention] All strategies failed, using absolute fallback")
        return self._absolute_fallback(question_element, field_type, options)
    
    def _try_ai_response(self, element: WebElement, question: str, 
                        field_type: str, options: List[str], context: Dict) -> Dict[str, Any]:
        """First strategy: Use AI (Grok) for intelligent response"""
        if not use_AI or not self.ai_client:
            return {'success': False, 'reason': 'AI not enabled'}
        
        try:
            # Check cache first
            cache_key = f"{question}_{field_type}_{str(options)}"
            if cache_key in self.response_cache:
                cached_response = self.response_cache[cache_key]
                return self._apply_response(element, cached_response, field_type)
            
            # Get AI response based on provider
            if ai_provider.lower() == "grok" or use_grok_for_openai:
                response = grok_answer_question(
                    self.ai_client,
                    question,
                    options=options,
                    question_type=field_type,
                    job_description=context.get('job_description'),
                    about_company=context.get('company_info'),
                    user_information_all=self._format_user_info(),
                    personal_style=grok_personal_style,
                    stream=False
                )
            else:
                # Fallback to other AI providers
                response = self._get_other_ai_response(question, field_type, options, context)
            
            if response and self._validate_response(response, field_type, options):
                # Cache successful response
                self.response_cache[cache_key] = response
                return self._apply_response(element, response, field_type)
            
            return {'success': False, 'reason': 'Invalid AI response'}
            
        except Exception as e:
            print_lg(f"[Zero-Intervention] AI response failed: {str(e)}")
            return {'success': False, 'reason': str(e)}
    
    def _try_pattern_matching(self, element: WebElement, question: str,
                             field_type: str, options: List[str], context: Dict) -> Dict[str, Any]:
        """Second strategy: Use pattern matching for known question types"""
        try:
            # Use the response generator which includes pattern matching
            response = self.response_generator.generate_response(
                question=question,
                question_type=field_type,
                options=options,
                context=context
            )
            
            if response and self._validate_response(response, field_type, options):
                return self._apply_response(element, response, field_type)
            
            return {'success': False, 'reason': 'Pattern matching failed'}
            
        except Exception as e:
            print_lg(f"[Zero-Intervention] Pattern matching failed: {str(e)}")
            return {'success': False, 'reason': str(e)}
    
    def _try_intelligent_default(self, element: WebElement, question: str,
                                field_type: str, options: List[str], context: Dict) -> Dict[str, Any]:
        """Third strategy: Use intelligent defaults based on question analysis"""
        try:
            # Classify question to determine best default
            classification = self.classifier.classify_question(question, options)
            
            # Get default response based on classification
            if classification['response_type'] == 'numeric':
                response = str(years_of_experience)
            elif classification['response_type'] == 'boolean':
                response = 'Yes'
            elif classification['response_type'] == 'select' and options:
                response = self._select_safe_option(options)
            elif field_type == 'textarea':
                response = self._get_safe_textarea_response(question)
            else:
                response = classification.get('default_response', 'Yes')
            
            return self._apply_response(element, response, field_type)
            
        except Exception as e:
            print_lg(f"[Zero-Intervention] Intelligent default failed: {str(e)}")
            return {'success': False, 'reason': str(e)}
    
    def _try_emergency_fallback(self, element: WebElement, question: str,
                               field_type: str, options: List[str], context: Dict) -> Dict[str, Any]:
        """Fourth strategy: Emergency fallback with universal safe responses"""
        try:
            response = self._get_emergency_response(field_type, options, question)
            return self._apply_response(element, response, field_type)
            
        except Exception as e:
            print_lg(f"[Zero-Intervention] Emergency fallback failed: {str(e)}")
            return {'success': False, 'reason': str(e)}
    
    def _absolute_fallback(self, element: WebElement, field_type: str, options: List[str]) -> Dict[str, Any]:
        """Absolute last resort - always returns something"""
        try:
            if field_type == 'select' and options:
                response = options[0]
            elif field_type == 'radio' and options:
                response = options[0]
            elif field_type == 'checkbox':
                response = True
            elif field_type == 'textarea':
                response = "I am interested in this opportunity."
            else:
                response = "5"  # Safe numeric default
            
            # Force apply the response
            if field_type in ['select', 'radio']:
                # Click the option
                element.click()
                time.sleep(0.5)
            elif field_type == 'checkbox':
                if not element.is_selected():
                    element.click()
            else:
                # Clear and type
                element.clear()
                element.send_keys(str(response))
            
            return {'success': True, 'response': response, 'strategy': 'absolute_fallback'}
            
        except Exception as e:
            # Even if this fails, return success to prevent stopping
            return {'success': True, 'response': 'Failed but continuing', 'error': str(e)}
    
    def _apply_response(self, element: WebElement, response: str, field_type: str) -> Dict[str, Any]:
        """Applies the response to the form element"""
        try:
            if field_type in ['text', 'textarea']:
                # Clear existing text
                element.clear()
                # Type response
                element.send_keys(str(response))
                # Trigger change event
                element.send_keys(Keys.TAB)
                
            elif field_type == 'select':
                # Handle select dropdown
                from selenium.webdriver.support.ui import Select
                select = Select(element)
                
                # Try to select by visible text
                try:
                    select.select_by_visible_text(str(response))
                except:
                    # Try by value
                    try:
                        select.select_by_value(str(response))
                    except:
                        # Select first option
                        select.select_by_index(0)
                        
            elif field_type == 'radio' or field_type == 'checkbox':
                # Click if not already selected
                if not element.is_selected():
                    element.click()
                    
            else:
                # Unknown type - try text input
                element.clear()
                element.send_keys(str(response))
            
            return {
                'success': True,
                'response': response,
                'field_type': field_type
            }
            
        except Exception as e:
            print_lg(f"[Zero-Intervention] Failed to apply response: {str(e)}")
            # Try JavaScript as fallback
            try:
                driver = element.parent
                driver.execute_script(f"arguments[0].value = '{response}';", element)
                driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
                return {'success': True, 'response': response, 'method': 'javascript'}
            except:
                return {'success': False, 'error': str(e)}
    
    def _validate_response(self, response: Any, field_type: str, options: List[str] = None) -> bool:
        """Validates that the response is appropriate for the field type"""
        if not response:
            return False
            
        response_str = str(response).strip()
        
        if field_type in ['text', 'textarea']:
            # Check length constraints
            if field_type == 'text' and len(response_str) > 200:
                return False
            if field_type == 'textarea' and len(response_str) > 1000:
                return False
            return len(response_str) > 0
            
        elif field_type in ['select', 'radio'] and options:
            # Check if response is in options
            return response_str in options
            
        elif field_type == 'checkbox':
            # Should be boolean-like
            return response_str.lower() in ['true', 'false', 'yes', 'no', '1', '0']
            
        else:
            return True
    
    def _format_user_info(self) -> str:
        """Formats user profile information for AI context"""
        info_parts = []
        
        info_parts.append(f"Name: {self.user_profile['name']}")
        info_parts.append(f"Email: {self.user_profile['email']}")
        info_parts.append(f"Location: {self.user_profile['location']}")
        info_parts.append(f"Years of Experience: {self.user_profile['years_experience']}")
        info_parts.append(f"Current/Recent Employer: {self.user_profile['current_employer']}")
        info_parts.append(f"Professional Headline: {self.user_profile['headline']}")
        info_parts.append(f"LinkedIn: {self.user_profile['linkedin']}")
        
        if self.user_profile['website']:
            info_parts.append(f"Portfolio/Website: {self.user_profile['website']}")
            
        info_parts.append(f"\nProfessional Summary:\n{self.user_profile['summary']}")
        
        info_parts.append(f"\nAdditional Information:")
        info_parts.append(f"- Desired Salary: ${self.user_profile['desired_salary']}")
        info_parts.append(f"- Notice Period: {self.user_profile['notice_period']} days")
        info_parts.append(f"- Visa Sponsorship Required: {self.user_profile['visa_status']}")
        info_parts.append(f"- Security Clearance: {'Yes' if self.user_profile['clearance'] else 'No'}")
        info_parts.append(f"- Education Level: {self.user_profile['education']}")
        
        return "\n".join(info_parts)
    
    def _select_safe_option(self, options: List[str]) -> str:
        """Selects the safest option from a list"""
        # Remove placeholder options
        valid_options = [opt for opt in options if not self._is_placeholder(opt)]
        
        if not valid_options:
            return options[0] if options else ""
        
        # Prefer positive/agreeable options
        positive_keywords = ['yes', 'agree', 'available', 'willing', 'authorized', 'eligible']
        for option in valid_options:
            if any(keyword in option.lower() for keyword in positive_keywords):
                return option
        
        # Avoid negative options
        negative_keywords = ['no', 'not', 'unable', 'unavailable', 'ineligible']
        non_negative_options = [opt for opt in valid_options 
                               if not any(keyword in opt.lower() for keyword in negative_keywords)]
        
        if non_negative_options:
            return non_negative_options[0]
        
        # Return first valid option
        return valid_options[0]
    
    def _is_placeholder(self, option: str) -> bool:
        """Checks if an option is a placeholder"""
        placeholders = ['select', 'choose', 'pick', '--', 'please select', 'select one', 
                       'select an option', 'choose one', 'pick one']
        return option.lower().strip() in placeholders
    
    def _get_safe_textarea_response(self, question: str) -> str:
        """Gets a safe response for textarea fields"""
        question_lower = question.lower()
        
        if 'why' in question_lower and ('interested' in question_lower or 'apply' in question_lower):
            return "I am excited about this opportunity because it aligns perfectly with my skills and career aspirations. The role offers the chance to contribute meaningfully while continuing to grow professionally."
        elif 'experience' in question_lower:
            return f"With {years_of_experience} years of relevant experience, I have developed strong expertise in the required areas. I'm confident in my ability to contribute effectively to your team."
        elif 'qualification' in question_lower or 'qualified' in question_lower:
            return "My background includes hands-on experience with similar projects and technologies, making me well-qualified for this position."
        else:
            return "I am enthusiastic about this opportunity and confident that my skills and experience make me a strong candidate for this role."
    
    def _get_emergency_response(self, field_type: str, options: List[str], question: str) -> str:
        """Gets emergency fallback response based on field type"""
        if field_type == 'select' and options:
            return self._select_safe_option(options)
        elif field_type == 'radio' and options:
            return options[0] if len(options) > 0 else 'Yes'
        elif field_type == 'checkbox':
            return 'true'
        elif field_type == 'textarea':
            return self._get_safe_textarea_response(question)
        elif any(num_word in question.lower() for num_word in ['how many', 'years', 'number']):
            return str(years_of_experience)
        else:
            return 'Yes'
    
    def _get_other_ai_response(self, question: str, field_type: str, 
                              options: List[str], context: Dict) -> str:
        """Gets response from other AI providers (placeholder for other integrations)"""
        # This would integrate with OpenAI, DeepSeek, etc.
        # For now, return None to trigger fallback
        return None

# Export main class
__all__ = ['ZeroInterventionHandler']