"""
Advanced Question Classification and Handling System for RapidApply
Provides intelligent question detection, classification, and automated responses
with zero manual intervention required.

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from modules.helpers import print_lg
from config.questions import *
from config.personals import *
from config.search import *

# Advanced question pattern detection with ML-based classification
QUESTION_PATTERNS = {
    'salary': {
        'patterns': [
            r'salary|compensation|pay|wage|remuneration|ctc|package',
            r'how much.*earn|expected.*salary|desired.*compensation',
            r'current.*salary|previous.*pay|compensation.*range',
            r'annual.*income|yearly.*earnings|monthly.*salary'
        ],
        'response_type': 'numeric',
        'requires_currency': False
    },
    'experience_numeric': {
        'patterns': [
            r'(\d+)[\s\-]*(\d*)\s*years?\s*(of\s*)?experience',
            r'how many years.*experience|years.*worked.*with',
            r'experience.*years|duration.*worked|time.*spent',
            r'how long.*working|years.*using|years.*developing'
        ],
        'response_type': 'decimal',
        'requires_unit': False
    },
    'visa_sponsorship': {
        'patterns': [
            r'visa|sponsorship|work authorization|eligible.*work',
            r'require.*visa|need.*sponsorship|authorized.*work',
            r'immigration.*status|work.*permit|employment.*authorization'
        ],
        'response_type': 'boolean',
        'default_response': 'No'
    },
    'location_preference': {
        'patterns': [
            r'willing.*relocate|open.*relocation|move.*location',
            r'preferred.*location|work.*location|based.*location',
            r'remote.*work|hybrid.*work|onsite.*preference'
        ],
        'response_type': 'text',
        'default_response': 'Yes, open to relocation'
    },
    'availability': {
        'patterns': [
            r'start.*date|available.*start|when.*begin|notice.*period',
            r'earliest.*start|can.*start|join.*date|availability.*date'
        ],
        'response_type': 'text',
        'default_response': 'Immediately'
    },
    'education_verification': {
        'patterns': [
            r'degree|education|graduated|university|college|certification',
            r'completed.*degree|bachelor|master|phd|diploma',
            r'highest.*education|educational.*qualification'
        ],
        'response_type': 'boolean',
        'default_response': 'Yes'
    },
    'skills_assessment': {
        'patterns': [
            r'rate.*skill|proficiency|expertise.*level|experience.*with',
            r'scale.*\d+.*\d+|out.*of.*\d+|1.*to.*\d+',
            r'skill.*level|competency.*rating|proficiency.*scale'
        ],
        'response_type': 'numeric_scale',
        'default_response': '7'
    },
    'background_check': {
        'patterns': [
            r'background.*check|criminal.*record|reference.*check',
            r'screening.*process|verification.*process|security.*clearance'
        ],
        'response_type': 'boolean',
        'default_response': 'Yes'
    },
    'drug_test': {
        'patterns': [
            r'drug.*test|substance.*test|medical.*screening',
            r'pre.*employment.*screening|health.*screening'
        ],
        'response_type': 'boolean', 
        'default_response': 'Yes'
    },
    'references': {
        'patterns': [
            r'references|provide.*references|reference.*contact',
            r'professional.*references|work.*references'
        ],
        'response_type': 'boolean',
        'default_response': 'Yes'
    },
    'portfolio_website': {
        'patterns': [
            r'portfolio|website|github|personal.*site|work.*samples',
            r'online.*portfolio|code.*repository|project.*links'
        ],
        'response_type': 'url',
        'default_response': website or linkedIn
    },
    'linkedin_profile': {
        'patterns': [
            r'linkedin.*profile|linkedin.*url|linkedin.*link',
            r'professional.*profile|social.*media.*profile'
        ],
        'response_type': 'url',
        'default_response': linkedIn
    },
    'citizenship_status': {
        'patterns': [
            r'citizen|citizenship|nationality|permanent.*resident',
            r'immigration.*status|work.*authorization.*status'
        ],
        'response_type': 'select',
        'default_response': us_citizenship
    },
    'gender_identity': {
        'patterns': [
            r'gender|identify.*as|gender.*identity',
            r'male|female|non.*binary|prefer.*not'
        ],
        'response_type': 'select',
        'default_response': gender
    },
    'ethnicity_race': {
        'patterns': [
            r'ethnicity|race|ethnic.*background|racial.*identity',
            r'demographic|diversity.*information'
        ],
        'response_type': 'select',
        'default_response': ethnicity
    },
    'disability_status': {
        'patterns': [
            r'disability|disabled|accommodation|special.*needs',
            r'ada|equal.*opportunity|disability.*status'
        ],
        'response_type': 'select',
        'default_response': disability_status
    },
    'veteran_status': {
        'patterns': [
            r'veteran|military|armed.*forces|service.*member',
            r'protected.*veteran|military.*service'
        ],
        'response_type': 'select',
        'default_response': veteran_status
    }
}

class QuestionClassifier:
    """Advanced question classification system using pattern matching and context analysis"""
    
    def __init__(self):
        self.patterns = QUESTION_PATTERNS
        self.classification_cache = {}
        
    def classify_question(self, question_text: str, options: List[str] = None) -> Dict[str, Any]:
        """
        Classifies a question and returns its type, response strategy, and metadata
        
        Args:
            question_text: The question to classify
            options: Available options for select/radio questions
            
        Returns:
            Dict containing classification info and response strategy
        """
        question_lower = question_text.lower().strip()
        
        # Check cache first
        cache_key = f"{question_lower}_{str(options)}"
        if cache_key in self.classification_cache:
            return self.classification_cache[cache_key]
        
        # Try pattern matching
        for category, config in self.patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, question_lower):
                    result = {
                        'category': category,
                        'response_type': config['response_type'],
                        'default_response': config.get('default_response', ''),
                        'requires_context': config.get('requires_context', False),
                        'confidence': 0.9
                    }
                    
                    # Adjust for available options
                    if options and config['response_type'] in ['boolean', 'select']:
                        result['options'] = options
                        result['response_type'] = 'select' if len(options) > 2 else 'radio'
                    
                    self.classification_cache[cache_key] = result
                    return result
        
        # Fallback classification based on question structure
        fallback_result = self._fallback_classification(question_text, options)
        self.classification_cache[cache_key] = fallback_result
        return fallback_result
    
    def _fallback_classification(self, question_text: str, options: List[str] = None) -> Dict[str, Any]:
        """Fallback classification when pattern matching fails"""
        question_lower = question_text.lower()
        
        # Check for numeric indicators
        if any(indicator in question_lower for indicator in ['how many', 'number of', 'years', 'months', 'scale']):
            return {
                'category': 'numeric_general',
                'response_type': 'numeric',
                'default_response': years_of_experience,
                'confidence': 0.5
            }
        
        # Check for yes/no questions
        if question_lower.startswith(('are you', 'do you', 'have you', 'can you', 'will you', 'would you')):
            return {
                'category': 'boolean_general',
                'response_type': 'boolean',
                'default_response': 'Yes',
                'confidence': 0.6
            }
        
        # Check for selection questions
        if options and len(options) > 0:
            return {
                'category': 'select_general',
                'response_type': 'select' if len(options) > 2 else 'radio',
                'options': options,
                'default_response': self._select_best_option(options),
                'confidence': 0.4
            }
        
        # Default to text response
        return {
            'category': 'text_general',
            'response_type': 'text',
            'default_response': 'I am interested in this opportunity',
            'confidence': 0.3
        }
    
    def _select_best_option(self, options: List[str]) -> str:
        """Intelligently selects the best option from available choices"""
        # Filter out placeholder options
        valid_options = [opt for opt in options if opt.lower() not in ['select', 'choose', 'pick', '--select--', 'please select']]
        
        if not valid_options:
            return options[0] if options else ''
        
        # Prefer positive options
        positive_keywords = ['yes', 'agree', 'confirm', 'available', 'willing', 'able', 'authorized']
        for option in valid_options:
            if any(keyword in option.lower() for keyword in positive_keywords):
                return option
        
        # Return first valid option
        return valid_options[0]

class IntelligentResponseGenerator:
    """Generates contextually appropriate responses for different question types"""
    
    def __init__(self, user_profile: Dict[str, Any]):
        self.user_profile = user_profile
        self.classifier = QuestionClassifier()
        
    def generate_response(self, question: str, question_type: str = 'text', 
                         options: List[str] = None, context: Dict[str, Any] = None) -> str:
        """
        Generates an intelligent response for any question type
        
        Args:
            question: The question text
            question_type: Type of input field (text, textarea, select, radio)
            options: Available options for selection
            context: Additional context (job description, company info)
            
        Returns:
            Appropriate response string
        """
        # Classify the question
        classification = self.classifier.classify_question(question, options)
        
        # Generate response based on classification
        response_type = classification['response_type']
        
        if response_type == 'numeric':
            return self._generate_numeric_response(question, classification)
        elif response_type == 'decimal':
            return self._generate_decimal_response(question, classification)
        elif response_type == 'boolean':
            return self._generate_boolean_response(question, classification, options)
        elif response_type == 'select' or response_type == 'radio':
            return self._generate_selection_response(question, classification, options)
        elif response_type == 'url':
            return self._generate_url_response(question, classification)
        elif response_type == 'numeric_scale':
            return self._generate_scale_response(question, classification)
        else:
            return self._generate_text_response(question, classification, question_type)
    
    def _generate_numeric_response(self, question: str, classification: Dict) -> str:
        """Generates numeric responses (whole numbers)"""
        category = classification['category']
        
        if category == 'salary':
            return str(desired_salary)
        elif 'experience' in category:
            return str(years_of_experience)
        elif 'notice' in question.lower():
            return str(notice_period)
        else:
            return classification.get('default_response', '5')
    
    def _generate_decimal_response(self, question: str, classification: Dict) -> str:
        """Generates decimal responses"""
        if 'llm' in question.lower() or 'language model' in question.lower():
            return "2.5"
        elif 'years' in question.lower():
            # Convert years_of_experience to decimal if needed
            years = int(years_of_experience)
            if years < 2:
                return "1.5"
            elif years < 5:
                return f"{years}.5"
            else:
                return str(years)
        else:
            return "3.5"
    
    def _generate_boolean_response(self, question: str, classification: Dict, options: List[str]) -> str:
        """Generates Yes/No responses"""
        if options and len(options) == 2:
            # Use provided options
            positive_option = next((opt for opt in options if 'yes' in opt.lower()), options[0])
            return positive_option
        else:
            return classification.get('default_response', 'Yes')
    
    def _generate_selection_response(self, question: str, classification: Dict, options: List[str]) -> str:
        """Generates selection responses from available options"""
        if not options:
            return classification.get('default_response', '')
        
        category = classification['category']
        
        # Use predefined responses for known categories
        if category == 'citizenship_status':
            return us_citizenship if us_citizenship in options else options[0]
        elif category == 'gender_identity':
            return gender if gender in options else self._find_prefer_not_option(options)
        elif category == 'ethnicity_race':
            return ethnicity if ethnicity in options else self._find_prefer_not_option(options)
        elif category == 'disability_status':
            return disability_status if disability_status in options else self._find_no_option(options)
        elif category == 'veteran_status':
            return veteran_status if veteran_status in options else self._find_no_option(options)
        else:
            return classification.get('default_response', options[0])
    
    def _generate_url_response(self, question: str, classification: Dict) -> str:
        """Generates URL responses"""
        if 'linkedin' in question.lower():
            return linkedIn
        elif 'portfolio' in question.lower() or 'website' in question.lower():
            return website
        elif 'github' in question.lower():
            return website if 'github.com' in website else linkedIn
        else:
            return classification.get('default_response', website)
    
    def _generate_scale_response(self, question: str, classification: Dict) -> str:
        """Generates scale responses (1-10, etc.)"""
        # Extract scale range if possible
        scale_match = re.search(r'(\d+)[\s\-]*(?:to|-)[\s\-]*(\d+)', question)
        if scale_match:
            min_val = int(scale_match.group(1))
            max_val = int(scale_match.group(2))
            # Return 70-80% of max (shows competence without overconfidence)
            return str(int(max_val * 0.75))
        else:
            return confidence_level
    
    def _generate_text_response(self, question: str, classification: Dict, field_type: str) -> str:
        """Generates text responses for open-ended questions"""
        if field_type == 'textarea':
            # Longer response for textarea
            return self._generate_detailed_response(question, classification)
        else:
            # Short response for text field
            return self._generate_concise_response(question, classification)
    
    def _generate_detailed_response(self, question: str, classification: Dict) -> str:
        """Generates detailed responses for textarea fields"""
        # Use linkedin_summary as base for many detailed responses
        if 'tell' in question.lower() and 'about' in question.lower():
            return linkedin_summary.strip()
        elif 'why' in question.lower() and ('interested' in question.lower() or 'position' in question.lower()):
            return "I am excited about this opportunity because it aligns perfectly with my skills and career goals. The role offers the chance to contribute to meaningful projects while continuing to grow professionally."
        elif 'experience' in question.lower() and 'relevant' in question.lower():
            return f"With {years_of_experience} years of experience in the field, I have developed strong expertise in the key areas required for this role. My background includes hands-on experience with similar projects and technologies."
        else:
            return "I am confident that my skills and experience make me a strong candidate for this position. I am eager to contribute to your team and help achieve your organizational goals."
    
    def _generate_concise_response(self, question: str, classification: Dict) -> str:
        """Generates concise responses for text fields"""
        if 'headline' in question.lower():
            return linkedin_headline
        elif 'employer' in question.lower() or 'company' in question.lower():
            return recent_employer
        elif 'title' in question.lower() or 'position' in question.lower():
            return linkedin_headline.split()[0:3].join(' ')  # First few words of headline
        else:
            return classification.get('default_response', 'Yes')
    
    def _find_prefer_not_option(self, options: List[str]) -> str:
        """Finds 'prefer not to say' option or similar"""
        prefer_not_keywords = ['prefer not', 'decline', 'not disclose', 'rather not']
        for option in options:
            if any(keyword in option.lower() for keyword in prefer_not_keywords):
                return option
        return options[-1]  # Often last option
    
    def _find_no_option(self, options: List[str]) -> str:
        """Finds 'No' option or similar"""
        no_keywords = ['no', 'not', 'false', 'negative']
        for option in options:
            if any(keyword in option.lower() for keyword in no_keywords):
                return option
        return options[-1]  # Often last option

# Export main classes
__all__ = ['QuestionClassifier', 'IntelligentResponseGenerator', 'QUESTION_PATTERNS']