"""
Comprehensive Error Recovery System for RapidApply
Handles all types of failures gracefully without stopping execution

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

import time
import traceback
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from modules.helpers import print_lg, critical_error_log

class RecoveryResult:
    """Result of a recovery attempt"""
    def __init__(self, success: bool, continue_to_next: bool = True, 
                 data: Any = None, error: str = None):
        self.success = success
        self.continue_to_next = continue_to_next
        self.data = data
        self.error = error

class ApplicationRecoverySystem:
    """
    Multi-layer recovery system for handling application errors
    Ensures continuous operation despite failures
    """
    
    def __init__(self, driver=None):
        self.driver = driver
        self.recovery_strategies = [
            self.retry_with_different_approach,
            self.skip_optional_questions,
            self.use_minimal_required_info,
            self.refresh_and_retry,
            self.emergency_abort_with_logging
        ]
        self.error_log = []
        self.recovery_stats = {
            'total_errors': 0,
            'recovered': 0,
            'failed': 0,
            'strategies_used': {}
        }
    
    def handle_application_error(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Main entry point for error recovery
        
        Args:
            error_type: Type of error encountered
            context: Error context including element, value, driver, etc.
            
        Returns:
            RecoveryResult indicating success and next action
        """
        print_lg(f"[Recovery] Handling error: {error_type}")
        self.recovery_stats['total_errors'] += 1
        
        # Log error details
        self._log_error(error_type, context)
        
        # Try each recovery strategy
        for i, strategy in enumerate(self.recovery_strategies):
            strategy_name = strategy.__name__
            print_lg(f"[Recovery] Attempting strategy {i+1}: {strategy_name}")
            
            try:
                result = strategy(error_type, context)
                
                if result.success:
                    print_lg(f"[Recovery] Success with strategy: {strategy_name}")
                    self.recovery_stats['recovered'] += 1
                    self.recovery_stats['strategies_used'][strategy_name] = \
                        self.recovery_stats['strategies_used'].get(strategy_name, 0) + 1
                    return result
                    
            except Exception as e:
                print_lg(f"[Recovery] Strategy {strategy_name} failed: {str(e)}")
                continue
        
        # All strategies failed
        self.recovery_stats['failed'] += 1
        self.log_failed_application(context)
        
        # Return result to continue to next job
        return RecoveryResult(success=False, continue_to_next=True, 
                             error="All recovery strategies exhausted")
    
    def retry_with_different_approach(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Strategy 1: Retry the action with alternative methods
        """
        if error_type == "element_not_interactable":
            return self._handle_not_interactable(context)
        elif error_type == "element_not_found":
            return self._handle_element_not_found(context)
        elif error_type == "input_validation_failed":
            return self._handle_input_validation(context)
        elif error_type == "submit_failed":
            return self._handle_submit_failure(context)
        else:
            return RecoveryResult(success=False)
    
    def skip_optional_questions(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Strategy 2: Skip optional questions that are causing issues
        """
        element = context.get('element')
        
        if not element:
            return RecoveryResult(success=False)
        
        try:
            # Check if question is required
            is_required = self._is_element_required(element)
            
            if not is_required:
                print_lg("[Recovery] Skipping optional question")
                # Try to move to next question
                try:
                    element.send_keys(Keys.TAB)
                except:
                    pass
                return RecoveryResult(success=True, data={'skipped': True})
            else:
                # Can't skip required question
                return RecoveryResult(success=False)
                
        except Exception as e:
            print_lg(f"[Recovery] Error checking if optional: {e}")
            return RecoveryResult(success=False)
    
    def use_minimal_required_info(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Strategy 3: Use minimal required information only
        """
        element = context.get('element')
        field_type = context.get('field_type', 'text')
        
        if not element:
            return RecoveryResult(success=False)
        
        try:
            # Provide minimal valid response
            minimal_responses = {
                'text': '1',
                'textarea': 'Yes',
                'email': 'user@example.com',
                'tel': '1234567890',
                'number': '1',
                'url': 'https://linkedin.com'
            }
            
            # Determine input type
            input_type = self._get_input_type(element)
            minimal_value = minimal_responses.get(input_type, 'Yes')
            
            # Try to input minimal value
            self._force_input_value(element, minimal_value)
            
            return RecoveryResult(success=True, data={'minimal_value': minimal_value})
            
        except Exception as e:
            print_lg(f"[Recovery] Minimal info strategy failed: {e}")
            return RecoveryResult(success=False)
    
    def refresh_and_retry(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Strategy 4: Refresh page and retry from current state
        """
        if not self.driver:
            self.driver = context.get('driver')
            
        if not self.driver:
            return RecoveryResult(success=False)
        
        try:
            print_lg("[Recovery] Refreshing page and retrying...")
            
            # Save current URL
            current_url = self.driver.current_url
            
            # Refresh
            self.driver.refresh()
            time.sleep(5)
            
            # Check if we're still on the same page
            if self.driver.current_url != current_url:
                # Navigation changed, might have lost progress
                return RecoveryResult(success=False, continue_to_next=True)
            
            # Try to find and interact with element again
            if 'element_xpath' in context:
                try:
                    new_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, context['element_xpath']))
                    )
                    context['element'] = new_element
                    
                    # Retry original action
                    if 'value' in context:
                        self._force_input_value(new_element, context['value'])
                        
                    return RecoveryResult(success=True, data={'refreshed': True})
                except:
                    pass
                    
            return RecoveryResult(success=False)
            
        except Exception as e:
            print_lg(f"[Recovery] Refresh strategy failed: {e}")
            return RecoveryResult(success=False)
    
    def emergency_abort_with_logging(self, error_type: str, context: Dict[str, Any]) -> RecoveryResult:
        """
        Strategy 5: Emergency abort current application, log everything, continue to next
        """
        print_lg("[Recovery] Emergency abort - logging and moving to next job")
        
        try:
            # Take screenshot if possible
            screenshot_path = self._take_error_screenshot(context)
            
            # Log comprehensive error data
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'error_type': error_type,
                'job_id': context.get('job_id', 'unknown'),
                'company': context.get('company', 'unknown'),
                'screenshot': screenshot_path,
                'context': str(context),
                'full_traceback': traceback.format_exc()
            }
            
            self._save_error_log(error_data)
            
            # Try to navigate back to job listings
            if self.driver:
                try:
                    # Click back button or navigate to jobs page
                    self.driver.back()
                    time.sleep(2)
                except:
                    pass
            
            # Always continue to next job
            return RecoveryResult(
                success=False, 
                continue_to_next=True,
                error="Emergency abort completed",
                data=error_data
            )
            
        except Exception as e:
            print_lg(f"[Recovery] Emergency abort failed: {e}")
            # Even if logging fails, continue to next job
            return RecoveryResult(success=False, continue_to_next=True)
    
    def _handle_not_interactable(self, context: Dict[str, Any]) -> RecoveryResult:
        """Handle element not interactable errors"""
        element = context.get('element')
        value = context.get('value', '')
        
        if not element:
            return RecoveryResult(success=False)
        
        try:
            # Method 1: Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Method 2: JavaScript click
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
            
            # Method 3: JavaScript value setting
            if value:
                self.driver.execute_script(
                    "arguments[0].value = arguments[1]; "
                    "arguments[0].dispatchEvent(new Event('input')); "
                    "arguments[0].dispatchEvent(new Event('change'));",
                    element, value
                )
            
            return RecoveryResult(success=True)
            
        except Exception as e:
            # Method 4: Action chains
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                
                if value:
                    element.send_keys(value)
                    
                return RecoveryResult(success=True)
            except:
                return RecoveryResult(success=False)
    
    def _handle_element_not_found(self, context: Dict[str, Any]) -> RecoveryResult:
        """Handle element not found errors"""
        if not self.driver:
            return RecoveryResult(success=False)
        
        # Try alternative selectors
        alternative_selectors = context.get('alternative_selectors', [])
        
        for selector_type, selector_value in alternative_selectors:
            try:
                element = self.driver.find_element(selector_type, selector_value)
                context['element'] = element
                return RecoveryResult(success=True, data={'element': element})
            except:
                continue
        
        # Try waiting longer
        try:
            if 'original_selector' in context:
                element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(context['original_selector'])
                )
                context['element'] = element
                return RecoveryResult(success=True, data={'element': element})
        except:
            pass
            
        return RecoveryResult(success=False)
    
    def _handle_input_validation(self, context: Dict[str, Any]) -> RecoveryResult:
        """Handle input validation failures"""
        element = context.get('element')
        value = context.get('value', '')
        validation_type = context.get('validation_type')
        
        if not element:
            return RecoveryResult(success=False)
        
        try:
            # Clean and reformat value based on validation type
            if validation_type == 'numeric':
                # Extract only numbers
                cleaned_value = ''.join(filter(str.isdigit, str(value)))
            elif validation_type == 'email':
                # Ensure valid email format
                if '@' not in value:
                    cleaned_value = 'user@example.com'
                else:
                    cleaned_value = value.strip()
            elif validation_type == 'phone':
                # Extract only numbers
                cleaned_value = ''.join(filter(str.isdigit, str(value)))
                if len(cleaned_value) < 10:
                    cleaned_value = '1234567890'
            else:
                cleaned_value = str(value).strip()
            
            # Clear and re-enter
            element.clear()
            time.sleep(0.5)
            element.send_keys(cleaned_value)
            
            return RecoveryResult(success=True, data={'cleaned_value': cleaned_value})
            
        except Exception as e:
            print_lg(f"[Recovery] Input validation handling failed: {e}")
            return RecoveryResult(success=False)
    
    def _handle_submit_failure(self, context: Dict[str, Any]) -> RecoveryResult:
        """Handle form submission failures"""
        if not self.driver:
            return RecoveryResult(success=False)
        
        try:
            # Method 1: Find and click alternative submit button
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Apply')]",
                "//button[contains(text(), 'Send')]",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(text(), 'Next')]",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(By.XPATH, selector)
                    submit_btn.click()
                    time.sleep(2)
                    
                    # Check if submission worked
                    if self._check_submission_success():
                        return RecoveryResult(success=True)
                except:
                    continue
            
            # Method 2: Submit form via JavaScript
            try:
                self.driver.execute_script(
                    "document.querySelector('form').submit();"
                )
                time.sleep(2)
                
                if self._check_submission_success():
                    return RecoveryResult(success=True)
            except:
                pass
            
            # Method 3: Press Enter on last field
            try:
                last_input = self.driver.find_elements(By.TAG_NAME, "input")[-1]
                last_input.send_keys(Keys.RETURN)
                time.sleep(2)
                
                if self._check_submission_success():
                    return RecoveryResult(success=True)
            except:
                pass
                
            return RecoveryResult(success=False)
            
        except Exception as e:
            print_lg(f"[Recovery] Submit failure handling failed: {e}")
            return RecoveryResult(success=False)
    
    def _is_element_required(self, element: WebElement) -> bool:
        """Check if an element is required"""
        try:
            # Check various indicators of required fields
            required_indicators = [
                element.get_attribute('required') is not None,
                element.get_attribute('aria-required') == 'true',
                '*' in element.find_element(By.XPATH, "./..").text,
                'required' in element.find_element(By.XPATH, "./..").text.lower()
            ]
            
            return any(required_indicators)
        except:
            # Assume required if we can't determine
            return True
    
    def _get_input_type(self, element: WebElement) -> str:
        """Determine the type of input element"""
        try:
            tag_name = element.tag_name.lower()
            
            if tag_name == 'input':
                return element.get_attribute('type') or 'text'
            elif tag_name == 'textarea':
                return 'textarea'
            elif tag_name == 'select':
                return 'select'
            else:
                return 'text'
        except:
            return 'text'
    
    def _force_input_value(self, element: WebElement, value: str):
        """Force input value using multiple methods"""
        # Method 1: Standard clear and send keys
        try:
            element.clear()
            element.send_keys(value)
            return
        except:
            pass
        
        # Method 2: JavaScript
        try:
            self.driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input'));"
                "arguments[0].dispatchEvent(new Event('change'));",
                element, value
            )
            return
        except:
            pass
        
        # Method 3: Select all and replace
        try:
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(value)
            return
        except:
            pass
        
        raise Exception("All input methods failed")
    
    def _take_error_screenshot(self, context: Dict[str, Any]) -> Optional[str]:
        """Take screenshot of error state"""
        try:
            if not self.driver:
                self.driver = context.get('driver')
                
            if self.driver:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"error_{context.get('error_type', 'unknown')}_{timestamp}.png"
                filepath = f"logs/errors/{filename}"
                
                # Ensure directory exists
                import os
                os.makedirs("logs/errors", exist_ok=True)
                
                # Take screenshot
                self.driver.save_screenshot(filepath)
                
                return filepath
        except Exception as e:
            print_lg(f"[Recovery] Screenshot failed: {e}")
            
        return None
    
    def _check_submission_success(self) -> bool:
        """Check if form submission was successful"""
        try:
            # Check for common success indicators
            success_indicators = [
                "success",
                "thank you",
                "application submitted",
                "received your application",
                "complete",
                "confirmation"
            ]
            
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            
            return any(indicator in page_text for indicator in success_indicators)
        except:
            return False
    
    def _log_error(self, error_type: str, context: Dict[str, Any]):
        """Log error details for analysis"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'context': {
                'job_id': context.get('job_id'),
                'company': context.get('company'),
                'question': context.get('question_text'),
                'field_type': context.get('field_type')
            },
            'traceback': traceback.format_exc()
        }
        
        self.error_log.append(error_entry)
    
    def _save_error_log(self, error_data: Dict[str, Any]):
        """Save error log to file"""
        try:
            import json
            import os
            
            # Ensure directory exists
            os.makedirs("logs/errors", exist_ok=True)
            
            # Save to daily log file
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = f"logs/errors/errors_{date_str}.json"
            
            # Load existing or create new
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Append new error
            logs.append(error_data)
            
            # Save back
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print_lg(f"[Recovery] Failed to save error log: {e}")
    
    def log_failed_application(self, context: Dict[str, Any]):
        """Log details of failed application for manual review"""
        try:
            failed_app = {
                'timestamp': datetime.now().isoformat(),
                'job_id': context.get('job_id', 'unknown'),
                'company': context.get('company', 'unknown'),
                'position': context.get('position', 'unknown'),
                'url': context.get('url', 'unknown'),
                'error_summary': context.get('error_type', 'unknown'),
                'recovery_attempts': len(self.recovery_strategies)
            }
            
            # Save to failed applications log
            import json
            import os
            
            os.makedirs("logs", exist_ok=True)
            log_file = "logs/failed_applications.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    failed_apps = json.load(f)
            else:
                failed_apps = []
            
            failed_apps.append(failed_app)
            
            with open(log_file, 'w') as f:
                json.dump(failed_apps, f, indent=2)
                
        except Exception as e:
            print_lg(f"[Recovery] Failed to log application: {e}")
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """Get recovery system statistics"""
        return {
            'total_errors': self.recovery_stats['total_errors'],
            'recovered': self.recovery_stats['recovered'],
            'failed': self.recovery_stats['failed'],
            'recovery_rate': (
                self.recovery_stats['recovered'] / 
                max(self.recovery_stats['total_errors'], 1) * 100
            ),
            'strategies_used': self.recovery_stats['strategies_used'],
            'error_log_size': len(self.error_log)
        }

# Global recovery system instance
recovery_system = ApplicationRecoverySystem()

# Export
__all__ = ['ApplicationRecoverySystem', 'RecoveryResult', 'recovery_system']