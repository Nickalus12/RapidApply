"""
Smart Resume Selection System using Grok AI
Intelligently selects the best resume variant for each job application

Author:     RapidApply Contributors
GitHub:     https://github.com/Nickalus12/RapidApply
License:    GNU Affero General Public License
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

from modules.helpers import print_lg
from modules.ai.grokConnections import grok_answer_question
from modules.resumes.extractor import extract_text_from_pdf, extract_text_from_docx
from config.secrets import use_AI, ai_provider, use_grok_for_openai

class SmartResumeSelector:
    """
    Uses Grok AI to intelligently select the best resume for each job application
    Analyzes job requirements and matches them with available resume variants
    """
    
    def __init__(self, ai_client=None, resume_folder: str = "resumes"):
        self.ai_client = ai_client
        self.resume_folder = resume_folder
        self.resume_cache = {}
        self.selection_cache = {}
        self.selection_history = []
        self._ensure_resume_folder()
        
    def _ensure_resume_folder(self):
        """Ensures the resume folder exists"""
        if not os.path.exists(self.resume_folder):
            os.makedirs(self.resume_folder)
            print_lg(f"[Resume Selector] Created resume folder: {self.resume_folder}")
            
            # Create subfolders for organization
            subfolders = ['technical', 'management', 'general', 'custom']
            for subfolder in subfolders:
                os.makedirs(os.path.join(self.resume_folder, subfolder), exist_ok=True)
    
    def load_available_resumes(self) -> Dict[str, Dict[str, str]]:
        """
        Loads all available resumes from the resume folder
        
        Returns:
            Dict mapping resume names to their metadata and content
        """
        resumes = {}
        
        # Scan resume folder and subfolders
        for root, dirs, files in os.walk(self.resume_folder):
            for file in files:
                if file.endswith(('.pdf', '.docx')):
                    file_path = os.path.join(root, file)
                    resume_name = os.path.splitext(file)[0]
                    
                    # Check cache first
                    cache_key = f"{file_path}_{os.path.getmtime(file_path)}"
                    if cache_key in self.resume_cache:
                        resumes[resume_name] = self.resume_cache[cache_key]
                        continue
                    
                    # Extract text content
                    try:
                        if file.endswith('.pdf'):
                            content = extract_text_from_pdf(file_path)
                        else:
                            content = extract_text_from_docx(file_path)
                        
                        # Extract metadata from filename or content
                        metadata = self._extract_resume_metadata(resume_name, content)
                        
                        resume_data = {
                            'path': file_path,
                            'name': resume_name,
                            'content': content[:5000],  # First 5000 chars for analysis
                            'full_content': content,
                            'metadata': metadata,
                            'category': os.path.basename(root)
                        }
                        
                        resumes[resume_name] = resume_data
                        self.resume_cache[cache_key] = resume_data
                        
                    except Exception as e:
                        print_lg(f"[Resume Selector] Error loading {file}: {str(e)}")
        
        print_lg(f"[Resume Selector] Loaded {len(resumes)} resumes")
        return resumes
    
    def select_best_resume(self, 
                          job_description: str,
                          company_name: str = "",
                          job_title: str = "",
                          required_skills: List[str] = None,
                          preferred_skills: List[str] = None) -> Tuple[str, Dict[str, str]]:
        """
        Selects the best resume for a given job using Grok AI
        
        Args:
            job_description: Full job description text
            company_name: Name of the company
            job_title: Job title/position
            required_skills: List of required skills
            preferred_skills: List of preferred skills
            
        Returns:
            Tuple of (resume_path, selection_reasoning)
        """
        # Load available resumes
        available_resumes = self.load_available_resumes()
        
        if not available_resumes:
            print_lg("[Resume Selector] No resumes found, using default")
            return self._get_default_resume()
        
        # Single resume shortcut
        if len(available_resumes) == 1:
            resume_name = list(available_resumes.keys())[0]
            return available_resumes[resume_name]['path'], {
                'selected_resume': resume_name,
                'reason': 'Only one resume available',
                'confidence': 1.0
            }
        
        # Check cache
        cache_key = self._generate_cache_key(job_description, company_name, job_title)
        if cache_key in self.selection_cache:
            cached = self.selection_cache[cache_key]
            print_lg(f"[Resume Selector] Using cached selection: {cached['selected_resume']}")
            return available_resumes[cached['selected_resume']]['path'], cached
        
        # Use AI to select best resume
        if use_AI and self.ai_client:
            selection = self._ai_select_resume(
                available_resumes,
                job_description,
                company_name,
                job_title,
                required_skills,
                preferred_skills
            )
        else:
            # Fallback to rule-based selection
            selection = self._rule_based_selection(
                available_resumes,
                job_description,
                job_title,
                required_skills
            )
        
        # Cache the selection
        self.selection_cache[cache_key] = selection
        
        # Log selection history
        self._log_selection(selection, job_title, company_name)
        
        selected_resume_name = selection['selected_resume']
        return available_resumes[selected_resume_name]['path'], selection
    
    def _ai_select_resume(self,
                         resumes: Dict[str, Dict],
                         job_description: str,
                         company_name: str,
                         job_title: str,
                         required_skills: List[str],
                         preferred_skills: List[str]) -> Dict[str, any]:
        """Uses Grok AI to intelligently select the best resume"""
        
        # Prepare resume summaries for AI
        resume_summaries = []
        for name, data in resumes.items():
            summary = f"""
