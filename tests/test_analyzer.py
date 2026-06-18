import unittest
from analyzer import PredictionAnalyzer, PredictionResult

class TestPredictionAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = PredictionAnalyzer()
    
    def test_sports_prediction(self):
        """Test sports prediction analysis"""
        result = self.analyzer.analyze("Will the Knicks win the NBA Finals?")
        
        self.assertIsInstance(result, PredictionResult)
        self.assertIsNotNone(result.probability)
        self.assertGreaterEqual(result.probability, 0)
        self.assertLessEqual(result.probability, 100)
        self.assertIsNotNone(result.confidence)
        self.assertGreater(len(result.key_factors), 0)
    
    def test_weather_prediction(self):
        """Test weather prediction analysis"""
        result = self.analyzer.analyze("Will it snow in New York on Christmas?")
        
        self.assertIsInstance(result, PredictionResult)
        self.assertIsNotNone(result.probability)
    
    def test_general_prediction(self):
        """Test general prediction analysis"""
        result = self.analyzer.analyze("Will something happen?")
        
        self.assertIsInstance(result, PredictionResult)
        self.assertIsNotNone(result.probability)
    
    def test_result_to_dict(self):
        """Test conversion of result to dictionary"""
        result = self.analyzer.analyze("Will the Knicks win?")
        result_dict = result.to_dict()
        
        self.assertIn("prediction", result_dict)
        self.assertIn("probability", result_dict)
        self.assertIn("confidence", result_dict)

if __name__ == "__main__":
    unittest.main()
