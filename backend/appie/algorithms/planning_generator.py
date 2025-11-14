from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import pandas as pd

class PlanningGenerator:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_study_plan(self, user_id: str, rules: Dict[str, Any]) -> List[Dict]:
        user_weaknesses = self.analyze_user_weaknesses(user_id)
        study_plan = []
        start_date = datetime.now()
        
        for week in range(15):
            week_plan = self.generate_week_schedule(
                user_weaknesses, week, start_date, rules
            )
            study_plan.extend(week_plan)
        
        return study_plan
    
    def analyze_user_weaknesses(self, user_id: str) -> List[Dict]:
        from appie.crud.crud_score import get_user_scores
        scores = get_user_scores(self.db, user_id)
        
        if not scores:
            return []
        
        score_data = []
        for score in scores:
            score_data.append({
                'module_id': score.module_id,
                'module_name': score.module.name,
                'score': score.value,
                'date': score.created_at
            })
        
        df = pd.DataFrame(score_data)
        if df.empty:
            return []
            
        module_performance = df.groupby('module_id').agg({
            'score': ['mean', 'count'],
            'module_name': 'first'
        }).round(3)
        
        module_performance.columns = ['average_score', 'attempt_count', 'module_name']
        module_performance = module_performance.reset_index()
        
        weaknesses = []
        for _, row in module_performance.iterrows():
            avg_score = row['average_score']
            
            if avg_score < 0.6:
                priority = "high"
            elif avg_score < 0.8:
                priority = "medium"
            else:
                priority = "low"
            
            weaknesses.append({
                'module_id': row['module_id'],
                'module_name': row['module_name'],
                'average_score': avg_score,
                'attempt_count': row['attempt_count'],
                'priority': priority
            })
        
        priority_order = {"high": 0, "medium": 1, "low": 2}
        weaknesses.sort(key=lambda x: priority_order[x['priority']])
        
        return weaknesses
    
    def generate_week_schedule(self, weaknesses: List[Dict], week: int, 
                             start_date: datetime, rules: Dict) -> List[Dict]:
        sessions = []
        week_start = start_date + timedelta(weeks=week)
        
        high_priority = [w for w in weaknesses if w['priority'] == 'high']
        medium_priority = [w for w in weaknesses if w['priority'] == 'medium']
        low_priority = [w for w in weaknesses if w['priority'] == 'low']
        
        total_sessions = rules.get('sessions_per_week', 5)
        allocation = self.allocate_sessions(
            total_sessions, len(high_priority), len(medium_priority), len(low_priority)
        )
        
        session_count = 0
        
        for i in range(min(allocation['high'], len(high_priority))):
            sessions.append(self.create_session(high_priority[i], week_start, session_count, rules))
            session_count += 1
        
        for i in range(min(allocation['medium'], len(medium_priority))):
            sessions.append(self.create_session(medium_priority[i], week_start, session_count, rules))
            session_count += 1
        
        for i in range(min(allocation['low'], len(low_priority))):
            sessions.append(self.create_session(low_priority[i], week_start, session_count, rules))
            session_count += 1
        
        return sessions
    
    def allocate_sessions(self, total_sessions: int, high_count: int, 
                         medium_count: int, low_count: int) -> Dict[str, int]:
        high_sessions = min(high_count, max(1, round(total_sessions * 0.6)))
        medium_sessions = min(medium_count, max(1, round(total_sessions * 0.3)))
        low_sessions = min(low_count, max(1, round(total_sessions * 0.1)))
        
        remaining = total_sessions - (high_sessions + medium_sessions + low_sessions)
        if remaining > 0:
            high_sessions += remaining
        
        return {
            'high': high_sessions,
            'medium': medium_sessions,
            'low': low_sessions
        }
    
    def create_session(self, module: Dict, week_start: datetime, 
                      session_index: int, rules: Dict) -> Dict:
        session_date = week_start + timedelta(days=session_index * 2)
        
        return {
            'module_id': module['module_id'],
            'module_name': module['module_name'],
            'date': session_date.isoformat(),
            'duration': rules.get('session_duration', 60),
            'objectives': [
                f"Révision {module['module_name']}",
                "Exercices pratiques",
                "Révision des points difficiles"
            ],
            'priority': module['priority'],
            'week': session_index // rules.get('sessions_per_week', 5) + 1
        }