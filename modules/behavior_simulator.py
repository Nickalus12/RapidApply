"""
LinkedIn Behavior Simulator for Anti-Detection
Implements human-like behavior patterns to avoid bot detection

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import json
import os

from selenium.webdriver.common.keys import Keys
from modules.helpers import print_lg

class LinkedInBehaviorSimulator:
    """
    Simulates human-like behavior patterns for LinkedIn automation
    Includes timing, rate limiting, and activity patterns
    """
    
    def __init__(self, config_file: str = "behavior_stats.json"):
        self.session_start = time.time()
        self.last_action_time = time.time()
        self.actions_this_hour = 0
        self.actions_this_session = 0
        self.daily_applications = 0
        self.session_applications = 0
        self.hour_start = datetime.now()
        self.config_file = config_file
        self.stats = self._load_stats()
        self.behavior_profile = self._generate_behavior_profile()
        
    def _load_stats(self) -> Dict:
        """Load persistent statistics from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    stats = json.load(f)
                    # Check if stats are from today
                    last_date = datetime.fromisoformat(stats.get('last_update', '2020-01-01'))
                    if last_date.date() != datetime.now().date():
                        # Reset daily counters
                        stats['daily_applications'] = 0
                        stats['daily_actions'] = 0
                    return stats
            except:
                pass
        
        # Default stats
        return {
            'total_applications': 0,
            'daily_applications': 0,
            'daily_actions': 0,
            'last_update': datetime.now().isoformat(),
            'avg_time_per_application': 240,  # 4 minutes average
            'detection_events': 0
        }
    
    def _save_stats(self):
        """Save statistics to file"""
        self.stats['last_update'] = datetime.now().isoformat()
        self.stats['daily_applications'] = self.daily_applications
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print_lg(f"Failed to save behavior stats: {e}")
    
    def _generate_behavior_profile(self) -> Dict:
        """Generate a random but consistent behavior profile for this session"""
        return {
            'typing_speed': random.uniform(0.08, 0.15),  # Seconds between keystrokes
            'reading_speed': random.uniform(0.2, 0.4),   # Seconds per word
            'decision_time': random.uniform(2, 5),       # Base decision time
            'fatigue_rate': random.uniform(0.2, 0.4),    # How quickly user gets tired
            'break_probability': random.uniform(0.1, 0.2), # Chance of taking breaks
            'scroll_behavior': random.choice(['smooth', 'chunky', 'mixed']),
            'mouse_precision': random.uniform(0.8, 0.95)  # How accurately user clicks
        }
    
    def smart_delay(self, action_type: str = "default", context: Dict = None) -> float:
        """
        Implements intelligent delays mimicking human behavior
        
        Args:
            action_type: Type of action being performed
            context: Additional context (e.g., text length, complexity)
            
        Returns:
            Actual delay time applied
        """
        # Base delays for different actions
        delays = {
            'page_load': (2, 5),
            'question_read': (1, 4),
            'question_answer': (2, 8),
            'typing': (0.05, 0.15),
            'form_submit': (3, 12),
            'job_click': (1, 5),
            'scroll': (0.5, 2),
            'mouse_move': (0.1, 0.5),
            'button_click': (0.5, 2),
            'page_navigation': (1, 3),
            'thinking': (1, 5),
            'reviewing': (5, 15),
            'default': (1, 3)
        }
        
        min_delay, max_delay = delays.get(action_type, delays['default'])
        
        # Adjust for context
        if context:
            # Longer delays for longer text
            if 'text_length' in context:
                text_factor = min(context['text_length'] / 100, 2)  # Cap at 2x
                min_delay *= (1 + text_factor * 0.3)
                max_delay *= (1 + text_factor * 0.5)
            
            # Longer delays for complex questions
            if 'complexity' in context:
                complexity_factor = context['complexity']  # 0-1 scale
                min_delay *= (1 + complexity_factor)
                max_delay *= (1 + complexity_factor * 1.5)
        
        # Time of day adjustments
        hour = datetime.now().hour
        if 22 <= hour or hour <= 6:  # Late night/early morning
            min_delay *= 1.5
            max_delay *= 2.0
            print_lg("[Behavior] Late night - increasing delays")
        elif 12 <= hour <= 14:  # Lunch time
            min_delay *= 1.2
            max_delay *= 1.4
        
        # Session fatigue (get slower over time)
        session_duration = (time.time() - self.session_start) / 3600  # Hours
        fatigue_multiplier = 1 + (session_duration * self.behavior_profile['fatigue_rate'])
        
        # Random micro-pauses (human hesitation)
        if random.random() < 0.1:  # 10% chance
            min_delay += random.uniform(0.5, 2)
            max_delay += random.uniform(1, 3)
            print_lg("[Behavior] Adding micro-pause (hesitation)")
        
        # Calculate final delay
        base_delay = random.uniform(min_delay, max_delay)
        final_delay = base_delay * fatigue_multiplier
        
        # Add random variation (humans aren't perfectly consistent)
        variation = random.uniform(0.9, 1.1)
        final_delay *= variation
        
        # Actual sleep
        time.sleep(final_delay)
        
        # Update tracking
        self.last_action_time = time.time()
        self.actions_this_session += 1
        
        print_lg(f"[Behavior] {action_type} delay: {final_delay:.2f}s (fatigue: {fatigue_multiplier:.2f}x)")
        
        return final_delay
    
    def check_rate_limits(self) -> bool:
        """
        Enforces safe application rates to avoid detection
        
        Returns:
            True if safe to continue, False if should stop
        """
        current_time = time.time()
        current_hour = datetime.now()
        
        # Update hourly counter if new hour
        if current_hour.hour != self.hour_start.hour:
            self.actions_this_hour = 0
            self.hour_start = current_hour
        
        # Check daily limit (100 applications)
        if self.daily_applications >= 100:
            print_lg("[Behavior] Daily limit reached (100 applications). Stopping.")
            self._save_stats()
            return False
        
        # Check hourly limit (15 applications)
        if self.actions_this_hour >= 15:
            print_lg("[Behavior] Hourly limit reached. Taking a break...")
            break_time = random.uniform(300, 600)  # 5-10 minute break
            self._take_break(break_time)
            self.actions_this_hour = 0
            return True
        
        # Check session limit (50 applications per session)
        if self.session_applications >= 50:
            print_lg("[Behavior] Session limit reached. Consider taking a long break.")
            self._save_stats()
            return False
        
        # Minimum time between applications (3-6 minutes)
        time_since_last = current_time - self.last_action_time
        min_interval = random.uniform(180, 360)  # 3-6 minutes
        
        if time_since_last < min_interval:
            wait_time = min_interval - time_since_last
            print_lg(f"[Behavior] Rate limiting: waiting {wait_time:.1f}s before next application")
            time.sleep(wait_time)
        
        # Random longer breaks (human behavior)
        if random.random() < self.behavior_profile['break_probability']:
            break_time = random.uniform(60, 300)  # 1-5 minute random break
            print_lg(f"[Behavior] Taking random break for {break_time:.1f}s")
            self._take_break(break_time)
        
        return True
    
    def record_application(self):
        """Records that an application was submitted"""
        self.daily_applications += 1
        self.session_applications += 1
        self.actions_this_hour += 1
        self.stats['total_applications'] += 1
        self.stats['daily_applications'] = self.daily_applications
        
        # Update average time
        session_time = time.time() - self.session_start
        avg_time = session_time / max(self.session_applications, 1)
        self.stats['avg_time_per_application'] = (
            self.stats['avg_time_per_application'] * 0.9 + avg_time * 0.1
        )
        
        print_lg(f"[Behavior] Application recorded. Daily: {self.daily_applications}, "
                f"Session: {self.session_applications}, Total: {self.stats['total_applications']}")
        
        # Save stats periodically
        if self.session_applications % 10 == 0:
            self._save_stats()
    
    def simulate_mouse_movement(self, start_pos: Tuple[int, int], 
                               end_pos: Tuple[int, int], 
                               driver) -> None:
        """
        Simulates human-like mouse movement between two points
        
        Args:
            start_pos: Starting (x, y) coordinates
            end_pos: Ending (x, y) coordinates
            driver: Selenium WebDriver instance
        """
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(driver)
            
            # Calculate distance
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            # Number of intermediate points based on distance
            steps = max(int(distance / 50), 5)  # At least 5 steps
            
            # Generate curved path (not straight line)
            curve_factor = random.uniform(-0.2, 0.2)
            
            for i in range(steps + 1):
                progress = i / steps
                
                # Add curve to path
                curve = curve_factor * math.sin(progress * math.pi)
                
                # Calculate position with curve and random jitter
                x = start_pos[0] + dx * progress + curve * dy
                y = start_pos[1] + dy * progress - curve * dx
                
                # Add small random jitter (hand tremor)
                if self.behavior_profile['mouse_precision'] < 0.95:
                    jitter = (1 - self.behavior_profile['mouse_precision']) * 5
                    x += random.uniform(-jitter, jitter)
                    y += random.uniform(-jitter, jitter)
                
                actions.move_by_offset(int(x), int(y))
                
                # Small delay between movements
                time.sleep(random.uniform(0.01, 0.03))
            
            actions.perform()
            
        except Exception as e:
            print_lg(f"[Behavior] Mouse simulation failed: {e}")
    
    def simulate_scrolling(self, driver, direction: str = "down", amount: int = None):
        """
        Simulates human-like scrolling behavior
        
        Args:
            driver: Selenium WebDriver instance
            direction: 'up' or 'down'
            amount: Pixels to scroll (None for random)
        """
        if amount is None:
            amount = random.randint(100, 500)
        
        scroll_type = self.behavior_profile['scroll_behavior']
        
        if scroll_type == 'smooth' or (scroll_type == 'mixed' and random.random() < 0.5):
            # Smooth scrolling
            steps = random.randint(5, 10)
            step_size = amount / steps
            
            for _ in range(steps):
                scroll_amount = step_size * (1 if direction == 'down' else -1)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.05, 0.1))
        else:
            # Chunky scrolling
            chunks = random.randint(1, 3)
            for _ in range(chunks):
                chunk_size = amount / chunks * (1 if direction == 'down' else -1)
                driver.execute_script(f"window.scrollBy(0, {chunk_size});")
                if chunks > 1:
                    time.sleep(random.uniform(0.2, 0.5))
    
    def simulate_typing(self, element, text: str, clear_first: bool = True):
        """
        Simulates human-like typing with variable speed and occasional corrections
        
        Args:
            element: Selenium WebElement to type into
            text: Text to type
            clear_first: Whether to clear existing text first
        """
        if clear_first:
            element.clear()
            time.sleep(random.uniform(0.1, 0.3))
        
        # Typing patterns
        typing_speed = self.behavior_profile['typing_speed']
        error_rate = 0.02  # 2% chance of typo
        
        for i, char in enumerate(text):
            # Occasional typos
            if random.random() < error_rate and i < len(text) - 1:
                # Make a typo
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(typing_speed * random.uniform(0.5, 1.5))
                
                # Correct it
                element.send_keys(Keys.BACKSPACE)
                time.sleep(typing_speed * random.uniform(0.5, 1.5))
            
            # Type the character
            element.send_keys(char)
            
            # Variable typing speed
            delay = typing_speed * random.uniform(0.5, 1.5)
            
            # Longer pauses after punctuation
            if char in '.,!?;:':
                delay *= random.uniform(1.5, 2.5)
            
            # Occasional thinking pauses
            if random.random() < 0.05:  # 5% chance
                delay += random.uniform(0.5, 2.0)
            
            time.sleep(delay)
    
    def _take_break(self, duration: float):
        """Simulates taking a break with random micro-activities"""
        print_lg(f"[Behavior] Taking break for {duration:.1f}s")
        
        break_end = time.time() + duration
        
        while time.time() < break_end:
            # Simulate random micro-activities during break
            activity_duration = random.uniform(10, 30)
            
            if random.random() < 0.3:  # 30% chance
                print_lg("[Behavior] Simulating idle time...")
            
            time.sleep(min(activity_duration, break_end - time.time()))
    
    def detect_anti_bot_challenge(self, driver) -> bool:
        """
        Checks for common anti-bot challenges or warnings
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            True if challenge detected, False otherwise
        """
        challenge_indicators = [
            "verify you're human",
            "suspicious activity",
            "rate limit",
            "too many requests",
            "please slow down",
            "security check",
            "verify your identity",
            "unusual activity",
            "temporary restriction"
        ]
        
        try:
            page_text = driver.find_element_by_tag_name('body').text.lower()
            
            for indicator in challenge_indicators:
                if indicator in page_text:
                    print_lg(f"[Behavior] Anti-bot challenge detected: '{indicator}'")
                    self.stats['detection_events'] += 1
                    self._save_stats()
                    return True
                    
        except Exception as e:
            print_lg(f"[Behavior] Error checking for anti-bot: {e}")
        
        return False
    
    def handle_detection(self, driver) -> bool:
        """
        Handles anti-bot detection with appropriate response
        
        Returns:
            True if handled successfully, False if should abort
        """
        print_lg("[Behavior] Handling bot detection...")
        
        # Take a long break
        break_time = random.uniform(1800, 3600)  # 30-60 minutes
        print_lg(f"[Behavior] Taking extended break for {break_time/60:.1f} minutes")
        
        self._take_break(break_time)
        
        # Clear cookies to get fresh session
        try:
            driver.delete_all_cookies()
            driver.refresh()
            time.sleep(10)
        except:
            pass
        
        # Reset session counters
        self.session_applications = 0
        self.actions_this_hour = 0
        self.session_start = time.time()
        
        return True

# Create global instance
behavior_simulator = LinkedInBehaviorSimulator()

# Export
__all__ = ['LinkedInBehaviorSimulator', 'behavior_simulator']