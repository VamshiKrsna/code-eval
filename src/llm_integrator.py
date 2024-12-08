import os
import google.generativeai as genai
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

@dataclass
class PerformanceInsight:
    """Data structure for performance insight from AI analysis."""
    line_number: Optional[int]
    issue_type: str
    description: str
    suggested_optimization: str
    severity: str

class LLMPerformanceAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini with your API key.
        """
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Google AI API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_code_performance(self, code: str) -> List[PerformanceInsight]:
        """
        Analyze code for performance bottlenecks using Gemini Flash.
        """
        prompt = f"""Perform a deep performance analysis on the following Python code.
        Provide insights in a clear, structured format with these details for each performance issue:
        - Line Number
        - Issue Type
        - Description
        - Suggested Optimization
        - Severity (low/medium/high)

        Code to analyze:
        ```python
        {code}
        ```

        Example output format:
        Line Number: 3
        Issue Type: Nested Loops
        Description: Inefficient nested loop causing O(n^2) time complexity
        Suggested Optimization: Consider list comprehension or generator expressions
        Severity: medium
        """
        
        try:
            response = self.model.generate_content(
                prompt, 
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.2
                )
            )
            
            # Parse and return insights
            insights = self.parse_insights(response.text)
            return insights
        
        except Exception as e:
            print(f"Error during analysis: {e}")
            return [
                PerformanceInsight(
                    line_number=None,
                    issue_type='analysis_error',
                    description=str(e),
                    suggested_optimization='Manual review recommended',
                    severity='high'
                )
            ]

    def parse_insights(self, response_text: str) -> List[PerformanceInsight]:
        """
        Parse AI-generated insights into structured objects.
        More robust parsing method.
        """
        insights = []
        
        insight_blocks = response_text.split('\n\n')
        
        for block in insight_blocks:
            # skip the empty blocks
            if not block.strip():
                continue
            
            # Initialize insight dictionary
            insight_data = {
                'line_number': None,
                'issue_type': 'Unknown',
                'description': 'No description provided',
                'suggested_optimization': 'No optimization suggested',
                'severity': 'low'
            }
            
            for line in block.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.lower().replace(' ', '_')
                    value = value.strip()
                    
                    if key == 'line_number':
                        try:
                            insight_data['line_number'] = int(value)
                        except ValueError:
                            insight_data['line_number'] = None
                    elif key == 'issue_type':
                        insight_data['issue_type'] = value
                    elif key == 'description':
                        insight_data['description'] = value
                    elif key == 'suggested_optimization':
                        insight_data['suggested_optimization'] = value
                    elif key == 'severity':
                        insight_data['severity'] = value
            
            if any([insight_data['issue_type'] != 'Unknown', 
                    insight_data['description'] != 'No description provided']):
                try:
                    insights.append(PerformanceInsight(**insight_data))
                except TypeError as e:
                    print(f"Error creating insight: {e}")
        
        return insights

if __name__ == "__main__":
    # Sample code to test
    sample_code = """
    for i in range(10):
        for j in range(5):
            print(i, j)
    greeting = "Hello " + "World"
    x = 42
    x = 42
    """

    try:
        load_dotenv()
        apikey = os.getenv("GEMINI_API_KEY")
        analyzer = LLMPerformanceAnalyzer(api_key=apikey)
        performance_insights = analyzer.analyze_code_performance(sample_code)
        
        print("\nPerformance Insights:")
        for insight in performance_insights:
            print(asdict(insight))
    
    except ValueError as e:
        print(f"Initialization error: {e}")