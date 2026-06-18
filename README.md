# Prediction Analyzer

A comprehensive prediction analysis system that evaluates the likelihood of events occurring based on **real, live data** from powerful free APIs.

## ✨ Features

- **📊 Real API Integrations**: ESPN, Open-Meteo (FREE weather), Alpha Vantage, NewsAPI
- **🎯 Smart Analysis**: Multiple prediction types (sports, weather, financial, political)
- **📈 Probability Calculation**: Get precise percentage chances with confidence levels
- **📝 Factual Breakdown**: Detailed reasoning with supporting evidence & sources
- **🔄 Auto-Caching**: Intelligent 1-hour caching to minimize API calls
- **📚 Historical Context**: Analysis of similar past events
- **🎨 Beautiful Reports**: Professional formatted predictions with key factors

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ellioty982/prediction-analyzer.git
cd prediction-analyzer

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy environment template
cp .env.example .env
```

### Basic Usage

```python
from analyzer import PredictionAnalyzer

# Initialize analyzer
analyzer = PredictionAnalyzer()

# Analyze a prediction
result = analyzer.analyze("Will the Knicks win the NBA Finals?")
print(result)
```

### Interactive CLI

```bash
python main.py
```

Then enter predictions like:
- `Will the Knicks win the NBA Finals?`
- `Will it snow on Christmas in New York?`
- `Will Tesla stock reach $500 by 2027?`

## 🔌 API Integrations

### **Sports 🏀** - ESPN API (FREE)
- Real NBA team statistics and standings
- Current season performance data
- Playoff probabilities
- **No authentication required**

```python
analyzer.analyze("Will the Lakers win the NBA Finals?")
# Pulls live standings, win rates, and roster data
```

### **Weather 🌧️** - Open-Meteo API (COMPLETELY FREE)
- Historical climate data (365 days)
- 7-day weather forecasts
- Precipitation & snowfall probabilities
- **Zero rate limiting, no API key needed!**

```python
analyzer.analyze("Will it snow on Christmas in New York?")
# Uses real historical weather patterns + current forecast
```

### **Financial 💰** - Alpha Vantage API (FREE tier)
- Real-time stock quotes
- Historical price data
- Technical indicators
- Get free key: https://www.alphavantage.co/

```python
analyzer.analyze("Will Tesla stock reach $500 by 2027?")
# Includes current price, trends, support/resistance
```

### **News 📰** - NewsAPI (FREE tier)
- Latest relevant articles
- Sentiment context
- Source tracking
- Get free key: https://newsapi.org/

## ⚙️ Configuration

### Setup API Keys (Optional)

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
# Open-Meteo needs NO key - it's completely free!
```

If no API keys are provided:
- ✅ Weather data still works (Open-Meteo is free)
- ✅ Sports data still works (ESPN is free)
- ⚠️ Stock & News use mock data

### Get Free API Keys

1. **Alpha Vantage** (Stocks):
   - Visit: https://www.alphavantage.co/
   - Free tier: 5 calls/min, 500 calls/day
   - No credit card required

2. **NewsAPI** (News):
   - Visit: https://newsapi.org/
   - Free tier: 100 requests/day
   - Instant activation

3. **Open-Meteo** (Weather):
   - No registration needed! Completely free
   - Unlimited requests (reasonable limits)
   - Includes 365 days of historical data

## 📊 Prediction Types

### Sports Predictions
Analyzes: historical performance, current season record, roster quality, competition strength, playoff position

```
Prediction: Will the Knicks win the NBA Finals?
Probability: 4.2%
Confidence: MODERATE
Data Quality: 85%
```

### Weather Predictions
Analyzes: historical climate patterns, current forecast, seasonal anomalies, precipitation trends

```
Prediction: Will it snow on Christmas in New York?
Probability: 32.5%
Confidence: HIGH
Data Quality: 90%
```

### Financial Predictions
Analyzes: current price, historical volatility, support/resistance, market trends

```
Prediction: Will Tesla stock reach $500?
Probability: 28.3%
Confidence: MODERATE
Data Quality: 87%
```

## 📈 Output Format

Every prediction returns:

