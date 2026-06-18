#!/usr/bin/env python3
"""
Main entry point for the Prediction Analyzer
"""

from analyzer import PredictionAnalyzer

def main():
    """Main function"""
    analyzer = PredictionAnalyzer()
    
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║           Welcome to the Prediction Analyzer                               ║")
    print("║     Analyze event probabilities with factual breakdowns                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    while True:
        print("\nEnter a prediction (or 'quit' to exit):")
        print("Examples:")
        print("  - Will the Knicks win the NBA Finals?")
        print("  - Will it snow on Christmas in New York?")
        print("  - Will Tesla stock reach $500 by 2027?")
        print()
        
        prediction = input("> ").strip()
        
        if prediction.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the Prediction Analyzer!")
            break
        
        if not prediction:
            print("Please enter a valid prediction.")
            continue
        
        print("\nAnalyzing prediction...\n")
        result = analyzer.analyze(prediction)
        print(result)

if __name__ == "__main__":
    main()
