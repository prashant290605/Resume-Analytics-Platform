from typing import Dict, List, Any, Tuple
from utils.embeddings import EmbeddingUtil
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MatcherAgent:
    """Agent to match job descriptions with resumes using embeddings"""
    
    def __init__(self):
        """Initialize Matcher Agent"""
        self.embedding_util = EmbeddingUtil()
    
    def calculate_match_score(self, jd_data: Dict[str, Any], cv_data: Dict[str, Any]) -> float:
        """Calculate match score between job description and resume
        
        Args:
            jd_data: Job description data
            cv_data: Resume data
            
        Returns:
            Match score (0-100)
        """
        try:
            # Get embeddings
            jd_embedding = self.embedding_util.get_jd_embedding(jd_data)
            cv_embedding = self.embedding_util.get_cv_embedding(cv_data)
            
            # Calculate similarity
            score = self.embedding_util.calculate_similarity(jd_embedding, cv_embedding)
            
            return score
        except Exception as e:
            # Use fallback scoring without embeddings
            return self._keyword_based_scoring(jd_data, cv_data)
    
    def _keyword_based_scoring(self, jd_data: Dict[str, Any], cv_data: Dict[str, Any]) -> float:
        """Fallback keyword-based scoring when embeddings are not available"""
        # Extract job requirements
        jd_skills = []
        if isinstance(jd_data, dict) and 'summary' in jd_data and 'required_skills' in jd_data['summary']:
            skills = jd_data['summary']['required_skills']
            if isinstance(skills, list):
                jd_skills = [s.lower().strip() for s in skills]
            elif isinstance(skills, str):
                jd_skills = [s.strip().lower() for s in skills.split(',')]
        
        # Extract candidate skills
        cv_skills = []
        if isinstance(cv_data, dict) and 'skills' in cv_data:
            skills = cv_data['skills']
            if isinstance(skills, list):
                cv_skills = [s.lower().strip() for s in skills]
            elif isinstance(skills, str):
                cv_skills = [s.strip().lower() for s in skills.split(',')]
        
        # Calculate skill match score
        if not jd_skills:
            return 60.0  # Default score when no job skills specified
        
        matching_skills = 0
        for jd_skill in jd_skills:
            for cv_skill in cv_skills:
                if jd_skill in cv_skill or cv_skill in jd_skill:
                    matching_skills += 1
                    break
        
        # Base score from skill matching
        skill_score = (matching_skills / len(jd_skills)) * 100
        
        # Add bonus for experience keywords
        experience_keywords = ['year', 'experience', 'senior', 'lead', 'manager', 'director']
        cv_text = str(cv_data.get('work_experience', '')).lower()
        experience_bonus = sum(5 for keyword in experience_keywords if keyword in cv_text)
        
        # Add bonus for education keywords
        education_keywords = ['degree', 'bachelor', 'master', 'phd', 'university', 'college']
        cv_education = str(cv_data.get('education', '')).lower()
        education_bonus = sum(3 for keyword in education_keywords if keyword in cv_education)
        
        # Calculate final score
        final_score = min(100, skill_score + experience_bonus + education_bonus)
        
        # Add some randomness for variety
        import random
        final_score += random.uniform(-5, 5)
        
        return max(0, min(100, final_score))
    
    def match_jd_with_all_cvs(self, jd_data: Dict[str, Any], cv_data_list: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], float]]:
        """Match a job description with all resumes
        
        Args:
            jd_data: Job description data
            cv_data_list: List of resume data
            
        Returns:
            List of tuples containing CV data and match score, sorted by score
        """
        matches = []
        
        for cv_data in cv_data_list:
            score = self.calculate_match_score(jd_data, cv_data)
            matches.append((cv_data, score))
        
        # Sort by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
    
    def match_all_jds_with_all_cvs(self, jd_data_list: List[Dict[str, Any]], cv_data_list: List[Dict[str, Any]]) -> Dict[str, List[Tuple[Dict[str, Any], float]]]:
        """Match all job descriptions with all resumes
        
        Args:
            jd_data_list: List of job description data
            cv_data_list: List of resume data
            
        Returns:
            Dictionary mapping job title to list of (CV, score) tuples
        """
        all_matches = {}
        
        for jd_data in jd_data_list:
            job_title = jd_data['title']
            print(f"Matching: {job_title}")
            
            matches = self.match_jd_with_all_cvs(jd_data, cv_data_list)
            all_matches[job_title] = matches
        
        return all_matches
    
    def get_top_matches(self, all_matches: Dict[str, List[Tuple[Dict[str, Any], float]]], threshold: float = 0.0, top_n: int = None) -> Dict[str, List[Tuple[Dict[str, Any], float]]]:
        """Get top matches for each job description
        
        Args:
            all_matches: Dictionary mapping job title to list of (CV, score) tuples
            threshold: Minimum score threshold
            top_n: Maximum number of top matches to return
            
        Returns:
            Dictionary mapping job title to filtered list of (CV, score) tuples
        """
        filtered_matches = {}
        
        for job_title, matches in all_matches.items():
            # Filter by threshold
            threshold_matches = [(cv, score) for cv, score in matches if score >= threshold]
            
            # Limit to top N
            if top_n is not None:
                threshold_matches = threshold_matches[:top_n]
            
            filtered_matches[job_title] = threshold_matches
        
        return filtered_matches 