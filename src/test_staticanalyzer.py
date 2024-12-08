import unittest
from static_performance_analyzer import StaticPerformanceAnalyzer, StaticPerfIssues

class TestStaticPerformanceAnalyzer(unittest.TestCase):

    def test_analyze_syntax_error(self):
        code = "def foo():\n  print('Hello World'\n"
        issues = StaticPerformanceAnalyzer.analyze(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].message, "Syntax Error : unexpected EOF while parsing")
        self.assertEqual(issues[0].severity, "high")
        self.assertEqual(issues[0].recommendation, "Fix syntax errors before evaluation.")

    def test_analyze_nested_loops(self):
        code = "for i in range(10):\n  for j in range(10):\n    print(i, j)"
        issues = StaticPerformanceAnalyzer.analyze(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].message, "Nested loop detected")
        self.assertEqual(issues[0].severity, "high")
        self.assertEqual(issues[0].recommendation, "Refactor to reduce loop nesting, use list comprehensions or generator expressions")

    def test_analyze_string_concatenation(self):
        code = "s = 'Hello ' + 'World'"
        issues = StaticPerformanceAnalyzer.analyze(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].message, "Inefficient string concatenation")
        self.assertEqual(issues[0].severity, "medium")
        self.assertEqual(issues[0].recommendation, "Use f-strings, .format(), or ''.join() for better performance")

    def test_analyze_repeated_computations(self):
        code = "x = 5\nx = 5"
        issues = StaticPerformanceAnalyzer.analyze(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].message, "Potential repeated computation")
        self.assertEqual(issues[0].severity, "low")
        self.assertEqual(issues[0].recommendation, "Consider caching or memoizing expensive computations")

    def test_analyze_multiple_issues(self):
        code = "for i in range(10):\n  for j in range(10):\n    s = 'Hello ' + 'World'\nx = 5\nx = 5"
        issues = StaticPerformanceAnalyzer.analyze(code)
        self.assertEqual(len(issues), 3)
        self.assertEqual(issues[0].message, "Nested loop detected")
        self.assertEqual(issues[1].message, "Inefficient string concatenation")
        self.assertEqual(issues[2].message, "Potential repeated computation")

if __name__ == '__main__':
    unittest.main()