Resume: {name}
Category: {data['category']}
Key Skills: {', '.join(data['metadata'].get('skills', [])[:10])}
Experience Level: {data['metadata'].get('experience_level', 'Unknown')}
Focus Areas: {', '.join(data['metadata'].get('focus_areas', []))}
Preview: {data['content'][:500]}...
"""
            resume_summaries.append(summary)
        
        # Build the selection prompt
        prompt = f"""
TASK: Select the best resume for this job application

JOB DETAILS:
- Company: {company_name}
- Position: {job_title}
- Required Skills: {', '.join(required_skills or [])}
- Preferred Skills: {', '.join(preferred_skills or [])}

JOB DESCRIPTION:
{job_description[:1500]}

AVAILABLE RESUMES:
{chr(10).join(resume_summaries)}

INSTRUCTIONS:
1. Analyze the job requirements carefully
2. Match required skills with resume content
3. Consider the job level and focus area
4. Select the resume that best highlights relevant experience

Return ONLY the resume name (e.g., "technical_backend_engineer" or "management_tech_lead").

SELECTED RESUME:"""

        try:
            if ai_provider.lower() == "grok" or use_grok_for_openai:
                # Use Grok to select resume
                response = grok_answer_question(
                    self.ai_client,
                    prompt,
                    question_type='text',
                    stream=False
                )
                
                selected_name = response.strip().strip('"').strip("'")
                
                # Validate selection
                if selected_name not in resumes:
                    # Try to find closest match
                    for resume_name in resumes.keys():
                        if selected_name.lower() in resume_name.lower():
                            selected_name = resume_name
                            break
                    else:
                        # Fallback to rule-based
                        return self._rule_based_selection(resumes, job_description, job_title, required_skills)
                
                # Get reasoning
                reasoning_prompt = f"""
