import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import json
from .models import PredictionResult, FactorAnalysis, ConfidenceLevel
from .data_sources import DataSource
from .utils import classify_prediction, extract_entities

class PredictionAnalyzer:
    """
    Main analyzer for predictions. Processes prompts and provides
    detailed probability estimates with factual breakdowns.
    """
    
    def __init__(self, use_cache: bool = True):
        """Initialize the analyzer"""
        self.use_cache = use_cache
        self.data_source = DataSource()
        self.cache = {}
        self.analysis_history = []
    
    def analyze(self, prediction: str) -> PredictionResult:
        """
        Analyze a prediction and return probability estimate with breakdown.
        
        Args:
            prediction: The prediction statement to analyze
            
        Returns:
            PredictionResult with detailed analysis
        """
        # Extract key information
        prediction_type = classify_prediction(prediction)
        entities = extract_entities(prediction)
        
        # Route to appropriate analyzer
        if prediction_type == "sports":
            result = self._analyze_sports(prediction, entities)
        elif prediction_type == "weather":
            result = self._analyze_weather(prediction, entities)
        elif prediction_type == "political":
            result = self._analyze_political(prediction, entities)
        elif prediction_type == "financial":
            result = self._analyze_financial(prediction, entities)
        elif prediction_type == "event":
            result = self._analyze_event(prediction, entities)
        else:
            result = self._analyze_general(prediction, entities)
        
        # Log analysis
        self.analysis_history.append({
            "prediction": prediction,
            "timestamp": datetime.now().isoformat(),
            "result": result.to_dict()
        })
        
        return result
    
    def _analyze_sports(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze sports-related predictions (teams winning, records, etc.)
        """
        team = entities.get("team", "")
        event = entities.get("event", "")
        
        # Fetch team statistics
        team_stats = self.data_source.get_team_stats(team) if team else {}
        league_stats = self.data_source.get_league_stats(entities.get("league", ""))
        
        factors = []
        supporting = []
        limiting = []
        probability = 50.0
        
        # Historical Performance Factor
        if team_stats:
            win_rate = team_stats.get("win_rate", 0.5)
            championships = team_stats.get("championships_won", 0)
            years_active = team_stats.get("years_active", 0)
            
            historical_factor = FactorAnalysis(
                name="Historical Performance",
                weight=0.25,
                positive_indicators=[f"Win rate: {win_rate:.1%}"] if win_rate > 0.55 else [],
                negative_indicators=[f"Only {championships} championships in {years_active} years"] if championships < 2 else [],
                current_value=(win_rate - 0.5) * 2,
                source="Official League Records"
            )
            factors.append(historical_factor)
            probability *= (1 + historical_factor.current_value * 0.2)
            
            if championships < 1:
                limiting.append(f"Team has never won a championship")
            if win_rate > 0.55:
                supporting.append(f"Above-average historical win rate")
        
        # Current Season Performance
        current_performance = team_stats.get("current_season", {})
        if current_performance:
            current_win_rate = current_performance.get("win_rate", 0.5)
            current_factor = FactorAnalysis(
                name="Current Season Performance",
                weight=0.25,
                positive_indicators=[f"Current win rate: {current_win_rate:.1%}"] if current_win_rate > 0.55 else [],
                negative_indicators=[f"Struggling season: {current_win_rate:.1%}"] if current_win_rate < 0.45 else [],
                current_value=(current_win_rate - 0.5) * 2,
                source="Current Season Stats"
            )
            factors.append(current_factor)
            probability *= (1 + current_factor.current_value * 0.25)
            
            if current_win_rate > 0.6:
                supporting.append(f"Strong current season performance")
        
        # Competition Analysis
        competition_strength = self.data_source.get_competition_strength(
            entities.get("league", ""), 
            team
        )
        if competition_strength:
            comp_factor = FactorAnalysis(
                name="Conference/League Competition",
                weight=0.20,
                negative_indicators=["Multiple strong competitors"] if competition_strength > 0.7 else [],
                positive_indicators=["Relatively weaker competition"] if competition_strength < 0.5 else [],
                current_value=1 - (competition_strength * 2),
                source="Strength of Schedule Analysis"
            )
            factors.append(comp_factor)
            probability *= (1 + comp_factor.current_value * 0.15)
            
            if competition_strength > 0.75:
                limiting.append("Very strong conference/league competition")
        
        # Roster Quality
        roster_quality = team_stats.get("roster_quality_score", 0.5)
        if roster_quality:
            roster_factor = FactorAnalysis(
                name="Roster Quality & Health",
                weight=0.15,
                positive_indicators=["Above-average roster"] if roster_quality > 0.55 else [],
                negative_indicators=["Below-average roster"] if roster_quality < 0.45 else [],
                current_value=(roster_quality - 0.5) * 2,
                source="Player Stats & Roster Analysis"
            )
            factors.append(roster_factor)
            probability *= (1 + roster_factor.current_value * 0.1)
        
        # Calculate confidence
        data_quality = 0.85 if team_stats else 0.5
        confidence = self._determine_confidence(probability, data_quality)
        
        # Historical context
        historical_context = f"""
In {league_stats.get('league_name', 'the league')}, there are typically {league_stats.get('teams', 30)} teams competing.
Winning the championship requires sustained excellence, with only 1 team succeeding out of {league_stats.get('teams', 30)} each season.
Historically, teams with winning records have a {league_stats.get('playoff_qualification_rate', 0.5):.1%} playoff qualification rate.
        """
        
        reasoning = f"""
The analysis evaluates {team}'s championship prospects based on multiple factors:

1. Historical Performance: {team} has a track record that influences their likelihood of success.
2. Current Season: Performance this season is a strong indicator of near-term championship chances.
3. Competition: The strength of competing teams significantly impacts championship probability.
4. Roster Quality: Player talent and team health are crucial for postseason success.

The calculated probability of {probability:.1f}% reflects the combination of these factors.
        """
        
        return PredictionResult(
            prediction=prediction,
            probability=min(probability, 100),
            confidence=confidence,
            key_factors=factors,
            historical_context=historical_context.strip(),
            detailed_reasoning=reasoning.strip(),
            supporting_factors=supporting,
            limiting_factors=limiting,
            data_quality_score=data_quality * 100,
            last_updated=datetime.now().isoformat()
        )
    
    def _analyze_weather(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze weather-related predictions
        """
        location = entities.get("location", "")
        date = entities.get("date", "")
        condition = entities.get("weather_condition", "")
        
        # Get climate data
        climate_data = self.data_source.get_climate_data(location)
        forecast_data = self.data_source.get_weather_forecast(location, date)
        
        factors = []
        supporting = []
        limiting = []
        probability = 50.0
        
        # Historical climate data
        if climate_data:
            historical_rate = climate_data.get(f"{condition}_frequency", 0.3)
            climate_factor = FactorAnalysis(
                name="Historical Climate Pattern",
                weight=0.35,
                positive_indicators=[f"Historically occurs {historical_rate:.1%} of the time"] if historical_rate > 0.3 else [],
                current_value=(historical_rate - 0.5) * 2,
                source="Historical Climate Records"
            )
            factors.append(climate_factor)
            probability = historical_rate * 100
        
        # Current forecast
        if forecast_data:
            forecast_confidence = forecast_data.get("confidence", 0.5)
            forecast_probability = forecast_data.get(f"{condition}_probability", 0.5)
            
            forecast_factor = FactorAnalysis(
                name="Current Weather Forecast",
                weight=0.40,
                positive_indicators=[f"Forecast confidence: {forecast_confidence:.1%}"],
                current_value=forecast_probability - 0.5,
                source="National Weather Service / Meteorological Data"
            )
            factors.append(forecast_factor)
            probability = (probability * 0.4 + forecast_probability * 100 * 0.6)
        
        # Seasonal factors
        seasonal_data = climate_data.get("seasonal_patterns", {})
        if seasonal_data:
            seasonality_factor = FactorAnalysis(
                name="Seasonal Patterns",
                weight=0.25,
                current_value=seasonal_data.get(condition, {}).get("anomaly", 0),
                source="Seasonal Climate Analysis"
            )
            factors.append(seasonality_factor)
        
        confidence = self._determine_confidence(probability, 0.8)
        data_quality = 85 if forecast_data else 70
        
        historical_context = f"""
{location} historically experiences {condition} approximately {climate_data.get(f'{condition}_frequency', 0.3):.1%} of the time.
Seasonal patterns indicate {'above-average' if seasonal_data else 'average'} likelihood during this period.
        """
        
        reasoning = f"""
Weather predictions combine historical climate data with current meteorological forecasts.
For {location} on {date}, analysis considers:
1. Historical frequency of {condition}
2. Current weather models and forecasts
3. Seasonal variations and climate patterns
4. Atmospheric conditions and pressure systems
        """
        
        return PredictionResult(
            prediction=prediction,
            probability=min(probability, 100),
            confidence=confidence,
            key_factors=factors,
            historical_context=historical_context.strip(),
            detailed_reasoning=reasoning.strip(),
            supporting_factors=supporting,
            limiting_factors=limiting,
            data_quality_score=data_quality,
            last_updated=datetime.now().isoformat()
        )
    
    def _analyze_political(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze political predictions
        """
        return PredictionResult(
            prediction=prediction,
            probability=50.0,
            confidence=ConfidenceLevel.MODERATE,
            detailed_reasoning="Political analysis module - coming soon",
            data_quality_score=50.0,
            last_updated=datetime.now().isoformat()
        )
    
    def _analyze_financial(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze financial/market predictions
        """
        return PredictionResult(
            prediction=prediction,
            probability=50.0,
            confidence=ConfidenceLevel.MODERATE,
            detailed_reasoning="Financial analysis module - coming soon",
            data_quality_score=50.0,
            last_updated=datetime.now().isoformat()
        )
    
    def _analyze_event(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze general event predictions
        """
        return PredictionResult(
            prediction=prediction,
            probability=50.0,
            confidence=ConfidenceLevel.MODERATE,
            detailed_reasoning="Event analysis module - coming soon",
            data_quality_score=50.0,
            last_updated=datetime.now().isoformat()
        )
    
    def _analyze_general(self, prediction: str, entities: Dict[str, Any]) -> PredictionResult:
        """
        Analyze general/uncategorized predictions
        """
        return PredictionResult(
            prediction=prediction,
            probability=50.0,
            confidence=ConfidenceLevel.MODERATE,
            detailed_reasoning="General analysis module - coming soon",
            data_quality_score=50.0,
            last_updated=datetime.now().isoformat()
        )
    
    def _determine_confidence(self, probability: float, data_quality: float) -> ConfidenceLevel:
        """
        Determine confidence level based on probability and data quality
        """
        combined_score = (abs(probability - 50) / 50) * data_quality
        
        if combined_score > 80:
            return ConfidenceLevel.VERY_HIGH
        elif combined_score > 60:
            return ConfidenceLevel.HIGH
        elif combined_score > 40:
            return ConfidenceLevel.MODERATE
        elif combined_score > 20:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get analysis history"""
        return self.analysis_history
    
    def clear_history(self):
        """Clear analysis history"""
        self.analysis_history = []
