import ast
from typing import List, Dict, Any 
from dataclasses import dataclass, asdict

@dataclass
class StaticPerfIssues:
    """Data Class for storing performance issue info"""
    line_number : int
    message : str 
    severity : str
    recommendation : str 

class StaticPerformanceAnalyzer:
    """Class for Static code performance analysis"""
    @staticmethod
    def analyze(code):
        """analyze code"""
        issues: List[StaticPerfIssues] = []
        try:
            tree = ast.parse(code)
            # Loop Issues : 
            nested_loop_issues = StaticPerformanceAnalyzer.detect_nested_loops(tree)
            issues.append(i for i in nested_loop_issues)
            # Repeated Computations :
            repeated_comp_issues = StaticPerformanceAnalyzer.detect_repeated_computations(tree)
            issues.append(i for i in repeated_comp_issues)
            # String Concatenation Issues : 
            str_concat_issues = StaticPerformanceAnalyzer.detect_string_concatenation(tree)
            issues.append(i for i in str_concat_issues)
        except SyntaxError as e:
            issues.append(StaticPerfIssues(
                line_number=e.lineno or 0,
                message=f"Syntax Error : {e}",
                severity="high",
                recommendation="Fix syntax errors before evaluation."
            ))
        return issues
    
    @staticmethod
    def detect_nested_loops(tree:ast.AST):
        class NestedLoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.nested_loops = []
                self.loop_depth = 0
            def visit_for(self,node):
                self.loop_depth += 1
                if self.loop_depth > 1:
                    self.nested_loops.append(node.lineno)
                self.generic_visit(node)
                self.loop_depth -= 1
            def visit_while(self,node):
                self.loop_depth += 1
                if self.loop_depth > 1:
                    self.nested_loops.append(node.lineno)
                self.generic_visit(node)
                self.loop_depth -= 1
        visitor = NestedLoopVisitor()
        visitor.visit(tree)
        return [
                StaticPerfIssues(
                    line_number=line,
                    message="Nested loop detected",
                    severity="high",
                    recommendation="Refactor to reduce loop nesting, use list comprehensions or generator expressions"
                ) for line in visitor.nested_loops
            ]

    @staticmethod
    def detect_string_concatenation(tree: ast.AST) -> List[StaticPerfIssues]:
        """Detect inefficient string concatenation."""
        class StringConcatVisitor(ast.NodeVisitor):
            def __init__(self):
                self.concat_lines = []

            def visit_BinOp(self, node):
                if isinstance(node.op, ast.Add) and isinstance(node.left, ast.Str) and isinstance(node.right, ast.Str):
                    self.concat_lines.append(node.lineno)
                self.generic_visit(node)

        visitor = StringConcatVisitor()
        visitor.visit(tree)

        return [
            StaticPerfIssues(
                line_number=line,
                message="Inefficient string concatenation",
                severity="medium",
                recommendation="Use f-strings, .format(), or ''.join() for better performance"
            ) for line in visitor.concat_lines
        ]

    @staticmethod
    def detect_repeated_computations(tree: ast.AST) -> List[StaticPerfIssues]:
        """Detect potential repeated computations."""
        class RepeatedComputationVisitor(ast.NodeVisitor):
            def __init__(self):
                self.assignments = {}
                self.repeated_lines = []

            def visit_Assign(self, node):
                if isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                    if var_name in self.assignments:
                        self.repeated_lines.append(node.lineno)
                    else:
                        self.assignments[var_name] = node.lineno
                self.generic_visit(node)

        visitor = RepeatedComputationVisitor()
        visitor.visit(tree)

        return [
            StaticPerfIssues(
                line_number=line,
                message="Potential repeated computation",
                severity="low",
                recommendation="Consider caching or memoizing expensive computations"
            ) for line in visitor.repeated_lines
        ]