Explain why {selected_name} is the best resume for the {job_title} position at {company_name}.
Focus on skill matches and relevant experience. Keep it under 100 words.
"""
                
                reasoning = grok_answer_question(
                    self.ai_client,
                    reasoning_prompt,
                    question_type='text',
                    stream=False
                )
                
                return {
                    'selected_resume': selected_name,
                    'reason': reasoning,
                    'confidence': 0.85,
                    'method': 'ai_selection'
                }
                
        except Exception as e:
            print_lg(f"[Resume Selector] AI selection failed: {str(e)}")
            return self._rule_based_selection(resumes, job_description, job_title, required_skills)
    
    def _rule_based_selection(self,
                             resumes: Dict[str, Dict],
                             job_description: str,
                             job_title: str,
                             required_skills: List[str]) -> Dict[str, any]:
        """Fallback rule-based resume selection"""
        
        scores = {}
        job_desc_lower = job_description.lower()
        job_title_lower = job_title.lower()
        
        for name, data in resumes.items():
            score = 0
            content_lower = data['full_content'].lower()
            
            # Category matching
            if 'senior' in job_title_lower or 'lead' in job_title_lower:
                if data['category'] == 'management':
                    score += 20
            elif 'engineer' in job_title_lower or 'developer' in job_title_lower:
                if data['category'] == 'technical':
                    score += 20
            
            # Skill matching
            if required_skills:
                for skill in required_skills:
                    if skill.lower() in content_lower:
                        score += 10
            
            # Keyword matching from job description
            important_keywords = self._extract_keywords(job_description)
            for keyword in important_keywords:
                if keyword.lower() in content_lower:
                    score += 5
            
            # Title matching
            if job_title_lower in content_lower:
                score += 15
            
            # Experience level matching
            exp_level = data['metadata'].get('experience_level', 'mid')
            if 'senior' in job_title_lower and exp_level == 'senior':
                score += 10
            elif 'junior' in job_title_lower and exp_level == 'junior':
                score += 10
            
            scores[name] = score
        
        # Select highest scoring resume
        best_resume = max(scores, key=scores.get)
        
        return {
            'selected_resume': best_resume,
            'reason': f"Best match based on {scores[best_resume]} scoring points from skill and keyword matching",
            'confidence': min(scores[best_resume] / 100, 0.95),
            'method': 'rule_based',
            'scores': scores
        }
    
    def _extract_resume_metadata(self, resume_name: str, content: str) -> Dict[str, any]:
        """Extracts metadata from resume content"""
        metadata = {
            'skills': [],
            'experience_level': 'mid',
            'focus_areas': []
        }
        
        # Extract skills (common technical terms)
        skill_patterns = [
            'python', 'java', 'javascript', 'react', 'node.js', 'aws', 'docker',
            'kubernetes', 'sql', 'mongodb', 'machine learning', 'ai', 'data science',
            'project management', 'agile', 'scrum', 'leadership', 'communication'
        ]
        
        content_lower = content.lower()
        for skill in skill_patterns:
            if skill in content_lower:
                metadata['skills'].append(skill)
        
        # Determine experience level
        if any(term in content_lower for term in ['senior', 'lead', 'principal', 'manager', 'director']):
            metadata['experience_level'] = 'senior'
        elif any(term in content_lower for term in ['junior', 'entry', 'graduate', 'intern']):
            metadata['experience_level'] = 'junior'
        
        # Determine focus areas
        if 'manage' in content_lower or 'lead' in content_lower:
            metadata['focus_areas'].append('management')
        if 'develop' in content_lower or 'engineer' in content_lower:
            metadata['focus_areas'].append('technical')
        if 'design' in content_lower or 'architect' in content_lower:
            metadata['focus_areas'].append('architecture')
        
        return metadata
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extracts important keywords from text"""
        # Simple keyword extraction based on frequency
        words = text.lower().split()
        
        # Filter common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                       'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                       'before', 'after', 'above', 'below', 'between', 'under', 'is', 'are',
                       'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
                       'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
                       'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
                       'we', 'they', 'them', 'their', 'what', 'which', 'who', 'when', 'where',
                       'why', 'how', 'all', 'each', 'every', 'some', 'any', 'few', 'many'}
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word = word.strip('.,!?;:"')
            if len(word) > 3 and word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
    
    def _generate_cache_key(self, job_desc: str, company: str, title: str) -> str:
        """Generates a cache key for resume selection"""
        content = f"{company}_{title}_{job_desc[:500]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_default_resume(self) -> Tuple[str, Dict[str, str]]:
        """Returns default resume when no selection can be made"""
        default_path = os.path.join(self.resume_folder, "default_resume.pdf")
        return default_path, {
            'selected_resume': 'default',
            'reason': 'No resumes available for selection',
            'confidence': 0.5,
            'method': 'default'
        }
    
    def _log_selection(self, selection: Dict, job_title: str, company: str):
        """Logs resume selection for analytics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'job_title': job_title,
            'company': company,
            'selected_resume': selection['selected_resume'],
            'confidence': selection['confidence'],
            'method': selection['method']
        }
        
        self.selection_history.append(log_entry)
        
        # Save to file periodically
        if len(self.selection_history) % 10 == 0:
            self._save_selection_history()
    
    def _save_selection_history(self):
        """Saves selection history to file"""
        try:
            history_file = os.path.join(self.resume_folder, "selection_history.json")
            with open(history_file, 'w') as f:
                json.dump(self.selection_history, f, indent=2)
        except Exception as e:
            print_lg(f"[Resume Selector] Failed to save history: {e}")
    
    def get_selection_stats(self) -> Dict[str, any]:
        """Returns statistics about resume selections"""
        if not self.selection_history:
            return {}
        
        stats = {
            'total_selections': len(self.selection_history),
            'resume_usage': {},
            'average_confidence': 0,
            'method_distribution': {}
        }
        
        total_confidence = 0
        for entry in self.selection_history:
            # Resume usage
            resume = entry['selected_resume']
            stats['resume_usage'][resume] = stats['resume_usage'].get(resume, 0) + 1
            
            # Confidence
            total_confidence += entry['confidence']
            
            # Method distribution
            method = entry['method']
            stats['method_distribution'][method] = stats['method_distribution'].get(method, 0) + 1
        
        stats['average_confidence'] = total_confidence / len(self.selection_history)
        
        return stats

# Export
__all__ = ['SmartResumeSelector']