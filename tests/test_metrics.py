"""
Тесты для модуля metrics
"""
import pytest
from src.metrics import CodeMetrics


def test_simple_code_analysis():
    """Тест базового анализа кода"""
    code = """
def hello(name):
    return f"Hello, {name}!"
"""
    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    assert metrics['functions']['count'] == 1
    assert metrics['total_lines'] > 0


def test_docstring_detection():
    """Тест обнаружения docstrings"""
    code = '''
def documented_function():
    """This function has a docstring"""
    pass

def undocumented_function():
    pass
'''
    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    assert metrics['docstrings']['total_functions'] == 2
    assert metrics['docstrings']['functions_documented'] == 1
    assert metrics['docstrings']['coverage_percent'] == 50.0


def test_complexity_calculation():
    """Тест расчёта сложности"""
    code = """
def complex_function(x):
    if x > 0:
        if x > 10:
            return "big"
        else:
            return "small"
    else:
        return "negative"
"""
    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    assert metrics['complexity']['maximum'] >= 3


def test_class_detection():
    """Тест обнаружения классов"""
    code = """
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass
"""
    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    assert metrics['classes']['count'] == 1
    assert 'MyClass' in metrics['classes']['names']


def test_invalid_syntax():
    """Тест обработки невалидного синтаксиса"""
    code = "def invalid syntax here"

    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    # Должны вернуться пустые метрики
    assert metrics['functions']['count'] == 0
    assert metrics['overall_score']['total'] == 0.0


def test_empty_code():
    """Тест пустого кода"""
    code = ""

    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    assert metrics['total_lines'] == 1
    assert metrics['code_lines'] == 0


def test_score_calculation():
    """Тест расчёта общего балла"""
    code = '''
"""Module docstring"""

def well_documented_function(x):
    """This is well documented"""
    return x * 2

def test_well_documented():
    """Test function"""
    assert well_documented_function(2) == 4
'''
    analyzer = CodeMetrics(code, "test.py")
    metrics = analyzer.analyze()

    score = metrics['overall_score']
    assert 'total' in score
    assert 'letter_grade' in score
    assert 0 <= score['total'] <= 100
    assert score['letter_grade'] in ['A', 'B', 'C', 'D', 'F']
