import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def format_date(date: datetime) -> str:
    return date.strftime("%d/%m/%Y %H:%M")

def calculate_progress(scores: list) -> float:
    if not scores:
        return 0.0
    return sum(score.value for score in scores) / len(scores)