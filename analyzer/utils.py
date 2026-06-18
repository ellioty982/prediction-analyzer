import re
from typing import Dict, Any, List

def classify_prediction(prediction: str) -> str:
    """
    Classify the type of prediction
    """
    prediction_lower = prediction.lower()
    
    # Sports keywords
    sports_keywords = ['win', 'champion', 'playoffs', 'finals', 'nba', 'nfl', 'mlb', 'soccer', 'game', 'team', 'score']
    if any(keyword in prediction_lower for keyword in sports_keywords):
        return "sports"
    
    # Weather keywords
    weather_keywords = ['snow', 'rain', 'weather', 'storm', 'sunny', 'temperature', 'climate']
    if any(keyword in prediction_lower for keyword in weather_keywords):
        return "weather"
    
    # Political keywords
    political_keywords = ['election', 'president', 'candidate', 'vote', 'congress', 'senate']
    if any(keyword in prediction_lower for keyword in political_keywords):
        return "political"
    
    # Financial keywords
    financial_keywords = ['stock', 'price', 'market', 'dollar', 'crypto', 'bitcoin', 'rise', 'fall']
    if any(keyword in prediction_lower for keyword in financial_keywords):
        return "financial"
    
    # Event keywords
    event_keywords = ['event', 'happen', 'occur', 'take place', 'arrive']
    if any(keyword in prediction_lower for keyword in event_keywords):
        return "event"
    
    return "general"

def extract_entities(prediction: str) -> Dict[str, Any]:
    """
    Extract key entities from prediction
    """
    entities = {}
    
    # Extract dates
    date_patterns = [
        r'(\d{4})',  # Year
        r'(\d{1,2}/\d{1,2})',  # MM/DD
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, prediction, re.IGNORECASE)
        if match:
            entities['date'] = match.group(0)
            break
    
    # Extract team names (basic)
    teams = ['knicks', 'lakers', 'celtics', 'warriors', 'bulls', 'heat', 'nets']
    for team in teams:
        if team in prediction.lower():
            entities['team'] = team.capitalize()
            break
    
    # Extract leagues
    if 'nba' in prediction.lower():
        entities['league'] = 'NBA'
    elif 'nfl' in prediction.lower():
        entities['league'] = 'NFL'
    elif 'mlb' in prediction.lower():
        entities['league'] = 'MLB'
    
    # Extract events
    events = ['finals', 'playoffs', 'championship', 'super bowl', 'world series']
    for event in events:
        if event in prediction.lower():
            entities['event'] = event.capitalize()
            break
    
    # Extract locations
    locations = ['new york', 'los angeles', 'chicago', 'boston', 'miami', 'denver']
    for location in locations:
        if location in prediction.lower():
            entities['location'] = location.capitalize()
            break
    
    # Extract weather conditions
    conditions = ['snow', 'rain', 'sunny', 'clear', 'cloudy', 'storm']
    for condition in conditions:
        if condition in prediction.lower():
            entities['weather_condition'] = condition
            break
    
    return entities

def calculate_base_probability(prediction_type: str) -> float:
    """
    Get base probability for different prediction types
    """
    base_probabilities = {
        "sports": 0.5,
        "weather": 0.5,
        "political": 0.5,
        "financial": 0.5,
        "event": 0.5,
        "general": 0.5
    }
    return base_probabilities.get(prediction_type, 0.5)

def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a value as a percentage string
    """
    return f"{value:.{decimals}f}%"

def get_confidence_text(confidence_value: float) -> str:
    """
    Get human-readable confidence text
    """
    if confidence_value > 0.8:
        return "Very High"
    elif confidence_value > 0.6:
        return "High"
    elif confidence_value > 0.4:
        return "Moderate"
    elif confidence_value > 0.2:
        return "Low"
    else:
        return "Very Low"