```
━━━━━━━━━━━━━━━━ PREDICTION ANALYSIS REPORT ━━━━━━━━━━━━━━━━

Prediction: [Your question]

Probability: 42.5%
Confidence Level: HIGH
Data Quality Score: 87.3%

✓ SUPPORTING FACTORS
  - Above-average historical win rate
  - Strong current season performance
  
✗ LIMITING FACTORS
  - Very strong conference/league competition
  - Recent injury to key player

━━━━ KEY CONTRIBUTING FACTORS ━━━━

• Historical Performance (Weight: 25%)
  Impact: +15%
  Source: Official League Records

• Current Season Performance (Weight: 25%)
  Impact: +18%
  Source: Current Season Stats

━━━━ DETAILED REASONING ━━━━
[Multi-paragraph analysis with supporting evidence]
```

## 🏗️ Project Structure

```
prediction-analyzer/
├── analyzer/
│   ├── __init__.py              # Package initialization
│   ├── core.py                  # Main PredictionAnalyzer class
│   ├── models.py                # Data structures & ConfidenceLevel
│   ├── data_sources.py          # Real API integrations
│   └── utils.py                 # Helper functions & classification
├── main.py                      # Interactive CLI entry point
├── tests/
│   └── test_analyzer.py         # Unit tests
├── requirements.txt             # Python dependencies
├── .env.example                 # API key template
├── .gitignore                   # Git configuration
└── README.md                    # This file
```

## 🔧 Dependencies

- **requests** - HTTP client for API calls
- **pandas** - Data analysis & manipulation
- **numpy** - Numerical computing
- **python-dotenv** - Environment variable management
- **scipy & scikit-learn** - Statistical analysis

See `requirements.txt` for complete list.

## 📝 Examples

### Example 1: Sports Analysis

```bash
$ python main.py
> Will the Lakers win the NBA Finals?

Analyzing prediction...

Prediction: Will the Lakers win the NBA Finals?

Probability: 12.5%
Confidence Level: MODERATE
Data Quality Score: 87.0%

✓ SUPPORTING FACTORS
  - Strong current season performance
  - Above-average roster quality

✗ LIMITING FACTORS
  - Team has never won a championship
  - Very strong conference/league competition
```

### Example 2: Weather Analysis

```bash
> Will it snow on Christmas in New York?

Analyzing prediction...

Probability: 32.5%
Confidence Level: HIGH
Data Quality Score: 90.0%

✓ SUPPORTING FACTORS
  - Historical snow patterns support possibility

✗ LIMITING FACTORS
  - Current forecast indicates lower probability

KEY FACTORS:
  Historical Climate Pattern (35%): +2.1%
  Current Weather Forecast (40%): -12.5%
  Seasonal Patterns (25%): +5.0%
```

## 🎯 Roadmap

- [ ] Political prediction analysis with polling data
- [ ] Cryptocurrency price predictions
- [ ] Sports injury impact modeling
- [ ] Advanced machine learning models
- [ ] Web interface (Flask/React)
- [ ] Real-time WebSocket updates
- [ ] Custom prediction categories
- [ ] Historical accuracy tracking

## 🧪 Testing

Run unit tests:

```bash
python -m pytest tests/ -v
```

Or run individual test:

```bash
python tests/test_analyzer.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Tips & Tricks

### Getting Better Predictions

1. **Be specific**: "Will the Lakers win the 2024 NBA Finals?" is better than "Will the Lakers win?"
2. **Include locations**: Weather predictions need geographic context
3. **Add timeframes**: "By end of 2025?" vs "eventually?"

### Improving Data Quality

- Add Alpha Vantage key for accurate stock data
- Add NewsAPI key for contextual news analysis
- No key needed for weather (Open-Meteo is fully free!)

### Caching

API responses are cached for 1 hour by default. To clear:

```python
analyzer.data_source.clear_cache()
```

## 🐛 Troubleshooting

**Q: Getting mock data instead of real data?**
A: Check your `.env` file. Weather works without a key (Open-Meteo is free). Sports uses free ESPN API. If stocks/news show mock data, add your API keys.

**Q: Rate limit errors?**
A: The cache helps! Most calls are cached for 1 hour. If still hitting limits, try using different prediction topics to spread requests.

**Q: Open-Meteo showing old data?**
A: Historical data is normal - it's by design. For current forecasts, the system uses the 7-day forecast endpoint automatically.

---

**Made with ❤️ for accurate, factual predictions**
