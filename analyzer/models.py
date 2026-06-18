from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

class ConfidenceLevel(Enum):
    """Confidence level for predictions"""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class FactorAnalysis:
    """Individual factor contributing to prediction"""
    name: str
    weight: float  # 0-1, importance multiplier
    positive_indicators: List[str] = field(default_factory=list)
    negative_indicators: List[str] = field(default_factory=list)
    current_value: float = 0.0  # Contribution to probability (-1 to 1)
    source: str = ""  # Data source
    last_updated: str = ""

@dataclass
class PredictionResult:
    """Complete prediction analysis result"""
    prediction: str
    probability: float  # 0-100
    confidence: ConfidenceLevel
    key_factors: List[FactorAnalysis] = field(default_factory=list)
    historical_context: str = ""
    detailed_reasoning: str = ""
    limiting_factors: List[str] = field(default_factory=list)
    supporting_factors: List[str] = field(default_factory=list)
    comparable_events: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    data_quality_score: float = 0.0  # 0-100, how reliable is the analysis
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "prediction": self.prediction,
            "probability": round(self.probability, 2),
            "confidence": self.confidence.value,
            "key_factors": [{
                "name": f.name,
                "weight": f.weight,
                "positive": f.positive_indicators,
                "negative": f.negative_indicators,
                "value": round(f.current_value, 3),
                "source": f.source
            } for f in self.key_factors],
            "historical_context": self.historical_context,
            "detailed_reasoning": self.detailed_reasoning,
            "limiting_factors": self.limiting_factors,
            "supporting_factors": self.supporting_factors,
            "comparable_events": self.comparable_events,
            "data_quality_score": round(self.data_quality_score, 2),
            "recommendations": self.recommendations
        }

    def __str__(self) -> str:
        """Pretty print the result"""
        output = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PREDICTION ANALYSIS REPORT                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Prediction: {self.prediction}

Probability: {self.probability:.1f}%
Confidence Level: {self.confidence.value.upper()}
Data Quality Score: {self.data_quality_score:.1f}%

─── SUPPORTING FACTORS ───
"""
        for factor in self.supporting_factors:
            output += f"✓ {factor}\n"

        output += "\n─── LIMITING FACTORS ───\n"
        for factor in self.limiting_factors:
            output += f"✗ {factor}\n"

        output += f"""

─── KEY CONTRIBUTING FACTORS ───
"""
        for factor in self.key_factors:
            output += f"\n• {factor.name} (Weight: {factor.weight:.1%})\n"
            output += f"  Impact: {factor.current_value:+.1%}\n"
            if factor.positive_indicators:
                output += f"  Positive: {', '.join(factor.positive_indicators)}\n"
            if factor.negative_indicators:
                output += f"  Negative: {', '.join(factor.negative_indicators)}\n"
            output += f"  Source: {factor.source}\n"

        output += f"""

─── HISTORICAL CONTEXT ───
{self.historical_context}

─── DETAILED REASONING ───
{self.detailed_reasoning}
"""
        if self.comparable_events:
            output += "\n─── COMPARABLE HISTORICAL EVENTS ───\n"
            for event in self.comparable_events:
                output += f"• {event.get('description', 'N/A')} - Probability: {event.get('probability', 'N/A')}\n"

        if self.recommendations:
            output += "\n─── RECOMMENDATIONS ───\n"
            for rec in self.recommendations:
                output += f"• {rec}\n"

        output += "\n" + "═" * 80 + "\n"
        return output
