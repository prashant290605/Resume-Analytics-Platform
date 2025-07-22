from typing import Dict, List, Any, Tuple
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ShortlisterAgent:
    """Agent to shortlist candidates based on match scores"""
    
    def __init__(self, threshold: float = 80.0):
        """Initialize Shortlister Agent
        
        Args:
            threshold: Minimum score threshold for shortlisting (default: 80.0)
        """
        self.threshold = threshold
    
    def shortlist_candidates(self, matches: Dict[str, List[Tuple[Dict[str, Any], float]]]) -> Dict[str, List[Tuple[Dict[str, Any], float]]]:
        """Shortlist candidates based on match score threshold
        
        Args:
            matches: Dictionary mapping job title to list of (CV, score) tuples
            
        Returns:
            Dictionary mapping job title to shortlisted (CV, score) tuples
        """
        shortlisted = {}
        
        for job_title, job_matches in matches.items():
            # Filter by threshold
            job_shortlisted = [(cv, score) for cv, score in job_matches if score >= self.threshold]
            
            if job_shortlisted:
                shortlisted[job_title] = job_shortlisted
        
        return shortlisted
    
    def print_shortlist_summary(self, shortlisted: Dict[str, List[Tuple[Dict[str, Any], float]]]) -> None:
        """Print summary of shortlisted candidates
        
        Args:
            shortlisted: Dictionary mapping job title to shortlisted (CV, score) tuples
        """
        print("\n===== SHORTLISTED CANDIDATES =====")
        
        for job_title, candidates in shortlisted.items():
            print(f"\nJob: {job_title}")
            print(f"Number of shortlisted candidates: {len(candidates)}")
            
            for i, (cv, score) in enumerate(candidates[:10], 1):  # Show top 10
                name = cv.get('name', 'Unknown')
                email = cv.get('email', 'N/A')
                print(f"  {i}. {name} ({email}) - Score: {score:.2f}%")
    
    def get_shortlist_data(self, shortlisted: Dict[str, List[Tuple[Dict[str, Any], float]]]) -> List[Dict[str, Any]]:
        """Convert shortlisted candidates to a flat list format
        
        Args:
            shortlisted: Dictionary mapping job title to shortlisted (CV, score) tuples
            
        Returns:
            List of candidate data dictionaries with job information
        """
        shortlist_data = []
        
        for job_title, candidates in shortlisted.items():
            for cv, score in candidates:
                candidate_data = cv.copy()  # Make a copy to avoid modifying original
                candidate_data['job_title'] = job_title
                candidate_data['match_score'] = score
                shortlist_data.append(candidate_data)
        
        return shortlist_data 